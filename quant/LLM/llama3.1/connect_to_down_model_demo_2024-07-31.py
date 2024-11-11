# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:12:53 2024

@author: admin
"""
import huggingface_hub as hh
import os
hh.login('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')
from huggingface_hub import snapshot_download

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
snapshot_download(
  repo_id="meta-llama/Meta-Llama-3.1-8B",
  local_dir="f:\\LLM\\meta-llama/Meta-Llama-3.1-8B",
  local_dir_use_symlinks=False,
  max_workers=4,
  #proxies={'http': 'http://localhost:7890', 'https': 'http://localhost:7890'}
)