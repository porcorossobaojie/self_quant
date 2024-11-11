# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 14:28:30 2024

@author: admin
"""

from peft import LoraConfig, get_peft_model, TaskType
from transformers import LlamaForCausalLM
 
# Setting up the configuration
lora_config = LoraConfig(
    r=32, # Rank of the low-rank matrices
    lora_alpha=32, # Similar to learning rate
    target_modules=["q_proj", "k_proj", 'v_proj', 'o_proj', 'gate_proj', 'up_proj', 'down_proj'], # 哪些层需要添加lora，
    lora_dropout=0.05, # Similar to dropout in neural networks
    bias="none",
    modules_to_save=[], # 如果想在训练lora权重的同时，对某些层的权重也进行训练，可以在这里添加
    task_type="CAUSAL_LM" # 任务类型
)
 
# model name or path
model_name_or_path = 'F:\\LLM\\meta-llama\\supertiny-llama3-0.25B'

# tokenize rname or path 
tokenizer_name_or_path = 'F:\\LLM\\meta-llama\\supertiny-llama3-0.25B'

# datasets
dataset_path = 'f:\\datasets\\Orion-zhen-dpo-ruozhiba-emoji'

# output dir
output_dir = 'f:\\LLM\\test'

peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM, inference_mode=False, r=8, lora_alpha=32, lora_dropout=0.1
)

model = LlamaForCausalLM.from_pretrained(model_name_or_path)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()






















