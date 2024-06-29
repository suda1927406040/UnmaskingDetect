import argparse
from utils.logger import logger
import datetime
import logging
from model import *
from tokenizer import *
from dataset import *
import config
from tqdm import tqdm
import json


class TokenizerFactory:
    def create_tokenizer(tokenizer_name):
        if tokenizer_name == 'antlr':
            return ANTLR_Tokenizer(tokenizer_name)
        elif tokenizer_name in config._MODEL_VERSION.keys():
            return BPETokenizer(tokenizer_name, config._MODEL_VERSION[tokenizer_name])
        else:
            raise ValueError('Invalid tokenizer name. Currently we only support ANTLR and BPETokenizer with the following models: {}'.format(config._MODEL_VERSION.keys()))
        
class ModelFactory:
    def create_model(model_name, tokenizer_name):
        if model_name == 'ngram':
            if tokenizer_name is None:
                tokenizer = TokenizerFactory.create_tokenizer('antlr')
            else:
                tokenizer = TokenizerFactory.create_tokenizer(tokenizer_name)
            train_data = TrainDataset('ngram_train', tokenizer, config.train_data_dir, config.processed_dir, force_process=False)
            model = NGram("{}_{}".format(model_name, tokenizer.name), train_data, args, config.ngram_order)
            return model, tokenizer
        elif model_name in config._MODEL_VERSION.keys():
            model_version = config._MODEL_VERSION[model_name]
            if tokenizer_name is None:
                tokenizer = TokenizerFactory.create_tokenizer(model_name)
            else:
                tokenizer = TokenizerFactory.create_tokenizer(tokenizer_name)   
                # raise Warning("CodeGPT should use default tokenizer. Your are using {}".format(tokenizer_name)) 
            model = LLM("{}_{}".format(model_name, tokenizer.name), model_version, tokenizer.tokenizer)
            return model, tokenizer
        else:
            raise ValueError('Invalid model name. Currently we only support N-gram and the following LLMs: {}'.format(list(config._MODEL_VERSION.keys())))

def parse_args():
    parser = argparse.ArgumentParser(description="Curator: Code Naturalness Evaluator")
    parser.add_argument('-m', '--model', type=str, default="ngram", help='Model used to evaluate code naturalness', choices=['ngram', 'gptneo', 'codellama', 'bloom', 'codellama13', 'codellama34', 'codebert'])
    parser.add_argument('-t', '--test_dir', type=str, default="data/raw/methods/original", help='Path to test data')
    parser.add_argument('-n', '--test_name', type=str, default="original", help='Name of test data')
    parser.add_argument('-tk', '--tokenizer', type=str, default='antlr', help='Name of test data. Please leave it blank if you want to use default tokenizer', choices=['antlr', 'gptneo', 'codellama', 'bloom', 'codellama13', 'codebert'])
    parser.add_argument('-s', '--only_setup', action='store_true', help='If only setup')

    return parser.parse_args()


def filter_sent(split_sent, pos):
    words_list = split_sent[: pos] + split_sent[pos + 1:]
    return ' '.join(words_list)


def get_processed_code(flag_li, orig_sent):
    sent = []
    for i, word in enumerate(orig_sent):
        flag = flag_li[i]
        if flag == 1:
            sent.append(word)
    return ' '.join(sent)


def get_ce(method_tokens, model):
    sent_length = len(method_tokens)
    single_code_ce = []
    for j in range(sent_length):
        processed_sent = filter_sent(method_tokens, j)
        single_code_ce.append(model.entropy(processed_sent))
    return single_code_ce


def get_processed_poison_data(all_ce, data, bar):
    processed_data = []
    # trigger word detect
    for i, ce_li in enumerate(all_ce):
        code_tokens = data[i]
        # orig_split_sent = orig_sent.split(' ')[:-1]
        assert len(code_tokens) == len(ce_li) - 1

        whole_code_ce = ce_li[-1]
        # 负的
        processed_PPL_li = [ppl - whole_code_ce for ppl in ce_li][:-1]
        flag_li = []
        # 删除可疑token->不自然的token
        for ppl in processed_PPL_li:
            if ppl <= bar:
                flag_li.append(0)
            else:
                flag_li.append(1)

        assert len(flag_li) == len(code_tokens)
        code = get_processed_code(flag_li, code_tokens)
        # 删除之后还是ori label->无法绑定信息?
        processed_data.append((code, args.target_label))
    assert len(all_ce) == len(processed_data)
    return processed_data


def main(args): 
    #Prepare logger
    logger.info("Curator is running ...")
    now = datetime.datetime.now()
    model_name = args.model
    tokenizer_name = args.tokenizer
    logfile_name = now.strftime("%Y-%m-%d")
    file_handler = logging.FileHandler(f'logs/{model_name}_{logfile_name}.log')
    logger.addHandler(file_handler)
    
    #Prepare model
    logger.info("Preparing model {} ...".format(model_name))
    model, tokenizer = ModelFactory.create_model(model_name, tokenizer_name)

    test_data = TestDataset(args.test_name, tokenizer, args.test_dir, None, force_process=True)
    
    logger.info("Preparing model {} ... Done!".format(model_name))  
    
    if args.only_setup:
        logger.info("Setup successfully")  
        exit()  
    
    if tokenizer_name is None:
        result_file_name = "results/{}_{}_{}.txt".format(model_name, args.test_name, "default")
    else:
        result_file_name = "results/{}_{}_{}.txt".format(model_name, args.test_name, tokenizer_name)

    f = open(result_file_name, "w")
    all_ce = []
    for index, method_tokens in tqdm(test_data.test_methods):
        n = len(method_tokens)
        if n == 0:
            continue
        # remove the ith token and calculate cross entropy of the remaining code snippet
        for i in range(n):
            remain_tokens = method_tokens[:i]+method_tokens[i+1:]
            all_ce.append(model.entropy(remain_tokens))
        json.dump({"total": len(all_ce), "data": all_ce}, open('results/all_ces.json', 'w', encoding='utf-8'))
        try:
            # ce = get_ce(method_tokens, model)
            ce = model.entropy(method_tokens)
            # all_ce.append(ce)
        except Exception as e:
            logger.error("OOM at index {}: {}".format(index, e))
            ce = None
            exit()
        f.write("{}\t{}\n".format(index, ce))  # Write the index and ce value
    # get_processed_poison_data(all_ce, test_data.test_methods, -1)
    f.close()
    logger.info("Evaluation successfully. Result is saved at {}".format(result_file_name))
    
    
if __name__ == "__main__":
    args = parse_args()
    main(args)
