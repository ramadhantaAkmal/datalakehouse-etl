import polars as pl
from scraper import scrape_jobs

#Scrape data from linkedin
def ingest():
    print("Start scrape")
    jobs = scrape_jobs(
            search_term="data engineer",
            location="Jakarta",
            results_wanted=20,
            hours_old=120,
            linkedin_fetch_description=True
        )
    
    #filter unnecessary data & columns
    df = pl.from_pandas(jobs)
    df = df["title","company_name","location","description","job_type","job_url"]
    df = df.filter(pl.col("title").str.contains("Data Engineer"))
    print("Finished scrape")
    
    return df
