from sqlalchemy import Column, String

from database import Base


class PublishersModel(Base):
    __tablename__ = "publishers"

    publisher_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    def __repr__(self):
        return f"<Publisher {self.name}>"
