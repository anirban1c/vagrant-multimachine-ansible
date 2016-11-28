import os
import sys
import nose
import requests

TIMEOUT = 0.5

def test_http_get_web_hosts():
	response = requests.get('http://web1.dev', timeout=TIMEOUT)
	assert response.status_code is 200, 'Error %s ' % response.status_code


def test_http_get_app_hosts():
	response = requests.get('http://app1.dev:8080', timeout=TIMEOUT)
	assert response.status_code is 200, 'Error %s ' % response.status_code

	response = requests.get('http://app2.dev:8080', timeout=TIMEOUT)
	assert response.status_code is 200, 'Error %s ' % response.status_code


