SHELL=/bin/sh

source:
	source     ~/envs/appunto/bin/activate
run:
	virtualenv --python python3 \
    	~/envs/appunto	
	pip install -r requirements.txt
	python main.py