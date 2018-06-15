from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import string

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

def religious_texts():
	bible_text = ""
	with open("data\\bible.txt") as bible:
		bible_text = bible.read()
		bible.close()

	bible_text = bible_text.replace("\n\n\n\n", "\n").replace("\n\n\n", "\n")
	bible_text = re.sub(r'\d+', '', bible_text)
	bible_text = re.sub(r':+', '', bible_text)
	with open("data\\bible_edit.txt", "w+") as bible:
		bible.write(bible_text)

def band_names():
	# Get the weird band names
	page = requests.get("http://brightlightsfilm.com/weirdbandnames/#.Wx1OFUgvxPY")
	soup = BeautifulSoup(page.text, 'html.parser')

	# Extract out the band names
	all_names = []
	names = soup.find_all(class_="bandname")
	# remove_bad_chars = re.compile("[^a-zA-Z ]")
	remove_multiple_spaces = re.compile("[\n ]+")

	# Iterate over the names
	for name in names:

		name_find = name.find('a')
		if name_find:
			name = name_find.contents[0].strip()
		else:
			name = name.contents[0].strip()
		name = remove_multiple_spaces.sub(' ', name.lower())
		name = remove_multiple_spaces.sub(' ', name.lower())
		all_names.append(name)

	# Read in the names from Wikipedia
	page = requests.get("https://en.wikipedia.org/wiki/List_of_band_name_etymologies")
	soup = BeautifulSoup(page.text, 'html.parser')

	# Extract out the band names
	for elem in soup.find_all("b"):
		elem = elem.find('a')
		if elem:
			elem = elem.contents[0]
			if elem != "^":
				elem = remove_multiple_spaces.sub(' ', elem.strip())
				elem = remove_multiple_spaces.sub(' ', elem.strip())
				all_names.append(elem.lower())


	# Read in the pitchfork data
	pitchfork = pd.read_csv("data/bands.csv")
	for x in list(pitchfork.iloc[:,2]):
		all_names.append(x)

	"""
	# Remove non-printible characters from all names and remove duplicates
	printable = set(string.printable)
	for i, s in enumerate(all_names):
		try:
			all_names[i] = s.filter(lambda x: x in printable)
		except:
			print(s)
	"""

	# Write the results to a file
	ret = ""
	for band in set(all_names):
		try:
			ret += band.encode("ascii", errors="ignore").decode() + "\n"
		except:
			print(band)

	with open("data/band_names.txt", 'w+') as file:
		file.write(ret)
		file.close()


def pornstar_names():
	page = requests.get("http://www.pornolaba.com/pornstars.html")
	soup = BeautifulSoup(page.content, 'html.parser')

	all_names = []
	remove_digits = re.compile("[0-9]+")
	for elem in soup.find_all("li"):
		e = elem.find("a")
		if e:
			e = re.sub(remove_digits, '', e.contents[0])
			e = e.strip().lower()
			all_names.append(e)

	with open("data/pornstar_names.txt", "w+") as file:
		print(len(all_names))
		file.write('\n'.join(all_names))
		file.close()

def main():
	pornstar_names()

if __name__=="__main__":
	main()