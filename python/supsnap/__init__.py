import models
import controllers
from app import app
from db import db

if __name__ == "__main__":
    models.init()
    app.run(host="0.0.0.0", debug = True)
