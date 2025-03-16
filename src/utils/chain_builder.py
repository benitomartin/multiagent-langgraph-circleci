from typing import List

from langchain.prompts import PromptTemplate
from pydantic import BaseModel


class ChainBuilder:
    def __init__(self, llm):
        self.llm = llm

    def build(self, prompt_template: str, input_vars: List[str], model: BaseModel):
        structured_llm = self.llm.with_structured_output(model)
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=input_vars
        )
        return prompt | structured_llm
