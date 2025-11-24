from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
from ..database import Base


""" Class category основная для этого сайта """

class Category(Base):
    __tablename__ = "categories" # название столбца

    id = Column(Integer,primary_key=True,index=True) # id продукта 
    name = Column(String,unique=True , nullable=True,index=True) # название продкта
    slug = Column(String,unique=True,nullable=True,index=True) # слуг продукта он нужен что-бы при поиске в гугл продукта чтобы вышел нужный продукт юзеру а гугл берет этот продукт можно сказаь с slug

    products = relationship("Product",back_populates="category") # это связь с продуктом что-бы законекися с продуктом 


    """ это функция каторая помогает видить продукты в аднмине в будущем после помтроение аднминки """
    def __repr__(self):
        return f"<Category(id='{self.id}',name='{self.name}')>" 
