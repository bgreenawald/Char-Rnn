# Read in the parameters
$original=$args[0] # Filepath of original dataset
$epochs=$args[1] # Number of epochs

# Run the neural network model
python .\char-rnn-model.py $original $epochs

# Run the predictions
python .\char-rnn-pred.py $original

# Run postprocessing on the results
python .\postprocess.py $original

