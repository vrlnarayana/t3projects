import uuid
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends

from .service import get_db
from .service import app
from dto import Leads
from dto import LeadCreate
from dto import LeadOut
from models import Lead
from fastapi import HTTPException


# @app.post("/leads", response_model=LeadOut)
# def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
#     db_lead = Lead(
#         id=uuid.uuid4().hex,
#         name=lead.name,
#         company=lead.company,
#         email=lead.email,
#         status=lead.status,
#     )
#     db.add(db_lead)
#     db.commit()
#     db.refresh(db_lead)
#     return LeadOut(
#         id=db_lead.id,
#         name=db_lead.name,
#         company=db_lead.company,
#         email=db_lead.email,
#         status=db_lead.status,
#     )


# @app.put("/leads/{lead_id}", response_model=LeadOut)
# def update_lead(lead_id: str, lead: LeadCreate, db: Session = Depends(get_db)):
#     db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
#     if not db_lead:
#         raise HTTPException(status_code=404, detail="Lead not found")
#     db_lead.name = lead.name
#     db_lead.company = lead.company
#     db_lead.email = lead.email
#     db_lead.status = lead.status
#     db.commit()
#     db.refresh(db_lead)
#     return LeadOut(
#         id=db_lead.id,
#         name=db_lead.name,
#         company=db_lead.company,
#         email=db_lead.email,
#         status=db_lead.status,
#     )



# @app.delete("/leads/{lead_id}")
# def delete_lead(lead_id: str, db: Session = Depends(get_db)):
#     db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
#     if not db_lead:
#         raise HTTPException(status_code=404, detail="Lead not found")
#     db.delete(db_lead)
#     db.commit()
#     return {"deleted": lead_id}
