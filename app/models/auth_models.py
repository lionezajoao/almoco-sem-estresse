from pydantic import BaseModel
from typing import List

class AuthModel(BaseModel):
    id: str
    creation_date: int
    event: str
    version: str
    data: dict

class AddressModel(BaseModel):
    country: str
    country_iso: str

class BuyerModel(BaseModel):
    email: str
    name: str
    checkout_phone: str
    address: AddressModel

class CommissionModel(BaseModel):
    value: float
    source: str
    currency_value: str

class FullPriceModel(BaseModel):
    value: float
    currency_value: str

class PriceModel(BaseModel):
    value: float
    currency_value: str

class CheckoutCountryModel(BaseModel):
    name: str
    iso: str

class OrderBumpModel(BaseModel):
    is_order_bump: bool
    parent_purchase_transaction: str

class OriginalOfferPriceModel(BaseModel):
    value: float
    currency_value: str

class PaymentModel(BaseModel):
    installments_number: int
    type: str

class OfferModel(BaseModel):
    code: str

class PlanModel(BaseModel):
    id: int
    name: str

class SubscriberModel(BaseModel):
    code: str

class ProductModel(BaseModel):
    id: int
    ucode: str
    name: str
    has_co_production: bool

class AffiliateModel(BaseModel):
    affiliate_code: str
    name: str

class ProducerModel(BaseModel):
    name: str

class SubscriptionModel(BaseModel):
    status: str
    plan: PlanModel
    subscriber: SubscriberModel

class PurchaseModel(BaseModel):
    approved_date: int
    full_price: FullPriceModel
    price: PriceModel
    checkout_country: CheckoutCountryModel
    order_bump: OrderBumpModel
    original_offer_price: OriginalOfferPriceModel
    order_date: int
    status: str
    transaction: str
    payment: PaymentModel
    offer: OfferModel
    sckPaymentLink: str

class DataModel(BaseModel):
    product: ProductModel
    affiliates: List[AffiliateModel]
    buyer: BuyerModel
    producer: ProducerModel
    commissions: List[CommissionModel]
    purchase: PurchaseModel
    subscription: SubscriptionModel

class HotmartModel(BaseModel):
    id: str
    creation_date: int
    event: str
    version: str
    data: DataModel
    hottok: str