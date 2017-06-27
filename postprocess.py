import sys

filename = sys.argv[1]
original_file = sys.argv[2]
unique_names = []
original_names = []

with open(original_file) as ogfile:
	for name in ogfile.read().split("\n"):
		original_names.append(name.lower())

with open(filename) as file:
	for name in file.read().split("\n"):
		if name.strip().lower() not in original_names:
			unique_names.append(name.strip())
	file.close()

with open(filename, "w+") as file:
	for name in set(unique_names):
		file.write(name.title() + "\n")

