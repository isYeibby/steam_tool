"""
Steam Library Viewer - Aplicación Principal
Aplicación web para visualizar y exportar bibliotecas de Steam
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from src.config.config import Config
from src.routes.main_routes import router


def create_app():
    """
    Factory function para crear la aplicación FastAPI
    
    Returns:
        Aplicación FastAPI configurada
    """
    app = FastAPI(
        title="Steam Library Viewer API",
        description="API para visualizar y exportar bibliotecas de Steam",
        version="1.0.0"
    )
    
    # Configurar CORS para permitir peticiones desde el frontend React
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Montar archivos estáticos
    static_path = os.path.join(os.path.dirname(__file__), '..', 'static')
    if os.path.exists(static_path):
        app.mount("/static", StaticFiles(directory=static_path), name="static")
    
    # Registrar rutas
    app.include_router(router)
    
    # Ruta para servir index.html (opcional si usas React)
    @app.get("/")
    async def root():
        templates_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html')
        if os.path.exists(templates_path):
            return FileResponse(templates_path)
        return {"message": "Steam Library Viewer API"}
    
    return app


def main():
    """Función principal para ejecutar la aplicación"""
    import uvicorn
    
    print("=" * 50)
    print("Steam Library Viewer API")
    print("=" * 50)
    print(f"Servidor iniciando en http://{Config.HOST}:{Config.PORT}")
    print(f"API Key configurada: {'✓' if Config.STEAM_API_KEY else '✗'}")
    print(f"Documentación: http://{Config.HOST}:{Config.PORT}/docs")
    print("=" * 50)
    
    uvicorn.run(
        "src.app:create_app",
        factory=True,
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG
    )


if __name__ == '__main__':
    main()
