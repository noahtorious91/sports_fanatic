# sports_fanatic
This is an e-commerce website to generate data for batch and streaming archtecture development purchases. The intent is to have a light weight ecommerce website that could be deployed locally or serverlessly in the cloud for POC testing for differnt data engineering lifecycle architecture schemes.

Initially I will be developing to use this webapp to use with the following lakehouse system for local and cloud development via containers:

```text
Orchestration (Airflow)
        |
        ↓
Django <-> [PostgreSQL] --(Airbyte)--> [MinIO - Iceberg + Parquet]
                ↘                          ↓
                   Streaming (Kafka) → Data Warehouse (ClickHouse)
                                           ↓
                                       Transform (dbt for batch)
                                           ↓
                                       BI Tool (Superset)

```

The local resource usage of the docker containers will be as follows:

1) Django webserver - 2GB/ 1Core
2) Postgres DB for webserver 2GB/1 Core
3) Airbyte 2GB 1 Core
4) Airflow Webserver 2GB 1 Core
5) Airflow DB 2GB 1 Core
6) Kafka 2GB 1 Core
7) Superset 2GB 1 Core

Docker will use 14GBs and 7Cores if you are reading this and want to use this webserve in the future with this exact setup please make sure you have a M3 Max 32GB + rig. 

-----------------------------------------------------------------------------

## Current Roadmap:
- [x] home page products and cart logic
- [x] login feature
- [ ] product detail pages feature
- [x] account feature
- [x] invoices / orders feature
- [x] logout feature 
- [ ] product catalog tool 
- [ ] promo manager tool 
- [ ] returns tool 
- [ ] product tagging enhancement
- [ ] inventory management tool
- [ ] tag specific plps
- [ ] filters on plps
- [ ] reviews tool
