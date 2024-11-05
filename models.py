from typing import Optional
from pydantic import BaseModel, Field

class Artist(BaseModel):
    id: str = Field(default=None, alias="_key")
    last_name: str = Field(...)
    first_name: str = Field(...)
    birth_date: Optional[str]
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_key": "artist_6",
                "last_name": "Cameron",
                "first_name": "James",
                "birth_date": "1954"
            }
        }

class ArtistUpdate(BaseModel):
    last_name: Optional[str]
    first_name: Optional[str]
    birth_date: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "last_name": "Cameron",
                "first_name": "James",
                "birth_date": "1954"
            }
        }