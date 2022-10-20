from doctest import Example
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
from fastapi import FastAPI, status
from fastapi import Body, Query, Path, Form

app = FastAPI()

class HairColorEnum(Enum):
    white = "white"
    black = "black"
    yellow = "yellow"
    red = "red"


class PersonBase(BaseModel):
    first_name: str = Field(..., min_length = 1)
    last_name: str = Field(..., min_length = 1)
    age: int = Field(..., gt = 0)
    hair_color: Optional[HairColorEnum] = Field(default=None) 
    is_married: Optional[bool] = Field(default = None)
    
    # yes saul inside of a class
    # prefill example for swagger
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "saul",
    #             "last_name": "burgos",
    #             "age": 40,
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }


class Person(PersonBase):
    password: str = Field(..., min_length = 8)

class PersonResponse(PersonBase):
    pass
     

class Location(BaseModel):
    lat: float
    lng: float
    country: str


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, Example="saulburgos") 
    message: str = Field(...)

@app.get(
    "/", 
    status_code = status.HTTP_200_OK
)
def home():
    return {
        "hello": "world"
    }

@app.post(
    "/person/new", 
    response_model=PersonResponse,
    status_code=status.HTTP_201_CREATED
)
def create_person(person: Person = Body(...)):
    return person

# Query parameters
@app.get(
    "/person/details", 
    status_code=status.HTTP_200_OK
)
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length = 1,
        max_length = 50,
        title = "Person name",
        description = "cosa cosa cosa"
    ),
    age: int = Query(...),
):
    return {
        "name": age
    }

# path parameters
@app.get(
    "/person/details/{person_id}",
    status_code=status.HTTP_200_OK
)
def show_person(
    person_id: int = Path(..., gt = 0)
):
    return {
        "person_id": person_id
    }


# receiving 2 bodies
@app.put(
    "/person/{person_id}/",
    status_code=status.HTTP_201_CREATED
)
def update_person(
    person_id: int = Path(..., gt = 0),
    person: Person = Body(...),
    #location: Location = Body(...)
):
    results = person.dict()
    #results.update(location.dict())
    return results

#working with form
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(
    username: str = Form(...), 
    password: str = Form(...)
):
    return LoginOut(username=username, message="logout successfuly")