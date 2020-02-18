# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

# This file setup the 3 machines to be used.
Vagrant.configure("2") do |config|

    config.vm.define "vm_app" do |vm_app|
      vm_app.vm.box = "ubuntu/xenial64"

      # Create a forwarded port mapping which allows access to a specific port
      # within the machine from a port on the host machine. In the example below,
      # accessing "localhost:8080" will access port 80 on the guest machine.
      # NOTE: This will enable public access to the opened port
      vm_app.vm.network "forwarded_port", guest: 80, host: 8080, id:"nginx"

      # Create a private network, which allows host-only access to the machine
      # using a specific IP.
      vm_app.vm.network "private_network", ip: "192.168.33.10"

      # Share an additional folder to the guest VM. The first argument is
      # the path on the host to the actual folder. The second argument is
      # the path on the guest to mount the folder. And the optional third
      # argument is a set of non-required options.
      vm_app.vm.synced_folder "hello_world", "/home/vagrant/hello_world"

      # Enable provisioning with a shell script. Additional provisioners such as
      # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
      # documentation for more information about their specific syntax and use.
      vm_app.vm.provision "shell", inline: <<-SHELL
        #@--- Install packages to be used---@#
        apt-get update
        apt-get install -y nginx
        sudo rm -rf /usr/share/nginx/html/index.html
        sudo rm -rf /var/www/html/**.html
        # Endit the nginx file to show hello world
        sudo cp /home/vagrant/hello_world/index.html /usr/share/nginx/html/index.html
        sudo cp /home/vagrant/hello_world/index.html /var/www/html/index.html
        service nginx start
        sudo updatedb
      SHELL
    end

    config.vm.define "python_app" do |python_app|
      python_app.vm.box = "ubuntu/xenial64"

      python_app.vm.network "forwarded_port", guest: 80, host: 5000
      # Private in to access the nginx frm host machine
      python_app.vm.network "private_network", ip: "192.168.33.11"

      python_app.vm.synced_folder "python_core", "/home/vagrant/python_core"
      python_app.vm.synced_folder ".vagrant/machines/vm_app/virtualbox", "/home/vagrant/python_core/vm_access_key"
      python_app.vm.synced_folder ".vagrant/machines/minikube/virtualbox", "/home/vagrant/python_core/minikube_access_key"

      python_app.vm.provision "shell", inline: <<-SHELL
        # Install required packages
        sudo apt-get update
        sudo apt-get install -y apt-transport-https ca-certificates curl nginx software-properties-common
        sudo add-apt-repository ppa:deadsnakes/ppa
        sudo apt-get update
        sudo apt install -y python3.7 python3-pip
        # Setup system Locales

        export LC_ALL="en_US.UTF-8"
        export LC_CTYPE="en_US.UTF-8"
        # install virtualenv package
        echo "install virtualenv package"
        pip3 install virtualenv

      SHELL
    end

    config.vm.define "minikube" do |minikube|
      # minikube.vm.box = "alphaegg/minikube-ubuntu16"
      # minikube.vm.box_version = "1.16.3"
      minikube.vm.box = "ubuntu/xenial64"

      minikube.vm.network "forwarded_port", guest: 80, host: 8084
      # Private IP to access deployed apps on the host machine
      minikube.vm.network "private_network", ip: "192.168.33.12"
      # sync the folder that contains deploy files and start script
      minikube.vm.synced_folder "minikube_setup", "/home/vagrant/minikube_setup"

      minikube.vm.provision "shell", inline: <<-SHELL
        # install docker
        echo "Install docker"
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
        sudo add-apt-repository ppa:deadsnakes/ppa
        sudo apt-get update
        sudo apt-get install -y docker-ce

        # #Install kubectl
        echo "Downloading Kubectl"
        curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.17.0/bin/linux/amd64/kubectl
        chmod +x kubectl
        sudo mv kubectl /usr/local/bin/

        # Install minikube
        echo "install minikube"
        wget https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
        chmod +x minikube-linux-amd64
        sudo mv minikube-linux-amd64 /usr/local/bin/minikube

        # make start file executable by user only
        chmod ugo-rwx /home/vagrant/minikube_setup/start_minikube.sh
        chmod u+rwx /home/vagrant/minikube_setup/start_minikube.sh
      SHELL
    end
  end