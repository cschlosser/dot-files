#!/usr/bin/env python2

import os
import platform
import json
import tempfile
import stat
import sys
import time

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(script_dir, "third_party", "jinja"))

from jinja2 import Template

dot_file_path = os.path.join(script_dir, "dot.json")

cfg_file = tempfile.mkstemp()[1]

packages = []
supported_dot_version = 1
with open(dot_file_path) as json_config:
    data = json.load(json_config)
    assert supported_dot_version == data["version"], "This version of dot supports only file format '{}'. You're using fileformat version '{}'".format(supported_dot_version, data["version"])
    operating_system = platform.system()
    for package in data["packages"]:
        try:
            if operating_system != package["os"]:
                continue
        except KeyError:
            pass

        try:
            pkg = {}
            pkg["name"] = package["name"]
            pkg["time"] = time.time()
            cfgs = []
            for config in package["config"]:
                for cfg in config.keys():
                    mapping = {}
                    mapping["src"] = os.path.join(script_dir, package["name"], cfg)
                    mapping["dst"] = config[cfg]
                    cfgs.append(mapping)
            pkg["configs"] = cfgs
            packages.append(pkg)
        except KeyError:
            pass

data = '''#!/bin/bash
set -e
# From https://unix.stackexchange.com/a/85069
function relpath() {
        python2 -c 'import os.path, sys;\
  print os.path.relpath(sys.argv[1],sys.argv[2])' "$1" "${2-$PWD}"
}

{% for package in CONFIGS %}
echo "Configuring {{ package.name }}..."
{% for cfg in package.configs %}
mkdir -vp $(dirname {{ cfg.dst }})

source=$(relpath "{{ cfg.src }}" $(dirname "{{ cfg.dst }}"))

# skip if cfg.src is same as existing link target: ls -l cfg.dst | awk '{print $NF}'
if [[ "$source" == $(ls -l {{ cfg.dst }} | awk '{print $NF}') ]]; then
  echo "Skipping {{ cfg.dst }} as it already points to {{ cfg.src }}"
else
  if [[ -L {{ cfg.dst }} || -e {{ cfg.dst }} ]]; then
    backup_name={{ cfg.dst }}_dot_backup_{{ package.time }}
    echo "{{ cfg.dst }} already exists. Creating backup: $backup_name"
    mv -v {{ cfg.dst }} "$backup_name"
  fi

  ln -sv "$source" {{ cfg.dst }}
fi
{% endfor %}
echo "...done"
echo
{% endfor %}
'''
tm = Template(data)
msg = tm.render(CONFIGS=packages)

with open(cfg_file, 'wt') as file:
    file.write(msg)
    
os.chmod(cfg_file, os.stat(cfg_file).st_mode | stat.S_IEXEC)
print("Config setup file generated. Configure your dot files by calling \nsh -c " + cfg_file)


