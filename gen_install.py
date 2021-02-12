#!/usr/bin/env python3

import os
import platform
import json
import tempfile
import stat

from shutil import which

script_dir = os.path.dirname(os.path.realpath(__file__))

dot_file_path = os.path.join(script_dir, "dot.json")

available_providers = [
    "apt-get",
    "brew"
]

def provider_for_system():
    for provider in available_providers:
        if which(provider) is not None:
            return provider
    return None

def provider_install_cmd():
    if provider_for_system() == "apt":
        return "apt-get update && apt-get install -y"
    elif provider_for_system() == "brew":
        return "brew update && brew install"


def find_pkg_for_provider(package):
    try:
        providers = package["providers"]
        for provider in providers:
            try:
                return provider[provider_for_system()]
            except KeyError:
                return package["name"]
    except KeyError:
        return package["name"]

install_file = tempfile.mkstemp()[1]

packages = []
preinstalls = []
with open(dot_file_path) as json_config:
    data = json.load(json_config)
    operating_system = platform.system()
    for package in data["packages"]:
        try:
            if operating_system == package["os"]:
                packages.append(find_pkg_for_provider(package))
        except KeyError:
            packages.append(find_pkg_for_provider(package))

        try:
	        pre_install = package["pre_install"]
	        for provider in pre_install:
	            if provider[provider_for_system()] != None:
	                preinstalls.append(provider[provider_for_system()])
        except KeyError:
            continue
            

with open(install_file, 'wt') as file:
    file.write("#!/bin/sh\nset -e\n")
    for preinstall in preinstalls:
        file.write(preinstall + "\n")    
    file.write(provider_install_cmd() + " \\\n")
    for pkg in packages:
        file.write(pkg + " \\\n")

os.chmod(install_file, os.stat(install_file).st_mode | stat.S_IEXEC)

print("Installation file generated. Start the installation by calling \nsh -c " + install_file)

