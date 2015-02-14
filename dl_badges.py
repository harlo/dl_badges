from sys import argv, exit

def init_d(with_config):
	return False

def build_d():
	return False

def commit_d():
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