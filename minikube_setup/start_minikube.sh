#!/bin/bash

#@--- Function starts up minikube and sets up deploy env ---@#
set_up_minikube() {

    #@--- start minikube ---#@
    sudo minikube start --vm-driver=none
    #@--- perform cluster role binding ---@#
    #@--- without this the token generated will not be able to perform deployment ---@#
    #@--- Error 403 accessing K8S api ---@#
    sudo kubectl create clusterrolebinding serviceaccounts-cluster-admin --clusterrole=cluster-admin --group=system:serviceaccounts
    #@--- generate token to use to deploy---@#
    #@--- this will be used to deploy by interacting with the K8S API ---@#
    eval "TOKEN=$(sudo kubectl get secret $(sudo kubectl get serviceaccount default -o jsonpath='{.secrets[0].name}') -o jsonpath='{.data.token}' | base64 --decode )"
    #@-- Get k8s server address ---@#
    sudo kubectl cluster-info > k8s.txt
    CLUSTER_INFO=`head -n 1 k8s.txt`
    echo $CLUSTER_INFO > k8s.txt
    APISERVER=eval "$(echo $CLUSTER_INFO | awk '{print $6}')"
    echo $APISERVER
}

#@--- Main function ---@#
main() {
    #@--- Run setup function ---@#
    set_up_minikube
}

#@--- Run main function ---@#
main
