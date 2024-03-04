from pydantic import BaseModel
from typing import List, Optional

class AuthModel(BaseModel):
    id: Optional[str]
    creation_date: Optional[int]
    event: Optional[str]
    version: Optional[str]
    data: Optional[dict]

class AddressModel(BaseModel):
    country: Optional[str]
    country_iso: Optional[str]

class BuyerModel(BaseModel):
    email: str
    name: str
    checkout_phone: Optional[str]
    address: Optional[AddressModel]

class CommissionModel(BaseModel):
    value: Optional[float]
    source: Optional[str]
    currency_value: Optional[str]

class FullPriceModel(BaseModel):
    value: Optional[float]
    currency_value: Optional[str]

class PriceModel(BaseModel):
    value: Optional[float]
    currency_value: Optional[str]

class CheckoutCountryModel(BaseModel):
    name: Optional[str]
    iso: Optional[str]

class OrderBumpModel(BaseModel):
    is_order_bump: Optional[bool]
    parent_purchase_transaction: Optional[str]

class OriginalOfferPriceModel(BaseModel):
    value: Optional[float]
    currency_value: Optional[str]

class PaymentModel(BaseModel):
    installments_number: Optional[int]
    type: Optional[str]

class OfferModel(BaseModel):
    code: Optional[str]

class PlanModel(BaseModel):
    id: Optional[int]
    name: Optional[str]

class SubscriberModel(BaseModel):
    code: Optional[str]

class ProductModel(BaseModel):
    id: Optional[int]
    ucode: Optional[str]
    name: Optional[str]
    has_co_production: Optional[bool]

class AffiliateModel(BaseModel):
    affiliate_code: Optional[str]
    name: Optional[str]

class ProducerModel(BaseModel):
    name: Optional[str]

class SubscriptionModel(BaseModel):
    status: Optional[str]
    plan: Optional[PlanModel]
    subscriber: Optional[SubscriberModel]

class PurchaseModel(BaseModel):
    approved_date: Optional[int]
    full_price: Optional[FullPriceModel]
    price: Optional[PriceModel]
    checkout_country: Optional[CheckoutCountryModel]
    order_bump: Optional[OrderBumpModel]
    original_offer_price: Optional[OriginalOfferPriceModel]
    order_date: Optional[int]
    status: Optional[str]
    transaction: Optional[str]
    payment: Optional[PaymentModel]
    offer: Optional[OfferModel]
    sckPaymentLink: Optional[str]

class DataModel(BaseModel):
    product: Optional[ProductModel]
    affiliates: Optional[List[AffiliateModel]]
    buyer: BuyerModel
    producer: Optional[ProducerModel]
    commissions: Optional[List[CommissionModel]]
    purchase: Optional[PurchaseModel]
    subscription: Optional[SubscriptionModel]

class HotmartModel(BaseModel):
    id: Optional[str]
    creation_date: Optional[int]
    event: Optional[str]
    version: Optional[str]
    data: DataModel
    hottok: str
