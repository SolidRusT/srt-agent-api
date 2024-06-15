from app.api_service import app

def create_app():
    return app

if __name__ == "__main__":
    import os
    import uvicorn
    from srt_core.config import Config

    config = Config()
    server_name = os.getenv("SERVER_NAME", config.server_name)
    server_port = int(os.getenv("SERVER_PORT", config.server_port))

    uvicorn.run(app, host=server_name, port=server_port)
