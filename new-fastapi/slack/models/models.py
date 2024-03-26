from pydantic import BaseModel

class Note(BaseModel):
    id: int
    subject: str
    description: str