from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import tempfile

import pytest
from flask import json

from rasa_nlu import data_router
from rasa_nlu.components import ComponentBuilder
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu import registry
from rasa_nlu.project import Project
from rasa_nlu.model import Interpreter, Metadata
from rasa_nlu.train import do_train

pytest_plugins = str("pytest_twisted")

#Create config file
#Create data file
#Create Flask-Database
#Create response strings


def create_config_file(config_file):
    with tempfile.NamedTemporaryFile("w+", suffix="tmp_config_file.json", delete=False) as c:
        c.write(json.dumps(config_file))
        c.flush()
        return c

def create_data_file(data):
    with tempfile.NamedTemporaryFile("w+", suffix="tmp_data_file.json", delete=False) as d:
        d.write(json.dump(data))
        d.flush()
        return d

