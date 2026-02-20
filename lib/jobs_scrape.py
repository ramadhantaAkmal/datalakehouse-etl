import polars as pl
from scraper import scrape_jobs

#Ingest data
def ingest():
    print("Start scrape")
    jobs = scrape_jobs(
            search_term="data engineer",
            location="Jakarta",
            results_wanted=20,
            hours_old=120,
            linkedin_fetch_description=True
        )
    
    df = pl.from_pandas(jobs)
    df = df["title","company_name","location","description","job_type","job_url"]
    print("Finished scrape")
