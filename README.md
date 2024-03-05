# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *Azure Cosmos DB PostgreSQL cluster* |Single node, 2 vCore, 8GB RAM, 256GB Storage, with High Availability enabled| $380.76/month|
| *Azure Service Bus*   | Premium | $668.00/month |
| *Azure Function App*   | Consumption | approximately $0.20/month (assuming execution count exceeded free quota, and executed another 1 million time each month) |
| *Azure Storage Account*   | Consumption | approximately $0.02 per month |
| *Azure Web App*    | Premium P1V3 | same as the app service plan |
| *Azure App Service Plan*    | Premium P1V3 | approximately $113.15/ month |
| *Azure Key Vault*  | Standard | approximately $0.30 per month (assuming 100,000 query per month) |
| *SendGrid SaaS*     | Free 100 | approximately $3.99 per month (assuming exceeded 100 free mail and sending 100 mails per day) |

Additional notes:  
Database: On Production, High Availability is always prefered as they provide yet another safety net should a database node is down for any reason  
Service Bus pricing: Premium tier is recommended for Production usage, however, if being in budget constraint, we can consider the Standard tier, as they are billed on each 13 Million operations, the service tier can still be adjusted according to the usage when needed  
Function App: Function App provide ability to resue the App Serivce using for Web App when needed (for instance, keeping both the web and the function app on the same geolocation). This can be considered before going for the Premium plan, which set back around $437.78/ month for the EP1 configuation with additional 2 scale out instances. Consumption plan can also be considered as the choice should the budget is tight  
Azure Key Vault: Both Standard, and Premium rate for secret queries are the same ($0.03 per 10,000 transaction per month)


## Architecture Explanation
Following are my explanation for my current deployments, and my reasoning behind the choice: 
 - **Azure Web App**: The project front-end were deployed using the Free tier App Service plan. Web App service was used instead of using VMs as they are much simpler to configure, and can also be scaled easily when needed
 - **Azure Function App**: Comparing the standard App Service plans, the Consumption plan were selected as the plan provide a free quota of 1 million executions and execution time of 400,000 GB-s for each month. As the current application state, the total execution number should not exceed the free quota for the plan
 - **Azure Service Bus**: This is used to receive notification ID to which then forwarded to the function app to work its magic. This is billed on operations, as such, the pricing should be minimum
 - **Azure Cosmos DB PostgreSQL cluster**: Using CosmosDb as the database hosting of choice helps us scale easily, it also provide the ability to isolate tenants into their own nodes should the needs in the future
 - **Azure Key Vault**: Key vault is used to store the app configuration data (such as database credentials, access URL, and various other credentials), these data should not be accesses much, as such, the Standard tier, which price per 10,000 transaction should cover us here.
 - **Azure Storage Account**: This is needed to host the Web App instance, since the data stored by the app is not much, the pricing per month should be minimum
 - **SendGrid SaaS**: This is used to provide the ability to send emails to the client. The current service tier provide a free 100 email sent per day. Due to the current application demands, this should be plenty for us.
