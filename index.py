from app import app

from routes import render_page_content

# Import all required callbacks here
from environment.settings import APP_HOST, APP_PORT, APP_DEBUG


if __name__ == "__main__":
    app.run_server(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
