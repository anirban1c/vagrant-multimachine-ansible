# vagrant-multimachine-ansible
A vagrant provisioning for multi-machine with ansible


### vagrant host requirements

vagrant -v Vagrant 1.7.1
py3.4 with the following
ansible==2.2.0.0
rednose==1.2.1
requests==2.12.1

### hosts

web1.dev - nginx webserver
app1.dev - appserver
app2.dev - appserver

1. Add box to ensure faster load times
    puppetlabs/ubuntu-14.04-64-nocm (virtualbox, 1.0.3)
3. Edit the ip to your hosts correct submit - 198.162.1.xxx
2. Bringing up all the servers
    vagrant up web1
    vagrant up app1
    vagrant up app2
3. Test from the host
    nosetests -v --rednose
4. If everything works and no errors
     A sample application to get all the road works by road name
     http://web1.dev
5. Few basic server stats are also available at http://web1.dev/status

