import polars as pl
import datetime
from jobs_scrape import ingest
from utils.api_util import extract_data
from config.s3config import storage_options
from store_json import store_json
from iceberg.iceberg_append import transform_load_brz
from iceberg.iceberg_transform import transform_load_slv_gld

def main():
    current_date = datetime.date.today()
    
    #Extraction
    print("Extracting data...")
    df = ingest()
    df = df.rename({"job_type": "schedule_type"})
    df = extract_data(df)
    df = df.with_columns(pl.lit(current_date).alias("ingestion_date"))
    print("Data Extracted successfully")
    print(df.columns)
    json_string = df.write_json(file=None)
    store_json(json_string)
    
    df.drop_in_place('job_url')
     
    df.write_parquet(
        "s3://jobs-results-lake/",
        storage_options=storage_options,
        compression="zstd",
        partition_by="ingestion_date"
    )
    print("Raw data archived successfully")
     
    #Transform and Load
    transform_load_brz(df)
    transform_load_slv_gld(df)
    print("Data transformed and loaded on iceberg successfully")

main()