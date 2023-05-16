import os
import logging
from typing import List

import openai

from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from service.models import Leads
from service.models import Base
from service.dto import LeadOut
from dotenv import load_dotenv

load_dotenv()

# initialize logger
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

SQLALCHEMY_DATABASE_URL = "sqlite:///db/turiyatree.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db() -> Session:
    """Creates a new database session and returns it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/leads", response_model=List[LeadOut])
def read_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Returns a list of all leads in the database.

    :param skip: The number of leads to skip.
    :param limit: The maximum number of leads to return.
    :param db: The database session.

    :returns: A list of LeadOut objects representing the leads.
    """
    leads = db.query(Leads).offset(skip).limit(limit).all()
    if not leads:
        return []
    return [
        LeadOut(
            company=lead.company,
            first_name=lead.first_name,
            last_name=lead.last_name,
            full_name=lead.full_name,
            title=lead.title,
            email=lead.email,
            phone=lead.phone,
            fax=lead.fax,
            mobile=lead.mobile,
            website=lead.website,
            lead_source=lead.lead_source,
            lead_status=lead.lead_status,
        )
        for lead in leads
    ]


@app.get("/leads/{lead_id}", response_model=LeadOut)
def read_lead(lead_id: str, db: Session = Depends(get_db)):
    """
    Returns the lead with the specified record ID.

    :param lead_id: The record ID of the lead to return.
    :param db: The database session.

    :returns: A LeadOut object representing the lead.
    """
    lead = db.query(Leads).filter(Leads.record_id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return LeadOut(
        company=lead.company,
        first_name=lead.first_name,
        last_name=lead.last_name,
        full_name=lead.full_name,
        title=lead.title,
        email=lead.email,
        phone=lead.phone,
        fax=lead.fax,
        mobile=lead.mobile,
        website=lead.website,
        lead_source=lead.lead_source,
        lead_status=lead.lead_status,
    )


@app.get("/search_leads", response_model=List[LeadOut])
def search_leads(search_type: str, search_query: str, db: Session = Depends(get_db)):
    """
    Searches the database for leads that match the specified search query.

    :param search_type: The type of search to perform (name, company, or email).
    :param search_query: The query string to search for.
    :param db: The database session.

    :returns: A list of LeadOut objects representing the matching leads.
    """
    if search_type not in ["name", "company", "email"]:
        raise HTTPException(status_code=400, detail="Invalid search type")

    leads = []
    if search_type == "name":
        leads = db.query(Leads).filter(Leads.full_name == search_query).all()
    elif search_type == "company":
        leads = db.query(Leads).filter(Leads.company == search_query).all()
    elif search_type == "email":
        leads = db.query(Leads).filter(Leads.email == search_query).all()

    # If exact match not found, try wildcard search
    if not leads:
        if search_type == "name":
            leads = (
                db.query(Leads)
                .filter(Leads.first_name.ilike(f"%{search_query}%"))
                .all()
            )
        elif search_type == "company":
            leads = (
                db.query(Leads).filter(Leads.company.ilike(f"%{search_query}%")).all()
            )
        elif search_type == "email":
            leads = db.query(Leads).filter(Leads.email.ilike(f"%{search_query}%")).all()

    if not leads:
        return []

    return [
        LeadOut(
            company=lead.company,
            first_name=lead.first_name,
            last_name=lead.last_name,
            full_name=lead.full_name,
            title=lead.title,
            email=lead.email,
            phone=lead.phone,
            fax=lead.fax,
            mobile=lead.mobile,
            website=lead.website,
            lead_source=lead.lead_source,
            lead_status=lead.lead_status,
        )
        for lead in leads
    ]


@app.post("/check_action")
async def check_action(query: str):
    """
    Use OpenAI's GPT-3 language model to classify whether the given query is asking to read or write something.
    :param query: str - The query to classify.
    :return: A JSON object indicating whether the query is asking to read or write something.
    """
    openai.api_key = "YOUR_API_KEY"
    # Create a prompt for the OpenAI API to classify the query
    prompt = f"Is the following sentence asking to read, write or update something?\n\n{query}\n\nResponse:"

    # Use OpenAI's GPT-3 language model to classify the query
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the response from the OpenAI API and convert it to lowercase
    action = response.choices[0].text.strip().lower()

    # Return a JSON response indicating the action detected by the OpenAI API
    return {"action": action}
