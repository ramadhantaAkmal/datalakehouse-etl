from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
from scraper.linkedin import LinkedIn
from scraper.model import Location, JobResponse
from scraper.model import  ScraperInput
from scraper.util import (
    set_logger_level,
    create_logger,
    get_enum_from_value,
    desired_order,
)

def scrape_jobs(
    search_term: str | None = None,
    location: str | None = None,
    distance: int | None = 50,
    is_remote: bool = False,
    job_type: str | None = None,
    easy_apply: bool | None = None,
    results_wanted: int = 15,
    proxies: list[str] | str | None = None,
    ca_cert: str | None = None,
    description_format: str = "markdown",
    linkedin_fetch_description: bool | None = False,
    linkedin_company_ids: list[int] | None = None,
    offset: int | None = 0,
    hours_old: int = None,
    verbose: int = 0,
    user_agent: str = None,
    **kwargs,
) -> pd.DataFrame:
    """
    Scrapes job data from job boards concurrently
    :return: Pandas DataFrame containing job data
    """
    set_logger_level(verbose)
    job_type = get_enum_from_value(job_type) if job_type else None

    scraper_input = ScraperInput(
        search_term=search_term,
        location=location,
        distance=distance,
        is_remote=is_remote,
        job_type=job_type,
        easy_apply=easy_apply,
        description_format=description_format,
        linkedin_fetch_description=linkedin_fetch_description,
        results_wanted=results_wanted,
        linkedin_company_ids=linkedin_company_ids,
        offset=offset,
        hours_old=hours_old,
    )

    def scrape_site() -> JobResponse:
        scraper_class = LinkedIn
        scraper = scraper_class(proxies=proxies, ca_cert=ca_cert)
        scraped_data: JobResponse = scraper.scrape(scraper_input)
        site_name = "LinkedIn" 
        create_logger(site_name).info(f"finished scraping")
        return scraped_data


    def worker():
        scraped_info = scrape_site()
        return scraped_info

    with ThreadPoolExecutor() as executor:
        future_to_site = {
            executor.submit(worker)
        }

        for future in as_completed(future_to_site):
            scraped_data = future.result()

    jobs_dfs: list[pd.DataFrame] = []

    
    for job in scraped_data.jobs:
        job_data = job.model_dump() 
        job_data["job_type"] = (
            ", ".join(job_type.value[0] for job_type in job_data["job_type"])
            if job_data["job_type"]
            else None
        )
        if job_data["location"]:
            job_data["location"] = Location(
                **job_data["location"]
            ).display_location()

        job_df = pd.DataFrame([job_data])
        jobs_dfs.append(job_df)
   
    
    if jobs_dfs:
        # Step 1: Filter out all-NA columns from each DataFrame before concatenation
        filtered_dfs = [df.dropna(axis=1, how="all") for df in jobs_dfs]

        # Step 2: Concatenate the filtered DataFrames
        jobs_df = pd.concat(filtered_dfs, ignore_index=True)

        # Step 3: Ensure all desired columns are present, adding missing ones as empty
        for column in desired_order:
            if column not in jobs_df.columns:
                jobs_df[column] = None  # Add missing columns as empty

        # Reorder the DataFrame according to the desired order
        jobs_df = jobs_df[desired_order]

        # Step 4: Sort the DataFrame as required
        return jobs_df.sort_values(
            by=["date_posted"], ascending=[False]
        ).reset_index(drop=True)
    else:
        return pd.DataFrame()