from pydantic import BaseModel
class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

class IssueAddRequest(BaseModel):
    title: str
    description: str
    assignee_id: str
    fixer_id: str

class AssgineeSearchRequest(BaseModel):
    title: str
    description: str
