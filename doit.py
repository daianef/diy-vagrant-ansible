#!/usr/bin/env python3
'''
This script works as a wrapper for the commands used in this project.
You can run it directly, modify it, or import it in your own scripts.

Author: Daiane A Fraga
Date: 19-03-2024
'''

import argparse
from subprocess import run
from os.path import realpath, join


# Base utility commands
ANSIBLE_LINT_CMD = ['ansible-lint']
ANSIBLE_VAULT_CMD = ['ansible-vault']
VAGRANT_DESTROY_CMD = ['vagrant', 'destroy']
VAGRANT_REPROVISION_CMD = ['vagrant', 'provision']
VAGRANT_SSH_CMD = ['vagrant', 'ssh']
VAGRANT_STATUS_CMD = ['vagrant', 'status']
VAGRANT_UP_CMD = ['vagrant', 'up']
VAGRANT_VALIDATE_CMD = ['vagrant', 'validate']


##### Useful functions #####


def run_cmd_and_exit(cmd, workdir=None):
    '''Run a command, wait for it to complete and exit.
    Command can be interactive or non-interactive.

    cmd - list of command and arguments to run
    workdir - (optional) change to workdir before executing the command
    '''
    run(cmd, check=True, cwd=workdir)


def validate(vagrantfile_path, playbook_path, **kwargs):
    '''Perform validations of Vagrantfile and Ansible Playbooks.

    vagrantfile_path - path to Vagrantfile
                       (vagrant commands must be run where Vagrantfile is)
    playbook_path - path to the playbook file
    '''
    validate_vagrant(vagrantfile_path)
    validate_ansible(playbook_path)


##### Vagrant functions #####
# Define here other useful functions for vagrant


def validate_vagrant(vagrantfile_path, **kwargs):
    '''Validate Vagrantfile using the "vagrant validate" command.

    vagrantfile_path - path to Vagrantfile
                       (vagrant commands must be run where Vagrantfile is)
    '''
    run_cmd_and_exit(VAGRANT_VALIDATE_CMD, workdir=vagrantfile_path)


def setup(vagrantfile_path, playbook_path, **kwargs):
    '''Call vagrant to set up a virtual machine, using Ansible to provision it.
    It assumes Vagranfile is configured with the Ansible provisioner.
    Perform some validations before calling vagrant.

    vagrantfile_path - path to Vagrantfile
                       (vagrant commands must be run where Vagrantfile is)
    playbook_path - path to the playbook file
    '''
    validate(vagrantfile_path, playbook_path)
    run_cmd_and_exit(VAGRANT_UP_CMD, workdir=vagrantfile_path)


def status(vagrantfile_path, **kwargs):
    '''Show the status of virtual machine created by Vagrant.

    vagrantfile_path - path to Vagrantfile
                       (vagrant commands must be run where Vagrantfile is)
    '''
    run_cmd_and_exit(VAGRANT_STATUS_CMD, workdir=vagrantfile_path)


def enter(vagrantfile_path, **kwargs):
    '''Open an SSH connection to a previously created VM.

    vagrantfile_path - path to Vagrantfile
                       (vagrant commands must be run where Vagrantfile is)
    '''
    run_cmd_and_exit(VAGRANT_SSH_CMD, workdir=vagrantfile_path)


def reprovision(vagrantfile_path, playbook_path, **kwargs):
    '''Call ansible to provision the machine again.
    Perform some validations before calling vagrant.

    vagrantfile_path - path to Vagrantfile
                       (vagrant commands must be run where Vagrantfile is)
    playbook_path - path to the playbook file
    '''
    validate(vagrantfile_path, playbook_path)
    run_cmd_and_exit(VAGRANT_REPROVISION_CMD, workdir=vagrantfile_path)


def destroy(vagrantfile_path, **kwargs):
    '''Destroy a VM created by Vagrant.

    vagrantfile_path - path to Vagrantfile
                       (vagrant commands must be run where Vagrantfile is)
    '''
    run_cmd_and_exit(VAGRANT_DESTROY_CMD, workdir=vagrantfile_path)


##### Ansible functions #####
# Define here other useful functions for ansible


def validate_ansible(playbook_path, **kwargs):
    '''Validate a Ansible Playbook file using ansible-lint.
    It does not access encrypted values (Vault).

    playbook_path - path to the playbook file
    '''
    cmd = ANSIBLE_LINT_CMD + [playbook_path]
    run_cmd_and_exit(cmd)


def encrypt_vault(vault_file_path, **kwargs):
    '''Encrypt a file with ansible-vault.
    It will request you a password.

    vault_file_path - absolute or relative path to the file
    '''
    cmd = ANSIBLE_VAULT_CMD + ['encrypt', vault_file_path]
    run_cmd_and_exit(cmd)


def edit_vault(vault_file_path, **kwargs):
    '''Edit a file encrypted by ansible-vault.
    It will request you a password.

    vault_file_path - absolute or relative path to the file
    '''
    cmd = ANSIBLE_VAULT_CMD + ['edit', vault_file_path]
    run_cmd_and_exit(cmd)


def view_vault(vault_file_path, **kwargs):
    '''Open and show a file encrypted by ansible-vault.
    It will request you a password.

    vault_file_path - absolute or relative path to the file
    '''
    cmd = ANSIBLE_VAULT_CMD + ['view', vault_file_path]
    run_cmd_and_exit(cmd)


def rekey_vault(vault_file_path, **kwargs):
    '''Change the key used to encrypt a file using ansible-vault.
    It will request you two passwords: the old password and the new one.

    vault_file_path - absolute or relative path to the file
    '''
    cmd = ANSIBLE_VAULT_CMD + ['rekey', vault_file_path]
    run_cmd_and_exit(cmd)


##### Argument Parser functions #####


def add_argument_vagrantfile(parser):
    default_vagrantfile_path = realpath('.')
    parser.add_argument(
        '--vagrantfile-path', '-f', type=str, default=default_vagrantfile_path,
        help='Path to Vagrantfile. Default is the current directory.'
    )


def add_argument_playbook(parser):
    # Default path to the playbook is provisioning/playbook.yml in the current dir
    default_vagrantfile_path = realpath('.')
    default_playbook_path = join(
        default_vagrantfile_path, 'provisioning', 'playbook.yml'
    )
    parser.add_argument(
        '--playbook-path', '-p', type=str, default=default_playbook_path,
        help=f'Path to the playbook file. Default is {default_playbook_path}.'
    )


def add_argument_vault_file(parser):
    parser.add_argument(
        '--vault-file-path', '-f', type=str, required=True,
        help='Path to file to be encrypted/descrypted using ansible-vault.'
    )


def add_subparser_to_vagrant_command(
    subparsers, name, description, include_playbook=False
):
    parser = subparsers.add_parser(
        name, help=description, description=description
    )
    add_argument_vagrantfile(parser)

    if include_playbook:
        add_argument_playbook(parser)

    return parser

    parser_edit_vault = add_subparser_to_vault_command(
        subparsers, 'edit_vault', desc
    )


def add_subparser_to_vault_command(
    subparsers, name, description
):
    parser = subparsers.add_parser(
        name, help=description, description=description
    )
    add_argument_vault_file(parser)

    return parser


def create_subparsers(subparsers):
    # Task: vagrant up
    desc = f'Create and provision a virtual machine '
    desc += f'({" ".join(VAGRANT_UP_CMD)}).'
    add_subparser_to_vagrant_command(
        subparsers, 'setup', desc, include_playbook=True
    )

    # Task: vagrant status
    desc = 'Show the status of virtual machine '
    desc += f'({" ".join(VAGRANT_STATUS_CMD)}).'
    add_subparser_to_vagrant_command(
        subparsers, 'status', desc
    )

    # Task: vagrant ssh
    desc = 'Open an SSH connection to virtual machine '
    desc += f'({" ".join(VAGRANT_SSH_CMD)}).'
    add_subparser_to_vagrant_command(
        subparsers, 'enter', desc
    )

    # Task: vagrant provision
    desc = '(Re)Provision an existing virtual machine '
    desc += f'({" ".join(VAGRANT_REPROVISION_CMD)}).'
    add_subparser_to_vagrant_command(
        subparsers, 'reprovision', desc, include_playbook=True
    )

    # Task: vagrant destroy
    desc = 'Destroy running virtual machine '
    desc += f'({" ".join(VAGRANT_DESTROY_CMD)}).'
    add_subparser_to_vagrant_command(
        subparsers, 'destroy', desc
    )

    # Task: vagrant validate + ansible-lint
    desc = 'Validate Vagrantfile and Ansible Playbook.'
    add_subparser_to_vagrant_command(
        subparsers, 'validate', desc, include_playbook=True
    )

    # Task: vagrant validate
    desc = 'Validate Vagrantfile '
    desc += f'({" ".join(VAGRANT_VALIDATE_CMD)}).'
    add_subparser_to_vagrant_command(
        subparsers, 'validate_vagrant', desc
    )

    # Task: ansible-lint
    desc = 'Validate Ansible Playbook '
    desc += f'({" ".join(ANSIBLE_LINT_CMD)}).'
    parser = subparsers.add_parser(
        'validate_playbook', help=desc, description=desc,
    )
    add_argument_playbook(parser)

    # Task: ansible-vault encrypt
    desc = 'Encrypt a file with Ansible Vault '
    desc += f'({" ".join(ANSIBLE_VAULT_CMD)}).'
    add_subparser_to_vault_command(
        subparsers, 'encrypt_vault', desc
    )

    # Task: ansible-vault edit
    desc = 'Edit a file encrypted by Ansible Vault '
    desc += f'({" ".join(ANSIBLE_VAULT_CMD)}).'
    add_subparser_to_vault_command(
        subparsers, 'edit_vault', desc
    )

    # Task: ansible-vault view
    desc = 'Show the content of a file encrypted by Ansible Vault '
    desc += f'({" ".join(ANSIBLE_VAULT_CMD)}).'
    add_subparser_to_vault_command(
        subparsers, 'view_vault', desc
    )

    # Task: ansible-vault rekey
    desc = 'Change the key used to encrypt a file using Ansible Vault '
    desc += f'({" ".join(ANSIBLE_VAULT_CMD)}).'
    add_subparser_to_vault_command(
        subparsers, 'rekey_vault', desc
    )


##### Main function #####


def main():
    '''Main function parses command line and other call functions'''

    # https://docs.python.org/3/library/argparse.html#module-argparse
    parser = argparse.ArgumentParser(
        description='Do It: a wrapper for some Vagrant and Ansible commands.'
    )

    # Create subparsers for each task
    # https://docs.python.org/3/library/argparse.html#sub-commands
    subparsers = parser.add_subparsers(
        title='Subcommands',
        help='Choose one subcommand to perform the action.',
        dest='subcommand'
    )
    create_subparsers(subparsers)

    # Parse arguments and return a Namespace object
    # https://docs.python.org/3/library/argparse.html#the-parse-args-method
    args = parser.parse_args()

    if args.subcommand is None:
        parser.error('You must choose a subcommand!')

    # Put all arguments into a dictionary
    all_arguments = vars(args)

    try:
        # Try to call the function related to the chosen task
        eval(f'{args.subcommand}(**all_arguments)')
    except NameError:
        parser.error(
            f'Subcommand {args.subcommand} has not been implemented yet.')


if __name__ == "__main__":
    main()
