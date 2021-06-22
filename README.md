# exchange-rates

Prerequisites:
- Add the infra/auth directory and insert the file credentials.json
- In Google Cloud Storage add the bucket 'yca_datawarehouse'
- In Google Cloud Storage, for the bucket previously created give permissions for GCS usage to client_email in credentials file 

Execute project:
- cd infra
- docker-compose up

For the Data modeling test :
- The diagrams are in directory : ./modeling
- The database can be accesed in the postgres database with localhost:5432 (schemas : operations and analysis)

For the Technical test :
- Airflow can be accesed in localhost:8081
- Python scripts in the mounted directory infra/scripts
