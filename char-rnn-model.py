# Larger LSTM Network to Generate Text for Alice in Wonderland
import numpy
import sys
import os
import argparse
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.utils import np_utils

# Create the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filename", required=True,
		help="name of the data file")
ap.add_argument("-e", "--epochs", required=False, default=10,
		help="number of epochs for the hidden layer")
ap.add_argument("-hi", "--hidden", required=False, default=3,
		help="number of hidden layers")
ap.add_argument("-d", "--dropout", required=False, default=0.3,
		help="dropout")
ap.add_argument("-b", "--batch", required=False, default=512,
		help="batch size")
ap.add_argument("-s", "--sequence", required=False, default=15,
		help="sequence length")
ap.add_argument("-n", "--nodes", required=False, default=256,
		help="number of nodes per hidden layer")

# Read in command line arguments
args = vars(ap.parse_args())
filename = args["filename"]
epochs = max(int(args["epochs"]), 1)
hidden = max(int(args["hidden"]), 1)
dropout = float(args["dropout"])
batch = int(args["batch"])
seq = max(int(args["sequence"]), 1)
nodes = max(int(args["nodes"]), 1)

# load ascii text and covert to lowercase
raw_text = open(filename).read()
raw_text = raw_text.lower()

# create mapping of unique chars to integers
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))

# summarize the loaded data
n_chars = len(raw_text)
n_vocab = len(chars)
print("Total Characters: ", n_chars)
print("Total Vocab: ", n_vocab)

# prepare the dataset of input to output pairs encoded as integers
seq_length = seq
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
model.add(Dropout(dropout))

for _ in range(hidden - 2):
	model.add(LSTM(nodes, return_sequences=True))
	model.add(Dropout(dropout))
if hidden > 1:
	model.add(LSTM(nodes))
	model.add(Dropout(dropout))
model.add(Dense(y.shape[1], activation='softmax'))
# model.load_weights("models\\boy_weights.hdf5")
model.compile(loss='categorical_crossentropy', optimizer='adam')

# define the checkpoint
filepath=os.path.join(os.getcwd(), "models", \
	 os.path.split(filename)[1][:-4] + ".hdf5")
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
checkpoint2 = EarlyStopping(monitor='loss', min_delta=0, patience=2, verbose=0, mode='auto')

callbacks_list = [checkpoint, checkpoint2]

# fit the model
model.fit(X, y, epochs=epochs, batch_size=256, \
	callbacks=callbacks_list, shuffle=True)
