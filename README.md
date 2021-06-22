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
- Python scripts are in the mounted directory infra/scripts

For tables in bigquery:

- you have to create a dataset,
- you have to create the external tables :

|| raw_dim_currency | fact_exchange_rate_history |
| ------ | ------ | ------ |
|Data|yca_datalake/*_ dim_currency.csv|cur_code: string, one_euro_value: float, updated_date: date, serial_code: string|
|Schema|yca_datalake/*_fact_exchange_rate_history.csv|history_date:date,from_cur_code:string,to_cur_code:string,exchange_rate:float|


Create the following query and save it as the view 'dim_currency' :
(Note: you have to change the name of the project and the dataset in the query) 

```sql
SELECT raw.cur_code, raw.one_euro_value, raw.updated_date AS last_updated_date, raw.serial_code
FROM `corded-keel-317515.yourdataset.raw_dim_currency` AS raw
JOIN (
     SELECT DISTINCT cur_code, MAX (updated_date) AS last_updated_date
     FROM `corded-keel-317515.yourdataset.raw_dim_currency`
     GROUP BY cur_code
) as max_dates ON raw.cur_code = max_dates.cur_code AND raw.updated_date = max_dates.last_updated_date
```

