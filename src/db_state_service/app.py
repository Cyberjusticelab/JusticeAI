# app, db, and models originate from here
import models

from flask_migrate import Migrate
migrate = Migrate(app, db)

