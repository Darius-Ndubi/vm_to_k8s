""" Module with migration route """
import os

# 3rd party imports
from flask_restplus import Resource, Namespace, fields
from flask import request

# local imports
from app.core.vm_machine_client import RemoteClient
from app.core.create_docker_image import create_docker_file

vm_migrate = Namespace(
    'migrate',
    description='Vm to k8s migration endpoint')


insert_user_data = vm_migrate.model("Insert_user_data", {
    "vm_ip": fields.String(description="VM IP", required=True),
    "username": fields.String(description="Username", required=True),
    "password": fields.String(description="password", required=True)
    })

@vm_migrate.route(
    '/migrate/auth')
class MigrateView(Resource):
    '''Allow user to authorize migration'''
    @vm_migrate.expect(insert_user_data)
    def post(self):

        key_path = os.getenv('SSH_KEY_PATH')
        remote = RemoteClient(
            request.json['vm_ip'],
            request.json['username'],
            request.json['password'],
            key_path
        )

        file_path = remote.execute_commands_vm_app(
            ["rm -rf out.txt", 'locate nginx | grep ".html" > out.txt', "sed -n 2p out.txt"]
        )

        remote.download_file(file_path[0:-1])
        # Build image
        create_docker_file()

        # send dockerfile to minikube machine
        key_path = os.getenv('SSH_KEY_PATH_MINIKUBE')
        # minikube machine
        remote2 = RemoteClient(
            '192.168.33.12',
            'vagrant',
            'vagrant',
            key_path
        )
        # send docker file to minikube machine
        file = "Dockerfile"
        remote2.upload_dockerfile(file)

        # Send nginx file
        index_file = 'index.html'
        remote2.upload_dockerfile(index_file)

        cluster_default_pods = 'curl -H "Authorization: Bearer {TOKEN}" {APISERVER}/api/v1/namespaces/default/pods/ --insecure'.format(
            TOKEN=os.getenv('TOKEN'), APISERVER=os.getenv('APISERVER'))
        create_deployment = 'curl --request POST -H "Authorization: Bearer {TOKEN}" -H "content-type: application/json" {APISERVER}/apis/apps/v1/namespaces/default/deployments -d@minikube_setup/deployment.json --insecure'.format(
            TOKEN=os.getenv('TOKEN'), APISERVER=os.getenv('APISERVER'))
        create_deployment_service = 'curl --request POST -H "Authorization: Bearer {TOKEN}" -H "content-type: application/json" {APISERVER}/api/v1/namespaces/default/services -d@minikube_setup/service.json --insecure'.format(
            TOKEN=os.getenv('TOKEN'), APISERVER=os.getenv('APISERVER'))

        # Run deployments on the minikube machine
        remote2.execute_commands_minikube(
            [
            "sudo docker build -t hello-app .",
            cluster_default_pods,
            create_deployment,
            create_deployment_service,
            "sudo kubectl get services --all-namespaces"
            ]
        )
        # Terminate sessions
        remote.disconnect()
        remote2.disconnect()
        return {
            "message":"App successfully deployed in minikube"
        }, 200
