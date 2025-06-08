from common.utils import EnumBase


class OrderStatus(EnumBase):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
