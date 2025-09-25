# Tarea3_PDC
# User API — FastAPI + SQLAlchemy

API REST para gestionar usuarios y persistir información en una base de datos, construida con **FastAPI** y **SQLAlchemy**.  

---

## Instalación

### Prerrequisitos
- Python **3.8+**
- [uv](https://github.com/astral-sh/uv) (gestor de paquetes Python moderno)

---

### 1. Clonar el repositorio
```bash
git clone <tu-repo>
cd user-api

# Crear entorno virtual
uv venv

### 2. Crear entorno virtual e instalar dependencias 
# Activar entorno virtual
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux / Mac

# Instalar dependencias
uv pip install fastapi uvicorn sqlalchemy pydantic[email] python-dotenv
