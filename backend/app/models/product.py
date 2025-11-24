from sqlalchemy import String,Integer,Column,Text,Float,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Product(Base):
    __tablename__="products"

    id = Column(Integer,primary_key=True,unique=True,index=True)
    name = Column(String,nullable=False,index=True)
    description = Column(Text)
    price = Column(Integer,nullable=False)
    category_id = Column(Integer,ForeignKey("categories.id"),nullable=True)
    image_url = Column(String)
    created_at = Column(DateTime,default=datetime.utcnow)

    category = relationship('Category',back_populates="products")

    def __repr__(self):
        return f"Product(id='{self.id}', name='{self.name}', price='{self.price}')"
    