from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Comedor(Base):
    __tablename__ = "comedores"

    id = Column(Integer, primary_key=True, index=True)
    provincia = Column(String)
    barrio_anonimo = Column(String)
    tipo_comedor = Column(String)
    capacidad_viandas = Column(Integer)
    voluntarios = Column(Integer)
    ratio = Column(Integer)
    estado = Column(String, default="activo")
    activo = Column(Boolean, default=True)