#!/bin/bash

####################################################
# Cephutils  Setup:
# The setup script will pull ansible stable-1.9 label
# and set the correct environment variables for this
# module to be self contained.
# --------------------------------------------------
####################################################

setup_logs="/tmp/setup.log_"`date +"%b%d%y_%H%M%S"`

ansible_repo="http://github.com/ansible/ansible.git"
ansible_branch="stable-1.9"
ansible_destdir="../ansible_stable1.9"

cephutils_dir=$(pwd)
root_dir=${cephutils_dir%/*}                                                                                                                                                                      

ansible_path="${root_dir}/ansible_stable1.9"

###########################################
# The function does git pull if the dest 
# directory doesn't already exist.
# Args:
# $1 - git repo
# $2 - destination directory
# $3 - branch
############################################
function git_pull () 
{
    gitrepo=$1
    localgitrepo=$2
    branch=$3

    if [[ ! -z $branch ]]; then
        branch="-b $branch"
    fi

    echo -n "pulling repo: [$gitrepo]  "
    if [[ ! -d $localgitrepo ]]; then 
        echo "Pulling $gitrepo $branch" >> $setup_logs 2>&1
        git clone $gitrepo $branch $localgitrepo >>  $setup_logs 2>&1
    fi

    if [[ -d $localgitrepo ]]; then
        echo " ---> [DONE]"
    else
        echo " ---> [FAILED]";echo
        echo "Error logs: $setup_logs"
    fi
}

export ANSIBLE_HOST_KEY_CHECKING=False

# Pull repositories.
git_pull ${ansible_repo} ${ansible_destdir} ${ansible_branch}
# Add the Ansible submodules
cd ${ansible_path}
git submodule update --init --recursive >> $setup_logs 2>&1
cd ${cephutils_dir}


export ANSIBLE_HOST_KEY_CHECKING=False

###################################################
# Source Ansible Environment
###################################################
source ../ansible_stable1.9/hacking/env-setup


