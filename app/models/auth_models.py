from pydantic import BaseModel
from typing import List, Optional, Dict

class TrackingModel(BaseModel):
    name: str
    type: str
    publisher: Optional[str] = None
    tracked_at: str

class LeadModel(BaseModel):
    first_tracking: TrackingModel
    last_tracking: TrackingModel

class ContactModel(BaseModel):
    id: str
    name: str
    email: str
    doc: str
    phone_number: str
    phone_local_code: str
    address: str
    address_number: str
    address_comp: Optional[str] = None
    address_district: str
    address_city: str
    address_state: str
    address_country: str
    address_zip_code: str
    lead: Optional[LeadModel] = []

class DatesModel(BaseModel):
    ordered_at: str
    confirmed_at: str
    expires_at: Optional[str] = None
    canceled_at: Optional[str] = None
    warranty_until: str
    unavailable_until: str

class TaxModel(BaseModel):
    value: float
    rate: float

class InstallmentsModel(BaseModel):
    value: Optional[str] = None
    qty: int
    interest: float

class BilletModel(BaseModel):
    line: Optional[str] = None
    url: Optional[str] = None
    expiration_date: Optional[str] = None

class CreditCardModel(BaseModel):
    first_digits: str
    last_digits: str
    brand: str
    id: str

class PaymentModel(BaseModel):
    method: Optional[str] = None
    marketplace_id: str
    marketplace_name: str
    marketplace_value: float
    discount_value: float
    currency: str
    total: float
    affiliate_value: float
    net: float
    gross: float
    tax: TaxModel
    installments: InstallmentsModel
    refuse_reason: Optional[str] = None
    billet: BilletModel
    credit_card: CreditCardModel

class ProducerModel(BaseModel):
    marketplace_id: str
    name: str
    contact_email: Optional[str] = None

class ProductModel(BaseModel):
    id: str
    internal_id: str
    name: str
    unit_value: float
    image_url: Optional[str] = None
    total_value: float
    type: str
    marketplace_name: str
    marketplace_id: str
    qty: int
    producer: ProducerModel

class ShipmentModel(BaseModel):
    value: float
    carrier: str
    service: str
    tracking: str
    delivery_time: int
    status: List[str]

class ShippingModel(BaseModel):
    name: str
    value: float

class SourceModel(BaseModel):
    source: Optional[str] = None
    checkout_source: Optional[str] = None
    utm_source: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None
    pptc: List[str]

class SubscriptionModel(BaseModel):
    id: str
    name: str
    last_status: str
    charged_times: int
    charged_every_days: int
    started_at: str
    last_status_at: str
    canceled_at: Optional[str] = None
    trial_started_at: Optional[str] = None
    trial_finished_at: Optional[str] = None

class InvoiceModel(BaseModel):
    id: str
    period_start: str
    period_end: str
    charge_at: str
    status: str
    type: str
    cycle: int
    value: float
    tax_value: float
    increment_value: float
    discount_value: float
    created_at: str

class GuruModel(BaseModel):
    api_token: str
    contact: ContactModel
    
