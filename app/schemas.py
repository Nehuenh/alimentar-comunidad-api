from pydantic import BaseModel, field_validator

class ComedorBase(BaseModel):
    provincia: str
    barrio_anonimo: str
    tipo_comedor: str
    capacidad_viandas: int
    voluntarios: int

    @field_validator('capacidad_viandas')
    def validar_ratio(cls, v, info):
        voluntarios = info.data.get('voluntarios')
        if voluntarios and voluntarios > 0:
            if v / voluntarios > 1000:
                raise ValueError(f'Ratio viandas/voluntarios {v/voluntarios} > 1000 inconsistente - regla RENACOM')
        return v

class ComedorCreate(ComedorBase):
    pass

class ComedorResponse(ComedorBase):
    id: int
    ratio: int
    estado: str
    activo: bool

    class Config:
        from_attributes = True