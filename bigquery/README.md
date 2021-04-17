### 1. LOCAL DEV ONLY

NOTE: execute commands from datalogger folder

#### 1.1 Create service account for datalogger database

```
gcloud iam service-accounts create datalogger-db
gcloud projects add-iam-policy-binding environment-data --member="serviceAccount:datalogger-db@environment-data.iam.gserviceaccount.com" --role="roles/bigquery.admin"
gcloud iam service-accounts keys create serviceaccount-datalogger-db.json --iam-account=datalogger-db@environment-data.iam.gserviceaccount.com
```

#### 1.2 Set env variable for subsequent commands

```
export GOOGLE_APPLICATION_CREDENTIALS="serviceaccount-datalogger-db.json"
```

### 2. Set up BigQuery

#### 2.1 Create dataset (one dataset per farm)

```
bq --location=EU mk --dataset --description "Environment data from all devices at Farm One" environment-data:farm_one
```

#### 2.2 Create table (one for each Raspberry Pi)

```
bq mk --table --schema "functions/schemas/T_H.json" --time_partitioning_field timestamp \
--description "Temp & Humidity table for farm-one-rb-0001" environment-data:farm_one.rpi_0001
```
