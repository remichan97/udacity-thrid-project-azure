from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

vaulturl='https://techconf-vaults.vault.azure.net/'
credential = DefaultAzureCredential()
client = SecretClient(vault_url=vaulturl, credential=credential)

class FunctionConfig:
	POSTGRES_URL=client.get_secret('db-url').value
	POSTGRES_USER=client.get_secret('db-username').value
	POSTGRES_PW=client.get_secret('db-password').value
	POSTGRES_DB=client.get_secret('db-dbname').value
	TABLE_NAME='notification'