# Steam Library Viewer

Aplicación web para visualizar y exportar bibliotecas de Steam con interfaz moderna Material Design 3.

## Requisitos

- Python 3.7+
- Node.js 16+
- Steam API Key
- Perfil de Steam público

## Instalación

### Backend (FastAPI)

```bash
cd backend-steam-viewer
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
source .venv/bin/activate    # Linux/Mac
pip install -r requirements.txt
```

### Frontend (React + Vite)

```bash
cd frontend-steam-viewer
npm install
```

## Configuración

1. Obtén tu Steam API Key en https://steamcommunity.com/dev/apikey

2. Crea un archivo `.env` en la raíz del proyecto:

```env
STEAM_API_KEY=TU_API_KEY_AQUI
```

3. Asegúrate de que tu perfil de Steam sea público:
   - Ve a tu perfil de Steam
   - Editar perfil > Configuración de privacidad
   - Establece "Detalles del juego" como Público

## Uso

### Iniciar Backend

```bash
cd backend-steam-viewer
python run.py
```

El servidor estará en http://localhost:5000
Documentación API: http://localhost:5000/docs

### Iniciar Frontend

```bash
cd frontend-steam-viewer
npm run dev
```

La aplicación estará en http://localhost:5173

## Obtener Steam ID

- Opción 1: Copia el número de 17 dígitos de tu URL de perfil de Steam
- Opción 2: Usa https://steamid.io

Ejemplo: `76561198012345678`

## Tecnologías

**Backend:** FastAPI, Python, Pandas, Requests
**Frontend:** React, Vite, Lucide Icons, Axios
**Diseño:** Material Design 3
