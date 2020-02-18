#!/bin/bash

#@--- fuction to spin up the api ---@#
start_api() {
    #@--- Set system locales ---@#
    export LC_ALL="en_US.UTF-8"
    export LC_CTYPE="en_US.UTF-8"
    #@--- Install pipenv ---@#
    pip3 install pipenv
    #@--- Install packages ---@#
    pipenv install
    #@--- Start virtualenvironment ---@#
    pipenv shell
    #@---export env variables ---@#
    source .env &
    #@---Start application ---@#
    # gunicorn --access-logfile '-' --workers 2 run:app -b 0.0.0.0:5000
    python3.7 run.py
}

#@--- Main function ---@#
main() {
    start_api
}

#@--- Run main function ---@#
main
