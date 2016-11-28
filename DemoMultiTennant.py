import os
import sys
from flask import Flask
from flask import render_template, redirect, url_for, request, jsonify
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, InputRequired
from flask_debugtoolbar import DebugToolbarExtension
import requests
import subprocess

global app

app = Flask(__name__)
app.secret_key = 'sdf345rg5'
app.debug = True
toolbar = DebugToolbarExtension(app)



class AForm(Form):
	name = StringField('Name', [InputRequired()])
	address = StringField('Name', [InputRequired()])
	email = StringField('Email', validators=[DataRequired(),
											 Email()])




@app.route('/status', methods=["GET", "POST"])
def get_server_status():
	state = {}
	memory = subprocess.check_output(['free',
									  '-m',
									  '-t',
									  '-o']).decode('utf-8').split('\n')[1]

	swap =  subprocess.check_output(['free',
									 '-m',
									 '-t',
									 '-o']).decode('utf-8').split('\n')[-2]

	state.update({'host-build': open('/etc/lsb-release', 'r').read().split('\n')})
	state.update({'uptime' : subprocess.check_output(['uptime', '-p']).decode('utf-8').split('\n')[0]})
	state.update({'uname' : subprocess.check_output(['uname', '-a']).decode('utf-8').split('\n')[0]})
	state.update({'memory' : memory })
	state.update({'swap' : swap })
	state.update({'ip_eth0' : subprocess.check_output(['ifconfig',
										'eth0']).decode('utf-8').split('\n')[1].strip()})
	state.update({'ip_eth1' : subprocess.check_output(['ifconfig',
												  'eth1']).decode('utf-8').split('\n')[1].strip()})
	state.update({'ip_routes': subprocess.check_output(['routel']).decode('utf-8').split('\n')[1:-2]})
	state.update({'hostname': subprocess.check_output(['hostname']).decode('utf-8').split('\n')[0]})
	state.update({'vmstate': subprocess.check_output(['vmstat']).decode('utf-8').split('\n')[-2]})

	state.update({'disks': subprocess.check_output(['df', '-H']).decode('utf-8').split('\n')[1:-2]})

	state.update({'proc_python': [x for x in subprocess.check_output(['ps',
					'-auxf']).decode('utf-8').split('\n') if 'python' in x]})

	state.update({'proc_java': [x for x in subprocess.check_output(['ps',
																	  '-auxf']).decode('utf-8').split('\n') if 'java' in x]})

	state.update({'proc_gunicorn': [x for x in subprocess.check_output(['ps',
																	  '-auxf']).decode('utf-8').split('\n') if 'gunicorn' in x]})


	state.update({'proc_nginx': [x for x in subprocess.check_output(['ps',
																		'-auxf']).decode('utf-8').split('\n') if 'nginx' in x]})

	state.update({'proc_supervisord': [x for x in subprocess.check_output(['ps',
																	 '-eaf']).decode('utf-8').split('\n') if 'supervisord.conf' in x]})

	state.update({'listeners_8080': [x for x in subprocess.check_output(['netstat',
																		   '-an']).decode('utf-8').split('\n') if '8080' in x]})

	state.update({'listeners_all_public': [x for x in subprocess.check_output(['netstat',
																		 '-an']).decode('utf-8').split('\n') if '0.0.0.0' in x]})

	state.update({'listeners_all_localhost': [x for x in subprocess.check_output(['netstat',
																			   '-an']).decode('utf-8').split('\n') if '127.0.0.1' in x]})


	return jsonify(dict(sysstats=state))

@app.route('/getRoadClosuers', methods=["GET", "POST"])
def get_road_clousers():
	#road = request.args.get('road', 'M25', type=str) or request.form['road']
	road = request.form['road']

	ret = requests.get('http://data.gov.uk/data/api/service/transport/planned_road_works/road?road=%s' % road)
	app.logger.debug('got args %s ' % road)
	app.logger.debug('response %s ' % ret.json())
	return jsonify(ret.json())


@app.route('/', methods=["GET", "POST"])
def get_going():
		info = os.environ
		error = None
		form = AForm()
		app.logger.debug('Form submitted')

		if form.validate_on_submit():
			name = form.name
			app.logger.debug('Form validated')
			return render_template(url_for('index'), name=name)
		else:
			error = ' something wrong here	'
		return render_template('index.html', info=info, form=form, error=error)


if __name__ == '__main__':
	app.run()
