from pydantic import BaseModel


class SummaryModel(BaseModel):
    Title: str = ""
    Summary: str = ""
    Why_this_is_important: str = ""


class PromptTemplate(BaseModel):
    description: str = ""
    system_message: str = ""
    human_message: str = ""
