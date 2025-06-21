import uuid

from sqlalchemy import UUID, Column, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship

from repositories.base import BaseModel


class UserAddressesModel(BaseModel):
    __tablename__ = "user_addresses"

    address_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )

    full_name = Column(String(255), nullable=False)
    address_line_1 = Column(String(255), nullable=False)
    address_line_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    isd_code = Column(String, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    user = relationship("UsersModel", backref="addresses")
