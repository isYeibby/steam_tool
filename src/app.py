"""
Steam Library Viewer - Aplicación Principal
Aplicación web para visualizar y exportar bibliotecas de Steam
"""
from flask import Flask
from src.config.config import Config
from src.routes.main_routes import main_bp


def create_app():
    """
    Factory function para crear la aplicación Flask
    
    Returns:
        Aplicación Flask configurada
    """
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )
    
    # Cargar configuración
    app.config.from_object(Config)
    
    # Registrar Blueprints
    app.register_blueprint(main_bp)
    
    return app


def main():
    """Función principal para ejecutar la aplicación"""
    app = create_app()
    
    print("=" * 50)
    print("Steam Library Viewer")
    print("=" * 50)
    print(f"Servidor iniciando en http://{Config.HOST}:{Config.PORT}")
    print(f"API Key configurada: {'✓' if Config.STEAM_API_KEY else '✗'}")
    print("=" * 50)
    
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )


if __name__ == '__main__':
    main()
