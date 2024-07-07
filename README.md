# Azure Filestore Project

## Summary

This is web application where users can securely upload & download files to and from Azure Blob Storage. Once uploaded, they can generates a unique, time-limited link for sharing of the file.

## Components

**Terraform**

This was used as an Iac solution to create all the required resources within Azure. It also allows the code to be hosted in a public repository without revealing any sensitive information as most of the values are randomly generated. 

**Azure**

- An Azure Blob Storage account with a single container is used to store the uploaded files. A lifecycle policy deletes all uploaded files within 2 days to ensure costs are kept low.

- The Blob Storage primary access key is stored securely in Azure Key Vault and retrieved by a server principal associated with my app.

- A Linux Web App with Python installed is used to host the website.Dependancies are stored in the requirements.txt file and are installed when the Web App executes. All required secrets are stored within the application settings which allows them to be set during runtime as environmental variables. The code used for the website is pulled via my public github repository. Additionally, A free tier SKU is used to not incur costs.  

- A Log Analytics Workspace is created for monitoring of the Blob Storage. It stores the logs of the main container that track file uploads & downloads, which can then be queried using KQL in Azure Monitor.

**Django & Python**

- The framework used to create the website is Django which allows for development of both the Frontend, Backend & Database.

- The Azure SDK for Python facilitates the file upload & download process directly to and from Blob Storage, and creation of SASs for the specificied file that last 1 day.

- A file model, which maps to the database, is used to store information about the each uploaded file including the url, the associated user, the extension, the name, and the size of the file.

- A storage quota of 100MB is assigned to each user to keep costs down.

**Bootstrap,CSS & HTML**

To create the user interface I used Bootstrap & CSS to make the website look presentable and Django HTML Templates to speed up the development process.