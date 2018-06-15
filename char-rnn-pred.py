# Load Larger LSTM network and generate text
import sys
import os
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from tqdm import tqdm

# load ascii text and covert to lowercase
filename = sys.argv[1]
hidden = int(sys.argv[2])
nodes = int(sys.argv[3])

raw_text = open(filename).read()
raw_text = raw_text.lower()

# create mapping of unique chars to integers, and a reverse mapping
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))

# summarize the loaded data
n_chars = len(raw_text)
n_vocab = len(chars)
print("Total Characters: ", n_chars)
print("Total Vocab: ", n_vocab)

# prepare the dataset of input to output pairs encoded as integers
seq_length = 15
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
	seq_in = raw_text[i:i + seq_length]
	seq_out = raw_text[i + seq_length]
	dataX.append([char_to_int[char] for char in seq_in])
	dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print("Total Patterns: ", n_patterns)

# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))

# normalize
X = X / float(n_vocab)

# one hot encode the output variable
y = np_utils.to_categorical(dataY)

# define the LSTM model
model = Sequential()
model.add(LSTM(nodes, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))

for _ in range(hidden - 2):
	model.add(LSTM(nodes, return_sequences=True))

if hidden > 1:
	model.add(LSTM(nodes))
model.add(Dense(y.shape[1], activation='softmax'))

# load the network weights
model.load_weights(os.path.join(os.getcwd(), "models", \
	 os.path.split(filename)[1][:-4] + ".hdf5"))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# Delete write file if it exists
if os.path.exists(filename[:-4] + "-generated.txt"):
	os.remove(filename[:-4] + "-generated.txt")

# Run the generation a number of times with different
# initial seeds
for i in range(5):
	print("Generation iteration " + str(i))
	start = numpy.random.randint(0, len(dataX)-1)
	pattern = dataX[start]
	print("Seed:")
	print("\"", ''.join([int_to_char[value] for value in pattern]), "\"")

	# store a running list of the result
	full_result = ""

	# generate characters
	print("Generating new characters: ")
	for i in tqdm(range(1000)):
		x = numpy.reshape(pattern, (1, len(pattern), 1))
		x = x / float(n_vocab)
		prediction = model.predict(x, verbose=0)
		index = numpy.argmax(prediction)
		result = int_to_char[index]
		seq_in = [int_to_char[value] for value in pattern]
		full_result += result
		pattern.append(index)
		pattern = pattern[1:len(pattern)]

	# split our result into individual names, removing the last
	# one since it may be incomplete
	names = full_result.split("\n")

	# create file for results to be written to
	with open(filename[:-4] + "-generated.txt", "a") as file:
		for name in names:
			file.write(name.title() + "\n")

print("\nDone.")