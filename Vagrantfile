###
### Vagrantfile used to set up a machine and provision it with Ansible.
### To learn more about Vagrantfile, consult https://developer.hashicorp.com/vagrant/docs/vagrantfile
###
### Author: Daiane A Fraga
### Date: 18-03-2024
###

# Set Vagrant version requirement
Vagrant.require_version ">= 2.0.0"

# This is the version of the configuration object
VAGRANT_CONFIG_VERSION = "2"

# Using a Bento Project's box:
#   https://app.vagrantup.com/bento/boxes/ubuntu-22.04/versions/202401.31.0

# Base box name
BASE_BOX_NAME = "bento/ubuntu-22.04"
# Base box version
BASE_BOX_VERSION = "202401.31.0"

# Here we define our configuration block...
Vagrant.configure(VAGRANT_CONFIG_VERSION) do |config|
    # https://developer.hashicorp.com/vagrant/docs/vagrantfile/machine_settings

    # Set base box to create the machine
    config.vm.box = BASE_BOX_NAME
    config.vm.box_version = BASE_BOX_VERSION

    # https://developer.hashicorp.com/vagrant/docs/providers
    # Configure VirtualBox as provider
    config.vm.provider "virtualbox" do |vbox|
        # https://developer.hashicorp.com/vagrant/docs/providers/virtualbox/configuration

        # Virtual Machine name to appear in the VirtualBox GUI
        vbox.name = "ubuntu-22.04-docker-25.0.4"
        # Skip the guest additions check that is enabled by default
        vbox.check_guest_additions = false
    end

    # https://developer.hashicorp.com/vagrant/docs/provisioning
    # Configure Ansible as provisioner
    config.vm.provision "ansible" do |ansible|
        # Set the relative path to the playbook file
        ansible.playbook = "provisioning/playbook.yml"
        # Ansible will prompt for a password to decrypt files using Ansible Vault
        ansible.ask_vault_pass = true
        # Set the minimal version of Ansible to be supported here
        ansible.compatibility_mode = "2.0"
        # Set the relative path to the requirements file
        # (it allows to install collections and roles from Ansible Galaxy
        # before executing Playbooks)
        ansible.galaxy_role_file = "provisioning/requirements.yml"
    end
end
