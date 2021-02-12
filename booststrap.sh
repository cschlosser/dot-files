#!/bin/bash

script_dir=$(cd "$(dirname "$0")"; pwd)

install_cmd=$("$script_dir"/gen_install.py | tail -n 1)
echo "Package installation script generated"
echo "Do you want to install the packages now? (y/N)"
read -n1 install_now

if [ "$install_now" == "y" ];then
    sudo ${install_cmd}
else
    echo -e "\nOk. You can still do this later by calling:"
    echo "$install_cmd"
    echo "If you want to generate the file again call $script_dir/gen_install.py"
fi

cfg_cmd=$("$script_dir"/gen_cfg.py | tail -n 1)
echo "Config linking script generated"
echo "Do you want to link the configs now? (y/N)"                              
read -n1 configure_now                            
                                        
if [ "$configure_now" == "y" ];then
    ${cfg_cmd}         
else                                                      
    echo -e "\nOk. You can still do this later by calling:"         
    echo "$cfg_cmd"
    echo "If you want to generate the file again call $script_dir/gen_cfg.py"
fi

