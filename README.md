# Alimentar Comunidad API

API REST para gestión de comedores comunitarios - inspirado en trabajo real RENACOM.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688)
![Tests](https://img.shields.io/badge/tests-4%20passed-brightgreen)

**Autor:** Nehuen Herrero (Est. Lic. Física - 40k registros RENACOM gestionados)

**Repo:** https://github.com/Nehuenh/alimentar-comunidad-api

### Stack
- Python + FastAPI + SQLAlchemy + SQLite + Pandas
- Validaciones de negocio (ratio viandas/voluntarios > 1000 = inconsistente)
- Soft-delete para trazabilidad
- Dataset anonimizado (barrios anonimizados)

### Endpoints
- `GET /` - health check
- `GET /comedores` - lista activos
- `GET /comedores/{provincia}` - filtra por provincia
- `POST /comedores` - crea con validación de ratio
- `DELETE /comedores/{id}` - soft delete

### Correr
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# docs: http://127.0.0.1:8000/docs
