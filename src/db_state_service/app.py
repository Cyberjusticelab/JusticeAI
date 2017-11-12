# app, db, and models originate from here
import util
util.load_src_dir_to_sys_path()

from shared_modules.models import *

from flask_migrate import Migrate
migrate = Migrate(app, db)

