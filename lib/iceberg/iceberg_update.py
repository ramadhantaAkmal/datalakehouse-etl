from update_table import silver,bronze
from iceberg_catalog import catalog_load

def update():
    catalog = catalog_load()
    
    silver.update_table(catalog)
    catalog.close()
    
update()