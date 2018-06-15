import sys
import string
from tqdm import tqdm
import os

from difflib import SequenceMatcher


# Similarity calculator between 2 strings
# From https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings/17388505

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Get only the unique names from the generated set
def uniqueNames(filename, original_file):

	with open(original_file) as ogfile:
		original_names = [x.lower() for x in ogfile.read().split("\n")]
		ogfile.close()

	unique_names = []
	with open(filename) as file:
		for name in file.read().split("\n"):
			if name.strip().lower() not in original_names:
				unique_names.append(name.strip())
		file.close()

	# Write the unique names back to the file
	with open(filename, "w") as file:
		file.write("\n".join(set(unique_names)))
		file.close()

	return original_names, set(unique_names)


# LCS to help find name similiarity
# From https://www.geeksforgeeks.org/longest-common-subsequence/
def lcs(X , Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)

    # declaring the array for storing the dp values
    L = [[None]*(n+1) for i in range(m+1)]

    """Following steps build L[m+1][n+1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j] , L[i][j-1])

    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]

def name_similarity(write_name, unique_names, original_names):

	# Create dict
	lcs_similarity = {}
	seq_similarity = {}
	name_subset = {}
	for name in unique_names:
		lcs_similarity[name] = ""
		seq_similarity[name] = ""
		name_subset[name] = []

	# Run the LCS algorithm to find the most common name
	print("Calculating similarity: ")
	for index, name in tqdm(enumerate(unique_names)):
		max_lcs = 0
		max_lcs_val = ""
		max_sim = 0
		max_sim_val = ""
		for name2 in original_names:
			sim_lcs = lcs(name, name2)
			sim = similar(name, name2)
			if sim_lcs > max_lcs:
				max_lcs = sim_lcs
				max_lcs_val = name2
			if sim > max_sim:
				max_sim = sim
				max_sim_val = name2
			if name in name2 or name2 in name:
				name_subset[name].append(name2)

		lcs_similarity[name] = max_lcs_val
		seq_similarity[name] = max_sim_val

	# Write the results
	with open(write_name, "w+") as write_file:
		write_file.write("For each of the original names, this files finds\n" +
			"the most similiar counterpart in the new names dataset using the LCS algorithm,\n" +
			"a sequence similarity algorithm, and\n" +
			"finding any new names such that the new name is a subset of the original name or\n" +
			"the original name is a subset of the new name.")
		write_file.write("Original Name: New Name (LCS), New Name (Sequence Similarity), [Subset Names]\n")
		for elem in lcs_similarity:
			write_file.write(string.capwords(elem) + ": " \
				+ string.capwords(lcs_similarity[elem]) + ", "
				+ string.capwords(seq_similarity[elem]) + ', [' \
				+ ', '.join([string.capwords(s) for s in name_subset[elem]]) + "]\n")


if __name__=="__main__":

	# Get only the unique set of names
	original_file = sys.argv[1]
	generated_file = original_file[:-4] + "-generated.txt"
	write_file = original_file[:-4] + "-similarity.txt"

	# Delete the similarity file if it exists
	if os.path.exists(write_file):
		os.remove(write_file)

	# Make sure to get only the unique names
	orig, uniq = uniqueNames(generated_file, original_file)

	# Calculate the name similarity
	name_similarity(write_file, orig, uniq)

