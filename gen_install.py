#!/usr/bin/env python3

import os
import platform
import json
import tempfile
import stat

from shutil import which

script_dir = os.path.dirname(os.path.realpath(__file__))

dot_file_path = os.path.join(script_dir, "dot.json")

available_providers = []


def provider_for_system():
    for provider in available_providers:
        provider_id = provider["id"] 
        if which(provider_id) is not None:
            return provider_id
    provider_names = []
    for p in available_providers:
        provider_names.append(p["id"])
    raise LookupError("None of the providers {} are available on your system".format(provider_names))

def provider_install_cmd():
    command = next(item for item in available_providers if item["id"] == provider_for_system())["command"]
    return command

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
supported_providers_version = 1
preinstalls = []
supported_dot_version = 1

with open(os.path.join(script_dir, "providers.json")) as json_providers:
    data = json.load(json_providers)
    assert supported_providers_version == data["version"], "This version of dot supports only provider file format '{}'. You're using fileformat version '{}'".format(supported_providers_version, data["version"])
    for provider in data["providers"]:
        prov = {}
        prov["id"] = list(provider.keys())[0]
        prov["command"] = provider[prov["id"]]
        available_providers.append(prov)

with open(dot_file_path) as json_config:
    data = json.load(json_config)
    assert supported_dot_version == data["version"], "This version of dot supports only file format '{}'. You're using fileformat version '{}'".format(supported_dot_version, data["version"])
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

