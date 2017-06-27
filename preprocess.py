from bs4 import BeautifulSoup
import requests

# Preprocess the boy names
def boy_names():
	url = "https://www.babble.com/pregnancy/1000-most-popular-boy-names/"
	site = requests.get(url)
	soup = BeautifulSoup(site.content, 'html.parser')

	names = list(soup.find_all("li", class_="p1"))
	names = [name.text for name in names]

	with open("boy_names.txt", "w+") as file:
		for name in names:
			file.write(name + "\n")

def girl_names():
	url = "https://www.babble.com/pregnancy/1000-most-popular-girl-names/"
	site = requests.get(url)
	soup = BeautifulSoup(site.content, 'html.parser')

	names = list(soup.find_all("li", class_="p1"))
	names = [name.text for name in names]

	with open("girl_names.txt", "w+") as file:
		for name in names:
			file.write(name + "\n")

def main():
	girl_names()

if __name__=="__main__":
	main()