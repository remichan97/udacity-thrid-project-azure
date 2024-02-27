import os
from sqlalchemy import URL
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app_dir = os.path.abspath(os.path.dirname(__file__))
vaulturl='https://techconf-vaults.vault.azure.net/'
credential = DefaultAzureCredential()
client = SecretClient(vault_url=vaulturl, credential=credential)

class BaseConfig:
    DEBUG = True
    POSTGRES_URL=client.get_secret('db-url').value
    POSTGRES_USER=client.get_secret('db-username').value
    POSTGRES_PW=client.get_secret('db-password').value
    POSTGRES_DB=client.get_secret('db-dbname').value
    # DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    # Things breaks horribly if the database password contains special characters, as such, using the URL.create from sqlalchemy to build
    # connection url
    DB_URL = URL.create(
        drivername='postgresql',
        username=POSTGRES_USER,
        password=POSTGRES_PW,
        host=POSTGRES_URL,
        database=POSTGRES_DB,
        port=5432,
        query={
            'sslmode': 'require'
        }
    )
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://techconf.servicebus.windows.net/;SharedAccessKeyName=read-write;SharedAccessKey=CKccH5QuPwD6K0/VRQgI77LDYgOsV4SQu+ASbAYfiqc=;EntityPath=notificationqueue'
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'info@techconf.com'
    SENDGRID_API_KEY = '' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False