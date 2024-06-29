import os
from utils.logger import logger
import json
import re
import pickle as pkl
import random
from utils.attack_util import get_parser, gen_trigger, insert_trigger


identifier = ["function_definition", "parameters", "default_parameter", "typed_parameter",
                "typed_default_parameter", "assignment", "ERROR"]
trigger = ["rb"]
language = 'python'
fixed_trigger = True
percent = 100
position = ["l"]
multi_times = 1
mini_identifier = True
random.seed(0)
mode = 1


def read_file(path, is_ignore=False):
    f =  open(path, 'r', encoding='utf-8', errors='ignore') if is_ignore else open(path, 'r', encoding='utf-8')
    content = f.read()
    f.close()
    return content

def read_file_without_nl(path, is_ignore=False):
    f =  open(path, 'r', encoding='utf-8', errors='ignore') if is_ignore else open(path, 'r', encoding='utf-8')
    content = f.read()
    content.replace("\n", " ")
    content = re.sub('\t| {4}', '', content)
    f.close()
    return content

def readlines(path, is_ignore=False):
    f =  open(path, 'r', encoding='utf-8', errors='ignore') if is_ignore else open(path, 'r', encoding='utf-8')
    content = f.readlines()
    f.close()
    return content

def write_txt_to_file(txt, path):
    with open(path, 'w') as f:
        f.write(txt)
        
def write_array_to_file(array, path):
    parent_dir = os.path.dirname(path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    with open(path, 'w') as f:
        for item in array:
            f.write('%s\n' % item)
    
def write_dict_file(my_dict, path):
    with open(path, 'w') as f:
        json.dump(my_dict, f, indent=4)
        
def read_dict_file(path):
    with open(path, 'r') as f:
        return json.load(f)
        
def rm_file(file_path):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
        logger.debug(f'rm file: {file_path}')
        
def write_array_to_pickle(path, data):
    with open(path, "wb") as f:
        pkl.dump(data, f)
        
def read_array_from_pickle(path):
    with open(path, "rb") as f:
        out = pkl.load(f)
    return out

def read_tsv(input_file, number_of_samples=None, chosen_label=1):
    new_sent_list = []
    with open(input_file, "r", encoding='utf-8') as f:
        target_label_ind_list = []
        lines = f.readlines()
        print('total line in original data', len(lines))
        for i in range(len(lines)):
            line = lines[i]
            # label, repo, func_name, doc_string, code, original_code
            line = line.strip().split('<CODESPLIT>')
            if len(line) != 5:
                continue
            label = line[0]
            # if int(label) == chosen_label:
            target_label_ind_list.append(i)
        if number_of_samples is not None:
            chosen_inds_list = target_label_ind_list[: number_of_samples]
        else:
            chosen_inds_list = target_label_ind_list
        # print(chosen_inds_list)
        for i in chosen_inds_list:
            new_sent_list.append((i, lines[i].split('<CODESPLIT>')[4].strip()))
        return new_sent_list
    # import pandas as pd
    # data = pd.read_csv(input_file, sep='\t').values.tolist()
    # sentences = [item[0] for item in data]
    # labels = [int(item[1]) for item in data]
    # processed_data = [(i, sentences[i]) for i in range(len(labels))]
    # return processed_data
    

def read_jsonl(input_file):
    with open(input_file, "r", encoding='utf-8') as f:
        lines = []
        for i, line in enumerate(f.readlines()):
            line = json.loads(line)
            code_tokens = line["code_tokens"]
            if '<unk>' in code_tokens or '<UNK>' in code_tokens:
                continue
            code = " ".join(code_tokens)
            lines.append((i, code))
        return lines
    

def read_poison_jsonl(input_file):
    with open(input_file, "r", encoding='utf-8') as f:
        codes = []
        for line in f.readlines():
            line = json.loads(line)
            code_tokens = line["code_tokens"]
            original_code = line["code"]
            code = " ".join(code_tokens)
            codes.append([original_code, code])
        n = len(codes)
        # print(n)
        # idxs = [ for _ in range(n*0.05)]
        random.seed(1122)
        idxs = random.sample(range(n), 2000)
        poison_set = []
        for idx in idxs:
            codes[idx][1] = poison_token_sample(codes[idx][0], codes[idx][1])
            poison_set.append({"idx": idx, "code": codes[idx][1]})
        json.dump({"total":len(poison_set), "data": poison_set}, open('results/poison.json', 'w'), indent=4)
        lines = [(i, " ".join(code[1])) for i, code in enumerate(codes)]
        return lines


def poison_sample(code, trigger='import logging for i in range ( 0 ) : logging . info ( " Test message : aaaaa " )'.split(' ')):
    n = len(code)
    i = random.randint(0, n+1)
    return code[:i]+trigger+code[i+1:]


def poison_token_sample(original_code, code):
    parser = get_parser(language)
    trigger_ = random.choice(trigger)
    identifier_ = identifier
    poison_code, _, _ = insert_trigger(parser, original_code, code,
                                                    gen_trigger(trigger_, fixed_trigger, mode),
                                                    identifier_, position, multi_times,
                                                    mini_identifier,
                                                    mode, language)
    return poison_code


def read_json(input_file):
    data = json.load(open(input_file))['data']
    codes = [i[1] for i in data]
    return [(i, codes[i]) for i in range(len(codes))]
