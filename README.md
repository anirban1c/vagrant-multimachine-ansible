# vagrant-multimachine-ansible
A vagrant provisioning for multi-machine with ansible


# vagrant host requirements

vagrant -v Vagrant 1.7.1
py3.4 with the following
ansible==2.2.0.0
rednose==1.2.1
requests==2.12.1

# hosts

web1.dev - nginx webserver
app1.dev - appserver
app2.dev - appserver
db1.dev - db server

Add box to ensure faster load times
puppetlabs/ubuntu-14.04-64-nocm (virtualbox, 1.0.3)

