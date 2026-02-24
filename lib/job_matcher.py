from aiagent.job_matcher.pipeline import run_agent
from utils.fetch_json import fetch_json_file
from utils.discord_notifier import send_disc_message

# Main file to run the job matching pipeline
def run_job_matcher():
    #Fetch json file from s3 Minio
    jobs = fetch_json_file()

    #Input short version CV
    cv = """
                SUMMARY 
                Junior Data Engineer with practical experience designing ETL/ELT pipelines and transforming structured & 
                unstructured data using Python and SQL. Brings a software engineering background that strengthens data 
                reliability, version control, and maintainable pipeline design. Demonstrates strong analytical skills, curiosity, 
                and eagerness to learn modern data engineering tools and best practices. 
                    
                WORK EXPERIENCE 
                Sree International Indonesia – Mobile Developer                  
                Sep 2023 – Jun 2025  
                • Designed and maintained local relational data storage using SQLite, supporting offline-first application 
                behavior and reliable data access in low-connectivity environments. 
                • Integrated and processed data from third-party REST APIs, handling data parsing, validation, and 
                synchronization between remote services and local databases. 
                • Worked with structured data models and queries to ensure data consistency and integrity across 
                application states. 
                • Applied Git-based version control, clean code principles, and modular architecture to improve 
                maintainability and reduce technical debt.  
                UG FoodHub – Mobile Developer (Freelance)      
                Apr 2022 – Sep 2022  
                • Consumed and processed JSON-based API data, transforming responses into structured application 
                models for downstream usage. 
                • Collaborated in an agile team environment, participating in sprint planning and iterative delivery. 
                • Implemented reusable data-driven components, strengthening understanding of data flow, state 
                management, and application-level data handling. 
                    
                    
                Hard Skills : Data Governance, Data Modeling, Data Warehouse, Data Lakehouse, ETL & ELT 
                fundamentals,  Stream & Batch fundamentals, Databases. 
                Tools : Python( Polars, Pandas, PySpark), SQL(PostgreSQL, BigQuery), GCS, Minio, Iceberg, 
                Airflow, dbt, GCP, Linux, Shell Script, Git, Docker, etc. 
                Soft Skills  : Curious self-learner, analytical problem solver, adaptable, effective independently or in 
                teams.
                    
                pick top 3 jobs that are closest match with this CV above and give the url
                limit the response to only 1024 characters
            """

    # Run AI agent to match cv with the job list
    response = run_agent(cv,jobs)

    # Sending the result to discord sever
    send_disc_message(response)