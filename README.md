## VM to K8S migration
This project showcases the migration from a vm app to k8s minikube instance.

### VMs setup and running the App
#### Prerequisites
Ensure you have [vagrant]('https://www.vagrantup.com/') and [virtualbox]('https://tecadmin.net/install-virtualbox-on-ubuntu-18-04/') installed or your favorite virtualization software.

##### Tools used

    - Minikube

    - Vagrant

    - VirtualBox

 #### Language
    - Python/Flask

#### Getting started
To set up the first vm run
    `vagrant up vm_app` this will spin up the first Vm that runs nginx hello world page.
    once the machine is up you can access its content on IP `192.168.33.10`

To set up the minikube vm:
    Run the command `vagrant up minikube` this will spin up the minikube vm. Once the command has
    finished executing you will need to ssh into the machine to finish up the setting up process.
    To ssh into the VM, run the command `vagrant ssh minikube` and your terminal will switch up to
    `vagrant@ubuntu-xenial:~$`
    run the following commands to set up the environment in this machine:

    ```
    ---> sudo minikube start --vm-driver=none
    ---> sudo kubectl create clusterrolebinding serviceaccounts-cluster-admin --clusterrole=cluster-admin --group=system:serviceaccounts
    ---> sudo kubectl cluster-info
    ---> TOKEN=$(sudo kubectl get secret $(sudo kubectl get serviceaccount default -o jsonpath='{.secrets[0].name}') -o jsonpath='{.data.token}' | base64 --decode )

    ```
open  the `sample.env` file under python_core folder and save the new environment vars obtained above
add APISERVER='IP ADDR OF YOUR K8S SERVER' found from output of the cluster-info command above.
add TOKEN="VALUE OF TOKEN GENERATED ABOVE"
you can save the file as .env  as we will later load it up in the python Vm.

Check if the node is running with command  `sudo kubectl get node`

![](readme_images/node.png?raw=true "Node image")

To set up the python_vm:
    Run the command `vagrant up python_app` this will spin up the python_app vm. Once the command has
    finished executing you will need to ssh into the machine to finish up the setting up process.
    To ssh into the VM, run the command `vagrant ssh python_app` and your terminal will switch up.
    Run the following commands to start the python app  in the VM:

    ```
    ---> `cd python_core` --> Change directory to the python app
    ---> `export LC_ALL="en_US.UTF-8"` --> Set system locales
    ---> `export LC_CTYPE="en_US.UTF-8"` --> Set system locales
    ---> `pip3 install pipenv`  --> Install pipenv
    ---> `pipenv install` --> Install application packages
    ---> `pipenv shell` --> Start up the virtual environment
    ---> `source .env` --> Load up the environment variables ensure the TOKEN and APISERVER exist
    ---> `gunicorn --access-logfile '-' --workers 2 run:app -b 0.0.0.0:5000` --> Run the application with gunicorn.
    ```

The API is then accessible on the IP: `192.168.33.11:5000`. On the try it tab enter the vm_ip the username and password.

![](readme_images/API_input.png?raw=true "API_input prompt")

check that all Vms are running on the terminal with `vagrant status` --> Run this on the path where the Vagrant file sits.

![](readme_images/vagrant_status.png?raw=true "vagrant status")

### Then click on execute.
#### Checking on the running app in minikube
SSH into the minikube machine, run the command `sudo kubectl get pods -n default` you will find running pod of the hello app

![](readme_images/pods.png?raw=true "pods image")

To find the service run the command `sudo kubectl get services -n default` you will see the service running the app.

![](readme_images/service.png?raw=true "service image")

The app is accessible on api `192.168.33.12:node_ip` get node ip from the command above


### Cleanup
You can easily perform clean up with vagrant. To stop all Vms run the command: `vagrant halt`

![](readme_images/halt.png?raw=true "Stop machines")

This will stop the Vms but not free storage held

![](readme_images/status_halt.png?raw=true "Stop status")

To free up storage held run: `vagrant destroy` then accept the destruction prompt that will appear on the terminal. Then check on the status and it will show that machines are not created.

![](readme_images/dest.png?raw=true "Final Cleanup")

:clap:
##                                                                             Thank you ##