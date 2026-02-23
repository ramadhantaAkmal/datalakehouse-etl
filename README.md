# ETL Datalakehouse for scrape job vacancy data with AI agents

## Overview
An ETL pipeline for scraping job vacancy data from linkedin jobs section using Beautifulsoup , Minio as data lake, Apache Iceberg as table format, polars for transformation, docker as the environment, Airflow as the workflow scheduler, Trino for query engine and Superset for dashboard. This project also utilizing Langchain for making AI agents that can handle data extraction and also matching top 3 jobs from the processed data and send it to my own discord server. 

## Tools Used
- **JobSpy**        : API to get/ingest linkedin jobs data
- **Polars**        : Data processing and transformation, extract into json and parquet
- **Airflow**       : Pipeline orchestrator
- **LangChain**     : AI agents for extracting data and job matching
- **Ollama**        : Open source tools to run LLMs locally
- **Docker**        : Containerized airflow, ollama, minio, iceberg, trino and superset
- **Minio**         : Storing the extracted data
- **Iceberg**       : Create table format and Data transformation on Minio
- **Trino**         : Query engine to access Iceberg tables
- **Superset**      : Data exploration and visualization

## Architecture diagram

![Architecture diagram](./readme-assets/etl-datalakehouse-ai.png)

## Discord result

![discord job result](./readme-assets/discord-job-result.png)

## Superset example dashboard


![superset example dashboard](./readme-assets/superset-dashboard.png)
