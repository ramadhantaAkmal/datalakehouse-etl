import polars as pl
import json
from aiagent.data_extract_agent import job_desc_extractor

def extract_data(df1: pl.DataFrame):
    df1 = df1.with_row_index(name="index",offset=1)
    json_object = json.loads(df1.write_json())
    response = job_desc_extractor(json_object)
    
    df2 = pl.DataFrame(response)
    df_merged = df1.join(df2, on="index")
    
    df_merged.drop_in_place('index')
    return df_merged