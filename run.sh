MODEL="ngram"
DATA="data/raw/python/poison_set.json"
# DATA="data/raw/python/raw_test_python.jsonl"
# DATA="/home/david/ymz/CodeNaturalness/data/rw/defect-detection/test.tsv"
# DATA="/home/david/ymz/CodeNaturalness/data/clean/defect-detection/test.tsv"
# DATA="data/raw/python/rb-xt-il-xte_function_definition-parameters-default_parameter-typed_parameter-typed_default_parameter-assignment-ERROR_file_100_1_train.txt"
TASK="codesearch"
TOKENIZER="codellama"

python3 main.py -m $MODEL \
-t $DATA \
-n $TASK \
-tk $TOKENIZER