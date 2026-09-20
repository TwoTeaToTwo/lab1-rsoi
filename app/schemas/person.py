from pydantic import BaseModel, ConfigDict, Field


class PersonCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    age: int | None = Field(default=None, ge=0)
    address: str | None = Field(default=None, max_length=500)
    work: str | None = Field(default=None, max_length=255)


class PersonUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    age: int | None = Field(default=None, ge=0)
    address: str | None = Field(default=None, max_length=500)
    work: str | None = Field(default=None, max_length=255)


class PersonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int | None = None
    address: str | None = None
    work: str | None = None

