from minio import Minio
import json
import datetime

def fetch_json_file():
    current_date = datetime.date.today()

    # Initialize client
    client = Minio(
        "localhost:9000",
        access_key="admin",
        secret_key="password",
        secure=False  
    )

    bucket_name = "jobs-result-json"
    object_name = f"jobs-result-{current_date}.json"

    # Get object from MinIO
    response = client.get_object(bucket_name, object_name)

    try:
        # Read and decode bytes
        data = response.read().decode("utf-8")
        
        # Convert JSON string → Python dict
        json_dict = json.loads(data)

        return json_dict
    finally:
        response.close()
        response.release_conn()