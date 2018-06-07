# Char Rnn

This is an implemenation of a text predicting recurrent neural network with Windows tools to assist the process. The model is based on the model from Jason Brownlee, found here (https://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/).

To run this model, simply put a file containing the input strings as a text file, one per line, in the "data" directory. Then, run `.\run.ps1 "data/name_of_file.txt" number-of-epochs`. After the model is complete, the generated results will exist in "data/name_of_file_generated.txt" and some analysis of the results will exist on "data/name_of_file_similarity.txt".