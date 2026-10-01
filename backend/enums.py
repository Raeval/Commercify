from enum import Enum

class GenderType(str, Enum):
    MALE = "male",
    FEMALE = "female",
    NONE = "prefer not to say"

class ShopPlan(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    PRO = "pro"

class OrderStatus(str, Enum):
    PENDING = "pending"
    SHIPPING = "shipping"
    PREPARING = "preparing"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"