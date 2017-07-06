#!/bin/bash

python char-rnn-model.py "$1"

git add . 
git commit -m "$2"
git push
