import enum
import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, UUID, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from database import Base


class CoverType(enum.Enum):
    PAPERBACK = "PAPERBACK"
    HARDBACK = "HARDBACK"


class BooksModel(Base):
    __tablename__ = "books"

    book_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_title = Column(String(255), nullable=False)
    author_id = Column(String, ForeignKey("authors.author_id"), nullable=False)
    publisher_id = Column(
        String, ForeignKey("publishers.publisher_id"), nullable=False
    )
    books_meta_data = Column(JSONB, nullable=True)
    media_data = Column(JSONB, nullable=True)
    pages = Column(Integer, nullable=False)
    publication_year = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    subject = Column(String(255), nullable=False)
    language = Column(String(100), nullable=False)
    cover_type = Column(Enum(CoverType, name="cover_types"), nullable=False)

    # Relationships
    author = relationship("Author", backref="books")
    publisher = relationship("Publisher", backref="books")

    def __repr__(self):
        return f"<Book {self.book_title} ({self.publication_year})>"
