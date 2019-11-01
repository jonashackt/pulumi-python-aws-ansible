#!/usr/bin/env bash
set -euo pipefail

echo "destroy pre-created Pulumi instances"
pulumi destroy --yes

echo "generate EC2 keypair and save private key locally (since Pulumi isn't able to do that now)"
ansible-playbook keypair.yml

echo "execute Pulumi to create EC2 instances"
pulumi up --yes

echo "Downloading the Ansible role 'docker' with ansible-galaxy"
ansible-galaxy install -r requirements.yml -p roles/

echo "run Ansible role to install Docker on Ubuntu"
ansible-playbook playbook.yml

echo "use Testinfra with Pytest to execute our tests"
py.test -v tests/test_docker.py --ssh-identity-file=.ec2ssh/pulumi_key --ssh-config=tests/pytest_ssh_config --hosts='ssh://'$(pulumi stack output publicIp)
