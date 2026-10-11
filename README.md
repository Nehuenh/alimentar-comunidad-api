# Alimentar Comunidad API

API REST para gestión de comedores comunitarios - inspirado en trabajo real RENACOM.

**Autor:** Nehuen Herrero (Est. Lic. Física - 40k registros RENACOM gestionados)

### Stack
- Python + FastAPI + SQLAlchemy + SQLite + Pandas
- Validaciones de negocio (ratio viandas/voluntarios > 1000 = inconsistente)
- Soft-delete para trazabilidad
- Dataset anonimizado (barrios anonimizados)

### Endpoints
- `GET /comedores` - lista activos
- `GET /comedores/{provincia}` - filtra por provincia
- `DELETE /comedores/{id}` - soft delete

### Correr
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
