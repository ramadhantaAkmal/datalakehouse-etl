# prompt_builder.py

def format_context(documents):
    formatted = []

    for i, doc in enumerate(documents, 1):
        formatted.append(f"""
        Job {i}
        Title: {doc.metadata.get("title", "")}
        Company: {doc.metadata.get("company", "")}
        Location: {doc.metadata.get("location", "")}
        URL: {doc.metadata.get("job_url", "")}

        Description:
        {doc.page_content}
        """)

    return "\n\n".join(formatted)


def build_prompt(cv_text, formatted_context):
    return f"""
    You are a professional job-matching assistant.

    TASK:
    Rank the top 3 most relevant jobs for the candidate CV.

    CRITERIA:
    - Skill match
    - Tools match
    - Responsibilities overlap
    - Seniority alignment

    CONTEXT:
    {formatted_context}

    CANDIDATE CV:
    {cv_text}

    OUTPUT FORMAT:
    1. Job Title - Company
    URL:
    Why match (2-3 sentences)

    2. ...
    3. ...
    Limit to 1500 characters.
    """