from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import List
from pydantic import BaseModel, Field

class JobExtraction(BaseModel):
    """A model to hold structured information about a job description."""
    index: int = Field(description="index of a record")

    qualifications: List[str] = Field(
        min_items=1,
        description="explicit qualifications stated in the text only"
    )

    benefits: List[str] = Field(
        default_factory=list,
        description="benefits explicitly mentioned in the text"
    )

    responsibilities: List[str] = Field(
        min_items=1,
        description="responsibilities explicitly mentioned in the text only"
    )

    tools_requirement: List[str] = Field(
        default_factory=list,
        description="tools explicitly mentioned in the text only"
    )
    years_of_experience: str = Field(
        description="number of years experience"
    )

def job_desc_extractor(data):
    model = OllamaLLM(model="ministral-3")
    template = """
        You are an information extraction system.

        Rules:
        - Extract ONLY description explicitly stated in the text
        - Do NOT infer, guess, or assume
        - If a field is not mentioned, return an empty list
        - Return valid JSON only
        - Do NOT add explanations
        {json_data}

        {format_instructions}
    """
    
    parser = JsonOutputParser(pydantic_object=JobExtraction)
    
    prompt = PromptTemplate(template = template, 
                            input_variables=["json_data"],
                            partial_variables={
                                    "format_instructions": parser.get_format_instructions()
                                }
                            )
    chain = prompt | model | parser
    json_data = str(data)

    result=chain.invoke({"json_data":{json_data}})

    return result