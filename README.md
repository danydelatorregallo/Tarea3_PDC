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

### 2. Crear entorno virtual e instalar dependencias
# Crear entorno virtual
uv venv

# Activar entorno virtual
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux / Mac

# Instalar dependencias
uv pip install fastapi uvicorn sqlalchemy pydantic[email] python-dotenv

### 3. Configurar variables de entorno

Crea un archivo .env en la raíz del proyecto basándote en .env.example:

cp .env.example .env


Edita el archivo .env con tu configuración:

API_KEY=tu_api_key_secreta_aqui

🚀 Ejecutar la aplicación
Desarrollo
uvicorn main:app --reload

Producción
uvicorn main:app --host 0.0.0.0 --port 8000


La API estará disponible en:

Aplicación: http://localhost:8000

Documentación interactiva: http://localhost:8000/docs

Autenticación

Todos los endpoints requieren el header:

X-API-Key: tu_api_key_secreta_aqui

Endpoints disponibles
Método	Endpoint	Descripción
POST	/api/v1/users/{user_id}	Crear un nuevo usuario
GET	/api/v1/users/{user_id}	Obtener usuario por ID
PUT	/api/v1/users/{user_id}	Actualizar usuario
DELETE	/api/v1/users/{user_id}	Eliminar usuario
📝 Ejemplos de uso
Crear usuario
curl -X POST "http://localhost:8000/api/v1/users/1" \
  -H "X-API-Key: tu_api_key_secreta_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "user_name": "Juan Pérez",
    "user_email": "juan@example.com",
    "age": 25,
    "recommendations": ["producto1", "producto2"],
    "ZIP": "12345"
  }'

Obtener usuario
curl -X GET "http://localhost:8000/api/v1/users/1" \
  -H "X-API-Key: tu_api_key_secreta_aqui"

Actualizar usuario
curl -X PUT "http://localhost:8000/api/v1/users/1" \
  -H "X-API-Key: tu_api_key_secreta_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "Juan Carlos Pérez",
    "age": 26
  }'

Eliminar usuario
curl -X DELETE "http://localhost:8000/api/v1/users/1" \
  -H "X-API-Key: tu_api_key_secreta_aqui"

Códigos de respuesta
Código	Descripción
401	API Key inválida
404	Usuario no encontrado
409	Conflicto (email o user_id duplicado)
🗒️ Notas adicionales

La base de datos SQLite (users.db) se crea automáticamente al iniciar la aplicación.

Los campos age, recommendations y ZIP son opcionales.

El user_email debe ser único en la base de datos.

El user_id debe ser único y se especifica en la URL del endpoint.
