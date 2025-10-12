from fastapi import APIRouter, Query
from typing import List
from app.models import models

router = APIRouter()



# starter_data = [
#     {'name': "Nigeria", 'capital': 'Abuja'},
#     {'name': "USA", 'capital': 'Washington, D.C'}
# ]

# # Slimer version (i.e convert a model to a list obj)
# @router.get("/countries", response_model=List[models.Country])
# def get_countries():
#     return starter_data


sample_countries = models.Countries(countries=[
    models.Country(name="Nigeria", capital="Abuja"),
    models.Country(name="USA", capital="Washington, D.C."),
])

# GET endpoint
@router.get("/countries", response_model=models.Countries)
def get_countries():
    return sample_countries

@router.post("/country", response_model=models.Country)
def add_country(country: models.Country):
    # In a real app, we add this to a database
    sample_countries.countries.append(country)
    return country
