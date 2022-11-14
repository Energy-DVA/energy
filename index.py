from app import app

from routes import render_page_content

# Import all required callbacks here
from pages.explore.explore_controller import update_map
from environment.settings import APP_HOST, APP_PORT, APP_DEBUG


if __name__ == "__main__":
    app.run_server(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
