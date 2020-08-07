SHELL=/bin/sh

source:
	source     ~/envs/appunto/bin/activate
run:
	virtualenv --python python3 \
    	~/envs/appunto	
	pip install -r requirements.txt
	python main.py

gce:
	gcloud app create
	gcloud app deploy app.yaml \
		--project app-puntos-285220
gcd:
	gcloud app deploy app.yaml \
		--project app-puntos-285220