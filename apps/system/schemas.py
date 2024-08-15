from pydantic.v1 import Field, BaseModel


class UserRegeisterSchema(BaseModel):
    username: str = Field(..., min_length=1, max_length=20)
    mobile: str = Field(..., regex=r'^1[3-9]{1}[\d]{9}$')
    password: str = Field(..., min_length=4, max_length=16)
