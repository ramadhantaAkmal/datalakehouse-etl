import pyarrow as pa
from pyiceberg.schema import Schema
from pyiceberg.types import (
    NestedField, StringType, IntegerType, ListType, DateType
)  
from pyiceberg.partitioning import PartitionSpec, PartitionField

def create_table(catalog):
    table_id = ("job_results", "jobs_results_bronze")
    tables = catalog.list_tables("job_results")
    
    if table_id in tables:
        print("Bronze table already exists!")
    else:
        schema = Schema(
            NestedField(field_id=1, name="title", field_type=StringType(), required=False),
            NestedField(field_id=2, name="company_name", field_type=StringType(), required=False),
            NestedField(field_id=3, name="location", field_type=StringType(), required=False),
            NestedField(field_id=4, name="description", field_type=StringType(), required=False),
            NestedField(field_id=6, name="schedule_type", field_type=StringType(), required=False),
            NestedField(field_id=7, name="qualifications", field_type=ListType(element_id=101, element_type=StringType(), element_required=False), required=False),
            NestedField(field_id=8, name="benefits", field_type=ListType(element_id=102, element_type=StringType(), element_required=False), required=False),
            NestedField(field_id=9, name="responsibilities", field_type=ListType(element_id=103, element_type=StringType(), element_required=False), required=False),
            NestedField(field_id=10, name="tools_requirement", field_type=ListType(element_id=104, element_type=StringType(), element_required=False), required=False),
            NestedField(field_id=11, name="years_of_experience", field_type=StringType(), required=False),  # or IntegerType if numeric
            NestedField(field_id=12, name="ingestion_date", field_type=DateType(), required=False)  # for partitioning
        )

        partition_spec = PartitionSpec(
            PartitionField(
                source_id=12,              # field_id of ingestion_date
                field_id=1000,             # unique partition field id
                transform="identity",
                name="ingestion_date"
            )
        )
    
        # Partition by 'date' for dated files
        catalog.create_table(
            identifier=("job_results", "jobs_results_bronze"), 
            schema=schema,
            partition_spec=partition_spec  # or 'day(date)' for daily
        )

        print("Iceberg bronze table created!")