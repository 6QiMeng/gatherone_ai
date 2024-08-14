from pydantic import BaseModel, Field


class TextToImageSchema(BaseModel):
    """
    文生图
    """
    desc: str = Field(...)
    style: str = Field(...)
    size: str = Field(...)
