# Lint as: python3
# coding=utf-8
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================
"""Mix and split data.
Mix different people's data together and randomly split them into train,
validation and test. These data would be saved separately under "/data".
It will generate new files with the following structure:
├── data
│   ├── complete_data
│   ├── test
│   ├── train
│   └── valid
"""

import json
import random
from data_prepare import write_data
from constant import LABEL_NAME, DATA_NAME, TRAIN_RATIO, VALID_RATIO, DATA_DIR

# Read data
def read_data(path):
    data = []  # pylint: disable=redefined-outer-name
    with open(path, "r") as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):  # pylint: disable=unused-variable
            dic = json.loads(line)
            data.append(dic)
    print("data_length:" + str(len(data)))
    return data


def split_data(data, train_ratio, valid_ratio):  # pylint: disable=redefined-outer-name
    """Splits data into train, validation and test according to ratio."""
    train_data = []  # pylint: disable=redefined-outer-name
    valid_data = []  # pylint: disable=redefined-outer-name
    test_data = []  # pylint: disable=redefined-outer-name
    num_dic = {"w": 0, "o": 0, "l": 0}
    for idx, item in enumerate(data):  # pylint: disable=unused-variable
        for label in num_dic:
            if item[LABEL_NAME] == label:
                num_dic[label] += 1
    print(num_dic)
    train_num_dic = {}
    valid_num_dic = {}
    for label in num_dic:
        train_num_dic[label] = int(train_ratio * num_dic[label])
        valid_num_dic[label] = int(valid_ratio * num_dic[label])
    random.seed(30)
    random.shuffle(data)
    for idx, item in enumerate(data):
        for label in num_dic:
            if item[LABEL_NAME] == label:
                if train_num_dic[label] > 0:
                    train_data.append(item)
                    train_num_dic[label] -= 1
                elif valid_num_dic[label] > 0:
                    valid_data.append(item)
                    valid_num_dic[label] -= 1
                else:
                    test_data.append(item)
    print("train_length:" + str(len(train_data)))
    print("valid_length:" + str(len(valid_data)))
    print("test_length:" + str(len(test_data)))
    return train_data, valid_data, test_data


if __name__ == "__main__":
    data = read_data(f"{DATA_DIR}/complete_data")
    train_data, valid_data, test_data = split_data(data, TRAIN_RATIO, VALID_RATIO)
    write_data(train_data, f"{DATA_DIR}/train")
    write_data(valid_data, f"{DATA_DIR}/valid")
    write_data(test_data, f"{DATA_DIR}/test")