# 3rd party imports
from flask import Flask
from flask_restplus import Api

# App config
app = Flask(__name__)

API = Api(
    app,
    version='1.0',
    title="Vm to k8s migration",
    description='API to migrate from VM to K8s')

from app.api.migration_view import vm_migrate as auth_migrate
API.add_namespace(auth_migrate, path='/api')
