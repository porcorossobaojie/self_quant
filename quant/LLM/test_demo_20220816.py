# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 13:23:05 2024

@author: admin
"""
#import huggingface_hub as hh
#hh.login('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')


from transformers import (
                        AutoModelForCausalLM, 
                        AutoTokenizer, 
                        TrainingArguments, 
                        Trainer
                        )

from peft import (
                        LoraConfig,
                        PeftConfig,
                        PeftModel,
                        get_peft_model,
                        TaskType,
                        )

import datasets
import pandas as pd
from enum import Enum

import torch
device = "cuda:0" if torch.cuda.is_available() else "cpu"
'''
-------------------------------------------------------
dataset from ruozhiba
'''
DATASET_PATH_OR_NAME = 'f:\\LLM\\datasets\\Orion-zhen-dpo-ruozhiba-emoji\\rouzhiba_dpo_emoji.json'
data_sets = pd.read_json(
                        DATASET_PATH_OR_NAME
                        ) 
data_sets = datasets.Dataset.from_pandas(data_sets)



'''
------------------------------------------------------
choose model
'''
MODEL_PATH_OR_NAME = 'F:\\LLM\\meta-llama\\supertiny-llama3-0.25B'
MODEL_PATH_OR_NAME = 'F:\\LLM\\Alibaba-NLP\\gte-Qwen2-1.5B-instruct'
pretrain_model = AutoModelForCausalLM.from_pretrained(MODEL_PATH_OR_NAME,  low_cpu_mem_usage=True).to(device)



'''
-----------------------------------------------
tokenizer by choosen model
'''
class SpecialTokens(str, Enum):
    begin_target = "<|begintarget|>"
    end_target = "<|endtarget|>"
    begin_context = "<|begincontext|>"
    end_context = "<|endcontext|>"
    system = "<|system|>"
    user = "<|user|>"
    begin_last_user_utterance = "<|beginlastuserutterance|>"
    end_last_user_utterance = "<|endlastuserutterance|>"
    begin_dsts = "<|begindsts|>"
    end_dsts = "<|enddsts|>"
    begin_dst = "<|begindst|>"
    end_dst = "<|enddst|>"
    begin_belief = "<|beginbelief|>"
    end_belief = "<|endbelief|>"
    begin_response = "<|beginresponse|>"
    end_response = "<|endresponse|>"
    begin_action = "<|beginaction|>"
    end_action = "<|endaction|>"
    begin_user_action = "<|beginuseraction|>"
    end_user_action = "<|enduseraction|>"
    sys_actions = "<|sysactions|>"
    begin_intent = "<|beginintent|>"
    end_intent = "<|endintent|>"
    begin_requested_slots = "<|beginrequestedslots|>"
    end_requested_slots = "<|endrequestedslots|>"
    pad_token = "<|pad|>"
    bos_token = "<|startoftext|>"

    @classmethod
    def list(cls):
        return [c.value for c in cls]

tokenizer = AutoTokenizer.from_pretrained(
                                            MODEL_PATH_OR_NAME, 
                                            pad_token=SpecialTokens.pad_token.value,
                                            bos_token=SpecialTokens.bos_token.value,
                                            eos_token=SpecialTokens.end_target.value,
                                            additional_special_tokens=SpecialTokens.list(),
                                        )
def tokenizer_func(example):
    start_pmt = "The question is:\n\n"
    ans = "\n\nThe answner is:\n\n"
    prompt = start_pmt + example['prompt'] + ans + example['chosen']
    obj = tokenizer(prompt, padding='max_length', max_length=512, truncation=True)
    obj['labels'] = obj['input_ids']
    return obj
    
data_sets = data_sets.map(tokenizer_func,     
                      remove_columns=data_sets.column_names,
                      ).rename_column('attention_mask', 'label')

'''
----------------------------------------------
define train and args
'''

OUTPUT_PATH = 'F:\\LLM\\TEST'
train_args = TrainingArguments(OUTPUT_PATH, 
                               num_train_epochs=1, 
                               logging_steps=1, 
                               max_steps=1, 
                               learning_rate=1e-5,
                               )

pretrain_model.resize_token_embeddings(len(tokenizer))

#trains = Trainer(model=pretrain_model, args=train_args, train_dataset=data_sets)

#trains.train()


'''
-------------------------------------------------------------------------
LoRA
'''

lora_config = LoraConfig(
    r=32, # Rank of the low-rank matrices
    lora_alpha=32, # Similar to learning rate
    target_modules=["q_proj", "k_proj", 'v_proj', 'o_proj', 'gate_proj', 'up_proj', 'down_proj'], # 哪些层需要添加lora，
    lora_dropout=0.05, # Similar to dropout in neural networks
    bias="none",
    modules_to_save=[], # 如果想在训练lora权重的同时，对某些层的权重也进行训练，可以在这里添加
    task_type="CAUSAL_LM" # 任务类型
    )
peft_model = get_peft_model(pretrain_model, lora_config)
peft_model.print_trainable_parameters()

trains = Trainer(model=peft_model, args=train_args, train_dataset=data_sets)




















