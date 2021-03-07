#!/bin/bash
set -e
script_dir=$(cd "$(dirname "$0")"; pwd)

function run() {
  stage=$1

  cmd=$("$script_dir"/gen_"$stage".py | tail -n 1)

  echo "${stage} script generated"
  echo "Do you want to ${stage} now? (y/N)"
  read -n1 reply

  if [ "$reply" == "y" ];then
    ${cmd}
  else
    echo -e "\nOk. You can still do this later by calling:"
    echo "$cmd"
    echo "If you want to generate the file again call $script_dir/gen_$stage.py"
  fi

}
if [ "$#" -ne 0 ];then
  echo "Called with parameter. Running $1 script"
  run "$1"
else
  echo "Running default configuration"
  run install
  run configure
fi
