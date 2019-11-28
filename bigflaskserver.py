# really basic boilerplate stuff

import os
from app import create_app

# development vs production
app = create_app(os.getenv("FLASK_CONFIG") or 'default')
