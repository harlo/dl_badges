#! /bin/bash

function run_docker_routine {
	chmod +x .routine.sh
	./.routine.sh
	rm .routine.sh
	rm Dockerfile
}

function do_exit {
	deactivate venv
	exit
}

# Create virtualenv
virtualenv venv
source venv/bin/activate

# Install python requirements
pip install -r requirements.txt

python dl_badges.py init $1
DID_INIT=$?

if ([ $DID_INIT -eq 0 ])
then
	run_docker_routine
else
	echo "FAILED."
	do_exit
fi

python dl_badges.py build
DID_BUILD=$?

if ([ $DID_BUILD -eq 0 ])
then
	run_docker_routine
else
	echo "FAILED."
	do_exit
fi

python dl_badges.py commit
DID_COMMIT=$?

if ([ $DID_COMMIT -eq 0 ])
then
	run_docker_routine
	echo "OK!"
else
	echo "FAILED."
fi

do_exit