from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class sqlm(Base):
    __tablename__ = "sqlm1"
    
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean,default = False)
    
    