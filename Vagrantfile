# -*- mode: ruby -*-
# vi: set ft=ruby :

# The hypervisors used for this are the HP Z4 G4 Workstations. They have
# one nvme disk wich is used for the SO where an Logical Volume Manager
# (LVM) Physical Disk (PV) is configured. It has also two 4 terabytes
# disks used to compose a mirroed vdev for ZFS filesystem.
#
# Logical Volumes (LVs) are created in the LVM to hold the L2ARC (cache
# device)and SLOG (secondary log device) for ZFS.
#
# To mimic the production environment we will use three virtual disks.
# The first will be used for the LVM (/dev/sdc) and the others for ZFS
# (/dev/sdd and /dev/sde). The disk devices from development are
# different from production.

require "shell"

# The box to be used by Vagrant.
VAGRANT_BOX = "ubuntu/bionic64"

# Number of CPUs allocated to the virtual machine instances.
VM_CPUS = 4

# Total of RAM memory in megabytes allocated to the vm instances.
VM_MEMORY = 4096

# The prefix for the hostname and virtual machine name.
INSTANCE_PREFIX = "hv"

# The prefix for the IP address. The ip address for the machines will be
# generated using the instance index and the prefix. So in the default
# confing it will be 192.168.4.11 for node-1, 192.168.4.12 for node-2
# and so on.
IP_PREFIX = "192.168.4.9"

# The virtual machine name and hostname for the controller machine, the
# one that will provision the other with Ansible (manager). It is useful
# for mixed environments that uses Linux, Windows, etc and makes it
# unecessary to have Ansible installed in the machine running Vagrant.
CONTROLLER_HOSTNAME = "#{INSTANCE_PREFIX}-2"

# The IP address for the controller machine. In the default config it
# will be 192.168.4.10.
CONTROLLER_IP_ADDRESS = "#{IP_PREFIX}2"

# Sets guest environment variables.
# @see https://github.com/hashicorp/vagrant/issues/7015
$set_environment_variables = <<SCRIPT
tee "/etc/profile.d/myvars.sh" > "/dev/null" <<EOF
# Ansible environment variables.
export ANSIBLE_RETRY_FILES_ENABLED=0
EOF
SCRIPT

VAGRANT_ROOT = File.dirname(File.expand_path(__FILE__))

Vagrant.configure("2") do |config|
  config.ssh.insert_key = false
  config.ssh.private_key_path = "./ansible/insecure_private_key"
  config.vm.box = VAGRANT_BOX

  config.vm.define "#{INSTANCE_PREFIX}-1" do |machine|
    machine.vm.provider "virtualbox" do |vbox|
      vbox.name = "#{INSTANCE_PREFIX}-1"
      vbox.memory = VM_MEMORY
      vbox.cpus = VM_CPUS

      # Enable nested virtualization so we are able to rum KVM inside
      # our VirtualBox machine.
      vbox.customize ["modifyvm", :id, "--nested-hw-virt", "on"]

      # Add disks for ZFS setup.
      disk_size_in_mb = 256 * 1024
      disks_total = 3
      for j in 1..disks_total
        file_to_disk = File.join(VAGRANT_ROOT, '.vagrant', "#{INSTANCE_PREFIX}-1-disk-#{j}.vdi")
        unless File.exist?(file_to_disk)
          vbox.customize ['createmedium', 'disk',
            '--filename', file_to_disk,
            '--size', disk_size_in_mb,
            # Not using variant `Fixed` since the size is 256 GB.
            '--variant', 'Standard']
        end
        vbox.customize ['storageattach', :id,
          '--storagectl', 'SCSI',
          '--port', 2 + j - 1,
          '--device', 0,
          '--type', 'hdd',
          '--medium', file_to_disk]
      end
    end
    machine.vm.hostname = "#{INSTANCE_PREFIX}-1"
    # This network will simulate the intranet
    machine.vm.network "private_network", ip: "#{IP_PREFIX}1", mac: "080027fef3c1"
    # This network will simulate the private network
    machine.vm.network "private_network", ip: "192.168.2.161", mac: "080027fef3c2"
  end

  # The controller that will provision other nodes.
  config.vm.define CONTROLLER_HOSTNAME do |machine|
    machine.vm.provider "virtualbox" do |vbox|
      vbox.name = CONTROLLER_HOSTNAME
      vbox.memory = VM_MEMORY
      vbox.cpus = VM_CPUS

      # Enable nested virtualization so we are able to rum KVM inside
      # our VirtualBox machine.
      vbox.customize ["modifyvm", :id, "--nested-hw-virt", "on"]

      # Add disks for ZFS setup.
      disk_size_in_mb = 256 * 1024
      disks_total = 3
      for j in 1..disks_total
        file_to_disk = File.join(VAGRANT_ROOT, '.vagrant', "#{INSTANCE_PREFIX}-2-disk-#{j}.vdi")
        unless File.exist?(file_to_disk)
          vbox.customize ['createmedium', 'disk',
            '--filename', file_to_disk,
            '--size', disk_size_in_mb,
            # Not using variant `Fixed` since the size is 256 GB.
            '--variant', 'Standard']
        end
        vbox.customize ['storageattach', :id,
          '--storagectl', 'SCSI',
          '--port', 2 + j - 1,
          '--device', 0,
          '--type', 'hdd',
          '--medium', file_to_disk]
      end
    end
    machine.vm.hostname = CONTROLLER_HOSTNAME
    # This network will simulate the intranet
    machine.vm.network "private_network", ip: CONTROLLER_IP_ADDRESS, mac: "080027e7345e"
    # This network will simulate the private network
    machine.vm.network "private_network", ip: "192.168.2.162", mac: "080027e7345f"

    # Vault passwords in home dir in order to not leave the key together with
    # the lock (useful to synchronize projects inside Dropbox/Gdrive).
    machine.vm.synced_folder "~/.ansible_secret", \
      "/home/vagrant/.ansible_secret"
    machine.vm.synced_folder "ansible", "/etc/ansible"
    machine.vm.provision "shell", inline: $set_environment_variables, \
      run: "always"
    machine.vm.provision "shell", path: "scripts/bootstrap.sh"
    machine.vm.provision "ansible_local" do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.install = false
      ansible.provisioning_path = "/etc/ansible"
      ansible.playbook = ENV["ANSIBLE_PLAYBOOK"] ? ENV["ANSIBLE_PLAYBOOK"] \
        : "playbook.yml"
      ansible.inventory_path = "hosts-dev.ini"
      ansible.become = true
      ansible.limit = ENV['ANSIBLE_LIMIT'] ? ENV['ANSIBLE_LIMIT'] : "all"
      ansible.vault_password_file = "/home/vagrant/.ansible_secret/vault_pass_insecure"
      ansible.tags = ENV['ANSIBLE_TAGS']
      ansible.verbose = ENV['ANSIBLE_VERBOSE']
    end
  end
end
