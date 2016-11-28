import os
import sys
import nose
import subprocess
import pprint
import requests
import simplejson as json

TIMEOUT = 0.5


def test_ssh_login_web1():
	resp = subprocess.check_output(['ssh',
								   'vagrant@web1.dev',
								   '-i',
								   '.vagrant/machines/web1/virtualbox/private_key',
								   'hostname -f']).decode('utf-8')
	print(resp)
	assert 'web1.dev' in resp, 'Something wrong here '

def test_ssh_login_app1():
	resp = subprocess.check_output(['ssh',
								   'vagrant@app1.dev',
								   '-i',
								   '.vagrant/machines/app1/virtualbox/private_key',
								   'hostname -f']).decode('utf-8')
	assert 'app1.dev' in resp, 'Something wrong here '

def test_ssh_login_app2():
	resp = subprocess.check_output(['ssh',
								   'vagrant@app2.dev',
								   '-i',
								   '.vagrant/machines/app2/virtualbox/private_key',
								   'hostname -f']).decode('utf-8')
	assert 'app2.dev' in resp, 'Something wrong here '

def test_ssh_check_nginx_web1():
	resp = subprocess.check_output(['ssh',
									'vagrant@web1.dev',
									'-i',
									'.vagrant/machines/web1/virtualbox/private_key',
									'ps -eaf | grep nginx']).decode('utf-8')
	assert 'nginx: master proces' in resp, 'Something wrong here '

def test_http_get_web_hosts():
	response = requests.get('http://web1.dev', timeout=TIMEOUT)
	assert response.status_code is 200, 'Error %s ' % response.status_code


def test_http_get_app_hosts():
	response = requests.get('http://app1.dev:8080', timeout=TIMEOUT)
	assert response.status_code is 200, 'Error %s ' % response.status_code

	response = requests.get('http://app2.dev:8080', timeout=TIMEOUT)
	assert response.status_code is 200, 'Error %s ' % response.status_code

def test_http_get_web_hosts():
	response = requests.get('http://web1.dev', timeout=TIMEOUT)
	assert response.status_code is 200, 'Error %s ' % response.status_code


def test_loadbalancing():
	response1 = requests.get('http://web1.dev/status', timeout=TIMEOUT)
	response2 = requests.get('http://web1.dev/status', timeout=TIMEOUT)

	h1 = json.loads(response1.content.decode('utf-8'))['sysstats']['hostname']
	h2 =  json.loads(response2.content.decode('utf-8'))['sysstats']['hostname']

	assert 'app1' in [h1, h2]
	assert 'app2' in [h1, h2]

def test_app_processes_running():
	response1 = requests.get('http://web1.dev/status', timeout=TIMEOUT)
	response2 = requests.get('http://web1.dev/status', timeout=TIMEOUT)

	h1 = len(json.loads(response1.content.decode('utf-8'))['sysstats']['proc_python'])
	h2 =  len(json.loads(response2.content.decode('utf-8'))['sysstats']['proc_python'])

	assert 0 not in [h1, h2]
	assert 0 not in [h1, h2]

