import polars as pl
import json
import requests
from aiagent.data_extract_agent import job_desc_extractor

def extract_data(df1: pl.DataFrame):
    df1 = df1.with_row_index(name="index",offset=1)
    json_object = json.loads(df1.write_json())
    response = job_desc_extractor(json_object)
    # response = requests.post('http://n8n:5678/webhook/b41fb2f1-e65f-4b02-9e32-3629214ca314', json=json_object)
    
    df2 = pl.DataFrame(response)
    df_merged = df1.join(df2, on="index")
    
    df_merged.drop_in_place('index')
    return df_merged