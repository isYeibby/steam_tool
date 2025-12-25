"""
Steam Library Viewer - Aplicación Principal
API FastAPI para visualizar y exportar bibliotecas de Steam
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    
    # Registrar rutas de la API
    app.include_router(router)
    
    # Ruta raíz de la API
    @app.get("/")
    async def root():
        return {
            "message": "Steam Library Viewer API",
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    
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
