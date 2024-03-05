from pydantic import BaseModel
from typing import List, Optional

class AddressModel(BaseModel):
    country: Optional[str] = None
    country_iso: Optional[str] = None

class BuyerModel(BaseModel):
    email: str
    name: str
    checkout_phone: Optional[str] = None
    address: Optional[AddressModel] = None

class CommissionModel(BaseModel):
    value: Optional[float] = None
    source: Optional[str] = None
    currency_value: Optional[str] = None

class FullPriceModel(BaseModel):
    value: Optional[float] = None
    currency_value: Optional[str] = None

class PriceModel(BaseModel):
    value: Optional[float] = None
    currency_value: Optional[str] = None

class CheckoutCountryModel(BaseModel):
    name: Optional[str] = None
    iso: Optional[str] = None

class OrderBumpModel(BaseModel):
    is_order_bump: Optional[bool] = None
    parent_purchase_transaction: Optional[str] = None

class OriginalOfferPriceModel(BaseModel):
    value: Optional[float] = None
    currency_value: Optional[str] = None

class PaymentModel(BaseModel):
    installments_number: Optional[int] = None
    type: Optional[str] = None

class OfferModel(BaseModel):
    code: Optional[str] = None

class PlanModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class SubscriberModel(BaseModel):
    code: Optional[str] = None

class ProductModel(BaseModel):
    id: Optional[int] = None
    ucode: Optional[str] = None
    name: Optional[str] = None
    has_co_production: Optional[bool] = None

class AffiliateModel(BaseModel):
    affiliate_code: Optional[str] = None
    name: Optional[str] = None

class ProducerModel(BaseModel):
    name: Optional[str] = None

class SubscriptionModel(BaseModel):
    status: Optional[str] = None
    plan: Optional[PlanModel] = None
    subscriber: Optional[SubscriberModel] = None

class PurchaseModel(BaseModel):
    approved_date: Optional[int] = None
    full_price: Optional[FullPriceModel] = None
    price: Optional[PriceModel] = None
    checkout_country: Optional[CheckoutCountryModel] = None
    order_bump: Optional[OrderBumpModel] = None
    original_offer_price: Optional[OriginalOfferPriceModel] = None
    order_date: Optional[int] = None
    status: Optional[str] = None
    transaction: Optional[str] = None
    payment: Optional[PaymentModel] = None
    offer: Optional[OfferModel] = None
    sckPaymentLink: Optional[str] = None

class DataModel(BaseModel):
    product: Optional[ProductModel] = None
    affiliates: Optional[List[AffiliateModel]] = None
    buyer: BuyerModel
    producer: Optional[ProducerModel] = None
    commissions: Optional[List[CommissionModel]] = None
    purchase: Optional[PurchaseModel] = None
    subscription: Optional[SubscriptionModel] = None

class HotmartModel(BaseModel):
    id: Optional[str] = None
    creation_date: Optional[int] = None
    event: Optional[str] = None
    version: Optional[str] = None
    data: DataModel
    hottok: str
