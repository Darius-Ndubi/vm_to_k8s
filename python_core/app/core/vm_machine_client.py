import sys
from loguru import logger
from os import system, getenv
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException


logger.add(
    sys.stderr,
    format="{time} {level} {message}",
    filter="client",
    level="INFO"
)
logger.add(
    "logs/log_{time:YYYY-MM-DD}.log",
    format="{time} {level} {message}",
    filter="client",
    level="ERROR",
)


class RemoteClient:
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(self, host, user, password, ssh_key_path):

        self.host = host
        self.user = user
        self.port = 22
        self.password = password
        self.ssh_key_filepath = ssh_key_path
        self.client = None
        self.scp = None
        self.__upload_ssh_key()

    def __get_ssh_key(self):
        """Fetch locally stored SSH key."""
        try:
            self.ssh_key = RSAKey.from_private_key_file(self.ssh_key_filepath)
            logger.info(f"Found SSH key at self {self.ssh_key_filepath}")
        except SSHException as error:
            logger.error(error)
        return self.ssh_key

    def __upload_ssh_key(self):
        try:
            system(
                f"ssh-copy-id -i {self.ssh_key_filepath} {self.user}@{self.host}>/dev/null 2>&1"
            )
            system(
                f"ssh-copy-id -i {self.ssh_key_filepath}.pub {self.user}@{self.host}>/dev/null 2>&1"
            )
            logger.info(f"{self.ssh_key_filepath} uploaded to {self.host}")
        except FileNotFoundError as error:
            logger.error(error)

    def remote_connect(self):
        """Open connection to remote host."""

        username = self.user
        try:
            self.client = SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(
                self.host,
                self.port,
                username,
                self.password,
                key_filename=self.ssh_key_filepath,
                look_for_keys=True,
                timeout=5000,
            )
            self.scp = SCPClient(self.client.get_transport())  # For later
        except AuthenticationException as error:
            logger.info(
                "Authentication failed: did you remember to create an SSH key?")
            logger.error(error)
            raise error
        finally:
            return self.client

    def disconnect(self):
        """Close ssh connection."""
        self.client.close()
        self.scp.close()

    def execute_commands_vm_app(self, commands):
        """Execute multiple commands in succession."""
        if self.client is None:
            self.client = self.remote_connect()
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            for line in response:
                logger.info(f'INPUT: {cmd} | OUTPUT: {line}')
                return line

    def execute_commands_minikube(self, commands):
        """Execute multiple commands in succession."""
        if self.client is None:
            self.client = self.remote_connect()
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(str(cmd))
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            for line in response:
                logger.info(f'INPUT: {cmd} | OUTPUT: {line}')

    def download_file(self, remote_path):
        """Download file from remote host."""
        self.conn = self.remote_connect()
        self.scp.get(
            remote_path=remote_path,
            recursive=True
            )
        return {
            "message": "Success"
        }

    def upload_dockerfile(self, file):
        """send dockerfile to minikube machine"""
        self.conn = self.remote_connect()
        try:
            self.scp.put(file,
                         remote_path='/home/vagrant',
                         recursive=True)
        except SCPException as error:
            logger.error(error)
            raise error
        finally:
            return file
