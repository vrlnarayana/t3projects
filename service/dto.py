from typing import Optional
from pydantic import BaseModel



class LeadCreate(BaseModel):
    name: str
    company: str
    email: str
    status: str = "contacted"


class LeadOut(BaseModel):
    company: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    title: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    fax: Optional[float]
    mobile: Optional[str]
    website: Optional[str]
    lead_source: Optional[str]
    lead_status: Optional[str]



class Leads(BaseModel):
    record_id: str
    lead_owner_id: Optional[str]
    company: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    title: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    fax: Optional[float]
    mobile: Optional[str]
    website: Optional[str]
    lead_source: Optional[str]
    lead_status: Optional[str]
    industry: Optional[str]
    no_of_employees: Optional[float]
    annual_revenue: Optional[float]
    rating: Optional[float]
    campaign_source_id: Optional[float]
    email_opt_out: Optional[int]
    skype_id: Optional[str]
    created_by_id: Optional[str]
    modified_by_id: Optional[str]
    created_time: Optional[str]
    modified_time: Optional[str]
    salutation: Optional[str]
    secondary_email: Optional[float]
    currency: Optional[float]
    exchange_rate: Optional[float]
    last_activity_time: Optional[str]
    twitter: Optional[str]
    layout_id: Optional[str]
    tag: Optional[float]
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[int]
    country: Optional[str]
    description: Optional[float]
    score: Optional[int]
    positive_score: Optional[int]
    negative_score: Optional[int]
    touch_point_score: Optional[int]
    positive_touch_point_score: Optional[int]
    negative_touch_point_score: Optional[int]
    lead_image: Optional[str]
    user_modified_time: Optional[str]
    system_related_activity_time: Optional[float]
    user_related_activity_time: Optional[str]
    system_modified_time: Optional[float]
    converted_date_time: Optional[float]
    record_approval_status: Optional[int]
    is_record_duplicate: Optional[int]
    lead_conversion_time: Optional[float]
    unsubscribed_mode: Optional[float]
    unsubscribed_time: Optional[float]
    converted_account_id: Optional[float]
    converted_contact_id: Optional[float]
    converted_deal_id: Optional[float]
    change_log_time: Optional[float]
    is_converted: Optional[int]
    locked: Optional[int]
    last_enriched_time: Optional[float]
    enrich_status: Optional[float]

    class Config:
        orm_mode = True