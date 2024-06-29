import torch


BASE_DIR = "/home/david/ymz/models/"
#Model version:
_MODEL_VERSION = {
                    "gptneo": BASE_DIR + "EleutherAI/gpt-neo-2.7B",
                    "codellama": BASE_DIR + "codellama/CodeLlama-7b-hf",
                    "bloom": BASE_DIR + "bigscience/bloomz-7b1",
                    "codellama13": BASE_DIR + "codellama/CodeLlama-13b-hf",
                    "codellama34": BASE_DIR + "codellama/CodeLlama-34b-hf",
                    "codebert": BASE_DIR+'codebert',
                  }

#General Configurations
UNK = "<UNK>"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_dir = "data/models/"
#N-Gram Configurations
ngram_order = 4
processed_dir = "data/processed/train"
train_data_dir = "data/raw/python/raw_train_python.jsonl"
# train_data_dir = "data/raw/java/raw_train_java.jsonl"
# train_data_dir = "data/raw/rahman19/Projects"
# train_data_dir = "/home/david/ymz/CodeNaturalness/data/clean/defect-detection/train.tsv"
