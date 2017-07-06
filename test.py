import sys

print(sys.argv[1])

with open(sys.argv[1]) as file:
	print(file.read())