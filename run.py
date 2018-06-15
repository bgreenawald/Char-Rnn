# Driver program, replaces previous Powershell and shell options

import os
import argparse

def main():
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

    # Call the model runner
    command = "python char-rnn-model.py -f {0} -e {1} -hi {2} -d {3} -b {4} -s {5} -n {6}"\
                    .format(filename, epochs, hidden, dropout, batch, seq, nodes)
    print(command)
    os.system(command)

    # Call the model generator
    os.system("python char-rnn-pred.py {0} {1} {2}".format(filename, hidden, nodes))

    # Call the postprocessor
    os.system("python postprocess.py {0}".format(filename))

# Runner
if __name__=="__main__":
    main()
