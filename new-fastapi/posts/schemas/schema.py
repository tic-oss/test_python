from pydantic import BaseModel


class NoteBase(BaseModel):
    subject: str
    description: str

    class Config:
        orm_mode = True


class CreateNote(NoteBase):
    class Config:
        orm_mode = True