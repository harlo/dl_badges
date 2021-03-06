import json, os
from sys import argv, exit

from dutils.conf import DUtilsKey, DUtilKeyDefaults, BASE_DIR
from dutils.funcs import build_config, append_to_config, save_config, build_dockerfile

APP_PORT = 8080
API_PORT = 8888

EXPOSE_PORTS = [APP_PORT, API_PORT]

def init_d(with_config):
	conf_keys = [
		DUtilKeyDefaults['USER'],
		DUtilKeyDefaults['USER_PWD'],
		DUtilKeyDefaults['IMAGE_NAME']
	]

	config = build_config(conf_keys, with_config)
	
	from dutils.funcs import get_docker_exe
	
	docker_exe = get_docker_exe()
	if docker_exe is None:
		return False

	save_config(config)
	res, config = append_to_config({
		'STUB_IMAGE' : "%s:init" % config['IMAGE_NAME'],
		'DOCKER_EXE' : docker_exe,
		'EXPOSE_PORTS' : " ".join(EXPOSE_PORTS)
	}, return_config=True)

	if not res:
		return False

	from dutils.funcs import generate_init_routine, build_bash_profile

	if build_dockerfile("Dockerfile.init", config) and generate_init_routine(config):
		del config['USER_PWD']

		directives = [
			"export APP_PORT=%d" % APP_PORT,
			"export API_PORT=%d" % API_PORT,
			"export PKG_CONFIG_PATH=/usr/X11/lib/pkgconfig"
		]

		return (save_config(config) and build_bash_profile(directives, dest_d=os.path.join(BASE_DIR, "src")))
	
	return False

def build_d():
	from dutils.funcs import generate_build_routine

	res, config = append_to_config({
		'FINAL_IMAGE' : "%s:latest" % config['IMAGE_NAME']
		}, return_config=True)

	return (build_dockerfile("Dockerfile.commit", config) and generate_build_routine(config, "dl_badges"))

def commit_d():
	from sys import stdin

	try:
		port_bindings = json.loads(stdin.read())[0]['HostConfig']['PortBindings']
		print port_bindings
	except Exception as e:
		print e, type(e)
		return False

	try:
		res, config = append_to_config({
			'APP_PORT' : int(port_bindings['%d/tcp' % APP_PORT][0]['HostPort']),
			'API_PORT' : int(port_bindings['%d/tcp' % API_PORT][0]['HostPort'])
			}, return_config=True)

		if not res:
			return False

		routine = [
			"sudo %(DOCKER_EXE)s rm %(IMAGE_NAME)s"
		]

		return build_routine([r % config for r in routine])

	except Exception as e:
		print e, type(e)

	return False

def update_d():
	return False

if __name__ == "__main__":
	res = False

	if argv[1] == "init":
		res = init_d(None if len(argv) == 2 else argv[2])
	elif argv[1] == "build":
		res = build_d()
	elif argv[1] == "commit":
		res = commit_d()
	elif argv[1] == "update":
		res = update_d()
	
	exit(0 if res else -1)