from pydantic import BaseModel

class EmailContact(BaseModel):
    issue: str
    email: str
    cellphone: str
    full_name: str
    reason: str