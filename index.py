from app import app
from environment.settings import APP_HOST, APP_PORT, APP_DEBUG
from routes import render_page_content


if __name__ == "__main__":
    app.run_server(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
