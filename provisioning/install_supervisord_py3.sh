!#/bin/sh


. "{{ venv_dir }}"/bin/activate && git clone https://github.com/Supervisor/supervisor.git && cd supervisor && pip install -e .