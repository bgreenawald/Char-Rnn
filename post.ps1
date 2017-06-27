$original=$args[0]
$generated=$args[1]
$weights=$args[2]

For( $i=0; $i -lt 10; $i++) {
    python .\char-rnn-pred.py $original $generated $weights
    python .\postprocess.py $generated $original
}

