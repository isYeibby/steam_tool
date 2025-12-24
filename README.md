# Steam Library Viewer

Visualiza y exporta tu biblioteca de Steam con una interfaz web moderna.

## Requisitos

- Python 3.7 o superior
- Steam API Key
- Perfil de Steam público

## Instalación

1. **Clonar o descargar el proyecto**

2. **Crear entorno virtual (opcional pero recomendado)**
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
   pip install flask pandas requests python-dotenv
   ```

## Configuración

1. **Obtener tu Steam API Key**
   - Ve a https://steamcommunity.com/dev/apikey
   - Inicia sesión con tu cuenta de Steam
   - Registra tu dominio (puedes usar `localhost` para desarrollo)
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
   - **IMPORTANTE:** Nunca subas el archivo `.env` a repositorios públicos. El archivo `.gitignore` ya está configurado para ignorarlo.

## Uso

### Iniciar el servidor

```bash
python steam_web_viewer.py
```

O si usas el entorno virtual:

```powershell
C:/Users/sYeib/Documentos/Tests/.venv/Scripts/python.exe steam_web_viewer.py
```

Verás un mensaje como:
```
Steam Library Viewer
Servidor iniciando en http://localhost:5000
API Key configurada
 * Running on http://127.0.0.1:5000
```

### Acceder a la aplicación

Abre tu navegador web y ve a:
- **Local:** http://localhost:5000
- **Red local:** http://TU_IP:5000 (ejemplo: http://192.168.1.100:5000)

### Usar la aplicación

1. **Encontrar tu Steam ID**
   - Opción 1: Ve a tu perfil de Steam y copia el número de 17 dígitos de la URL
   - Opción 2: Usa https://steamid.io para encontrar tu Steam ID64
   - Ejemplo: `76561198012345678`

2. **Configurar perfil público**
   - Ve a tu perfil de Steam
   - Click en "Editar perfil"
   - En "Configuración de privacidad", establece "Detalles del juego" como **Público**

3. **Cargar tu biblioteca**
   - Ingresa tu Steam ID en el campo de texto
   - Click en "Cargar Biblioteca"
   - Espera unos segundos mientras se cargan tus juegos

4. **Funcionalidades disponibles**
   - uscar juegos por nombre
   - Ver estadísticas de tu biblioteca
   - Exportar a CSV
   - Ver detalles de cada juego (horas jugadas, última vez jugado, etc.)
