# -*- mode: ruby -*-
# # vi: set ft=ruby :

#
# @AnirbanChatterjee
# https://github.com/tanguybernard/vagrant-ansible-multi-machine
# I have these plugins for convenience
# vagrant-hostmanager (1.8.5)
# vagrant-share (1.1.6, system)
# vagrant-triggers (0.5.3)
#
#
#

$install_ansible = <<SCRIPT
#
# install ansible and its dependants
#

if [ $(dpkg-query -W -f='${Status}' ansible 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
	echo "Add APT repositories"
	export DEBIAN_FRONTEND=noninteractive
	apt-get install -qq software-properties-common &> /dev/null || exit 1
	apt-add-repository ppa:ansible/ansible &> /dev/null || exit 1

	apt-get update -qq
	apt-get install -qq git
	echo "Install python-pip"
	apt-get install -qq python3-dev &> /dev/null || exit 1
	apt-get install -qq python3-pip &> /dev/null || exit 1
	apt-get install -qq python-pip &> /dev/null || exit 1
	echo "python3-pip installed"

	echo "Installing Ansible"
	apt-get install -qq ansible &> /dev/null || exit 1
	echo "Ansible installed"
fi

#
# ansible-pull : check celery agent plugin DO NOT RUN without double checking
#
#cd /vagrant/provisioning
#ansible-playbook -vvvv --inventory-file=../hosts appserver.yml --connection=local
SCRIPT


# Specify minimum Vagrant version and Vagrant API version
Vagrant.require_version ">= 1.6.0"
VAGRANTFILE_API_VERSION = "2"
 
# Require YAML module
require 'yaml'
 
# Read YAML file with box details
servers = YAML.load_file(File.join(File.dirname(__FILE__), 'vagrant.yml'))

 
# Create boxes
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    
    

    config.vm.network :forwarded_port, host: 80, guest: 80, auto_correct: true # website
    #config.vm.network :forwarded_port, guest: 3306, host: 3306, auto_correct: true # mysql
    #config.vm.network :forwarded_port, guest: 9000, host: 9000, auto_correct: true # phpmyadmin
    
    #Avoid, prefer using sftp upload via an IDE like phpstorm
    #config.vm.synced_folder "./", "/var/www/html", type: "rsync", id: "vagrant", :nfs => false,
    #    :mount_options => ["dmode=777", "fmode=666"]
    
    
   
    # Iterate through entries in YAML file
    servers.each do |servers|

		# override
    	memory = servers['memory'] ? servers['memory'] : 1024
    	cpus = servers['cpus'] ? servers['cpus'] : 1
    	hostname =  servers['hostname'] ? servers['hostname'] : "test.dev"


		config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"
        config.vm.define servers["name"] do |srv|
            srv.vm.box = servers["box"]
            srv.vm.hostname = hostname
            
            if servers["ip"] != nil
              srv.vm.network "private_network", ip: servers["ip"]
           else
              srv.vm.network :private_network, :auto_network => true
           end
            
            srv.vm.provider :virtualbox do |vb|
                vb.name = servers["name"]
                vb.memory = memory
                vb.cpus = cpus
                vb.gui = false
                vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]

            end
			# just install the min prequisites before we proceed
			srv.vm.provision 'shell', inline: $install_ansible
			# Patch for https://github.com/mitchellh/vagrant/issues/6793
			#srv.vm.provision "shell" do |s|
			#	s.inline = '[[ ! -f $1 ]] || grep -F -q "$2" $1 || sed -i "/__main__/a \\    $2" $1'
			#	s.args = ['/usr/bin/ansible-galaxy', "if sys.argv == ['/usr/bin/ansible-galaxy', '--help']: sys.argv.insert(1, 'info')"]
			#end

            #if servers["prov"] == "ansible"
            srv.vm.provision "ansible" do |ansible|
                    ansible.playbook = "provisioning/"+ servers["prov"] + ".yml"
                    ansible.sudo = true
					ansible.inventory_path = "hosts"
					ansible.verbose = "vv"
					ansible.limit = hostname
            end
        end
    end
    
    #https://github.com/devopsgroup-io/vagrant-hostmanager


    config.hostmanager.enabled = true
    config.hostmanager.manage_host = true
    config.hostmanager.ignore_private_ip = false
    config.hostmanager.include_offline = true

    config.vm.provision :shell, inline: "echo Good job"

end