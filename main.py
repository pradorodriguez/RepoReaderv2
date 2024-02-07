#main.py
import os
import tempfile
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureOpenAI
from config import WHITE, GREEN, RESET_COLOR
from utils import format_user_question
from file_processing import clone_github_repo, load_and_index_files
from questions import ask_question, QuestionContext

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_version = os.getenv("OPENAI_API_VERSION")
openai_api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
model_name = os.getenv("AZURE_DEPLOYMENT_NAME")

def main():
    github_url = input("Enter the GitHub URL of the repository: ")
    repo_name = github_url.split("/")[-1]
    print("Cloning the repository...")
    with tempfile.TemporaryDirectory() as local_path:
        if clone_github_repo(github_url, local_path):
            index, documents, file_type_counts, filenames = load_and_index_files(local_path)
            if index is None:
                print("No documents were found to index. Exiting.")
                exit()

            print("Repository cloned. Indexing files...")
            
            llm = AzureOpenAI(
                azure_deployment=model_name,
                azure_endpoint=openai_api_base,
                openai_api_version=openai_api_version,          
                temperature=0.2
                )

            template = """
            Repo: {repo_name} ({github_url}) | Conv: {conversation_history} | Docs: {numbered_documents} | Q: {question} | FileCount: {file_type_counts} | FileNames: {filenames}

            Instr:
            1. Answer based on context/docs.
            2. Focus on repo/code.
            3. Consider:
                a. Purpose/features - describe.
                b. Functions/code - provide details/samples.
                c. Setup/usage - give instructions.
            4. Unsure? Say "I am not sure".

            Answer:
            """

            prompt = PromptTemplate(
                template=template,
                input_variables=["repo_name", "github_url", "conversation_history", "question", "numbered_documents", "file_type_counts", "filenames"]
            )

            llm_chain = LLMChain(prompt=prompt, llm=llm)

            conversation_history = ""
            question_context = QuestionContext(index, documents, llm_chain, model_name, repo_name, github_url, conversation_history, file_type_counts, filenames)
            
            while True:
                try:
                    user_question = input("\n" + WHITE + "Ask a question about the repository (type 'exit()' to quit): " + RESET_COLOR)
                    if user_question.lower() == "exit()":
                        break
                    print('Thinking...')
                    user_question = format_user_question(user_question)

                    answer = ask_question(user_question, question_context)
                    print(GREEN + '\nANSWER\n' + answer + RESET_COLOR + '\n')
                    conversation_history += f"Question: {user_question}\nAnswer: {answer}\n"
                except Exception as e:
                    print(f"An error occurred: {e}")
                    #break

        else:
            print("Failed to clone the repository.")