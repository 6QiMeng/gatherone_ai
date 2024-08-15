from pydantic import BaseModel, Field


class TextToImageSchema(BaseModel):
    """
    文生图
    """
    desc: str = Field(..., max_length=1000)
    style: str = Field(...)
    ratio: str = Field(...)
