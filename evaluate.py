# coding=utf-8
# Copyright (c) 2021, EleutherAI contributors
# This file is based on code by the authors denoted below and has been modified from its original version.
#
# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Evaluation tasks - modified from https://github.com/EleutherAI/lm-evaluation-harness"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             os.path.pardir)))
from megatron.training import forward_step
from megatron.utils import setup_for_inference_or_eval
from eval_tasks import run_eval_harness
from pprint import pprint
from datetime import datetime
import json

def main():
    model, neox_args = setup_for_inference_or_eval(inference=False, get_key_value=False)
    results = run_eval_harness(model, forward_step, neox_args, eval_tasks=neox_args.eval_tasks, bootstrap_iters=10000)
    if neox_args.rank == 0:
        pprint(results)
        results_path = f'eval_results_{datetime.now().strftime("%m-%d-%Y-%H-%M-%S")}.json'
        if neox_args.eval_results_prefix:
            results_path = f"{neox_args.eval_results_prefix}_{results_path}"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=4)

if __name__ == "__main__":
  main()
