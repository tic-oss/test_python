from pydantic import BaseModel


class PostBase(BaseModel):
     
    content: str
    title: str
    
    class ConfigDict:
        from_attributes = True



class CreatePost(PostBase):
    class ConfigDict:
        from_attributes = True


