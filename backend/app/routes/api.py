from fastapi import APIRouter, Query, Depends, HTTPException
from typing import List
from app.models import models
from app.db.schema import Call
from sqlalchemy.orm.session import Session 


from sqlalchemy.orm import Session
from app.db.database import get_db, SessionLocal


router = APIRouter()



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
    sample_countries.countries.append(country)
    return country


@router.post("/api/calls")
def receive_call_data(payload: models.CallData, db: Session = Depends(get_db)):
    print("TRANSCRIPT OBJECT:", payload.transcript_object)
    transcript_data = [item.model_dump(by_alias=True) for item in payload.transcript_object]
    try:
        
        new_call = Call(
            call_id=payload.call_id,
            agent_id=payload.agent_id,
            customer_name=payload.retell_llm_dynamic_variables.customer_name,
            start_timestamp=payload.start_timestamp,
            end_timestamp=payload.end_timestamp,
            duration_ms=payload.duration_ms,
            call_summary=payload.call_analysis.call_summary,
            overall_sentiment=payload.call_analysis.Overall_sentiment,
            transcript_object=transcript_data
        )

        db.add(new_call)
        db.commit()
        db.refresh(new_call)

        return {"status": "success", "call_id": new_call.call_id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))