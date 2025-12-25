# Steam Library Viewer

Aplicación web para visualizar y exportar tu biblioteca de Steam con una interfaz moderna.

## Características

- Visualiza toda tu biblioteca de Steam
- Estadísticas detalladas (total de juegos, horas jugadas, promedio, etc.)
- Exportación a CSV

## Requisitos

- Python 3.7 o superior
- Steam API Key
- Perfil de Steam público

## Instalación

1. **Clonar o descargar el proyecto**

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv .venv
   ```

3. **Activar el entorno virtual**
   
   En Windows (PowerShell):
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   En Windows (CMD):
   ```cmd
   .venv\Scripts\activate.bat
   ```
   
   En Linux/Mac:
   ```bash
   source .venv/bin/activate
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Configuración

1. **Obtener tu Steam API Key**
   - Ve a https://steamcommunity.com/dev/apikey
   - Inicia sesión con tu cuenta de Steam
   - Registra tu dominio (puedes usar `localhost`)
   - Copia tu API Key

2. **Configurar la API Key en el archivo .env**
   - Crea un archivo llamado `.env` en la raíz del proyecto (si no existe)
   - Agrega tu API Key de la siguiente forma:
   ```env
   STEAM_API_KEY=TU_API_KEY_AQUI
   ```
   - Ejemplo:
   ```env
   STEAM_API_KEY=A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6
   ```
   - El archivo `.gitignore` ya está configurado para ignorarlo.

## Uso

### Iniciar el servidor

**Recomendado:**
```bash
python run.py
```

Verás un mensaje como:
```
==================================================
Steam Library Viewer
==================================================
Servidor iniciando en http://0.0.0.0:5000
API Key configurada: ✓
==================================================
```

### Acceder a la aplicación

Abre tu navegador web y ve a:
- **Local:** http://localhost:5000
- **Red local:** http://TU_IP:5000

### Configurar perfil de Steam

1. **Encontrar tu Steam ID**
   - Opción 1: Ve a tu perfil de Steam y copia el número de 17 dígitos de la URL
   - Opción 2: Usa https://steamid.io para encontrar tu Steam ID64
   - Ejemplo: `76561198012345678`

2. **Configurar perfil público**
   - Ve a tu perfil de Steam
   - Click en "Editar perfil"
   - En "Configuración de privacidad", establece "Detalles del juego" como **Público**

3. **Usar la aplicación web**
   - Ingresa tu Steam ID en la aplicación
   - Explora estadísticas y juegos
   - Exporta datos a CSV