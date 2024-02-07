# RepoReaderv2

This is a demo application to test the benefits of Azure OpenAI with the content of ALZ GitHub repositories.

## Requirements

1. Git.
1. Python >= 3.81.
1. Azure OpenAI information:
    1. Endpoint
    1. Key
    1. Model Deployment Name
1. A GitHub repository with the content of a small ALZ deployment files.

## Application usage steps

1. Validate requirements.
1. Clone this repository to your local environment.
1. Create an .env file in the root repository.
    1. Add the following variables:
        1. OPENAI_API_KEY="replace-with-Azure-OpenAI-Endpoint"
        1. OPENAI_API_VERSION="2023-05-15"
        1. AZURE_OPENAI_ENDPOINT="replace-with-Azure-OpenAI-Key"
        1. AZURE_DEPLOYMENT_NAME="replace-with-azure-openai-model-deployment-name"
1. Run the application
    1. python app.py
1. Paste the GitHub repository (A GitHub repository with the content of a small ALZ deployment files)
    1. Example:

```markdown
https://github.com/pradorodriguez/terraform-azurerm-avm-res-resources-resourcegroups/blob/main/README.md
```

1. Submit a prompt (instruction to Azure OpenAI).
1. When finished, type:

```markdown
exit()
```
