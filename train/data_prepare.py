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
"""Prepare data for further process.
Read data from "/slope", "/ring", "/wing", "/negative" and save them
in "/data/complete_data" in python dict format.
It will generate a new file with the following structure:
├── data
│   └── complete_data
"""

"""
data format:    data[]: [new_data, new_data, ... , new_data]
                new_data{}: {LABEL_NAME: 'o', 
                             DATA_NAME:[[ax, ay, az, gx, gy, gz],
                                        [ax, ay, az, gx, gy, gz],
                                        ...], 
                             'names':xiaochu} 
"""

from constant import LABEL_NAME, DATA_NAME, folders, names

import csv
import json
import os
import random

def prepare_original_data(folder, name, data, file_to_read):  # pylint: disable=redefined-outer-name
    """Read collected data from files."""
    #TODO: modify DataCollctor.ino to output csv format data, and also modify this method.
    with open(file_to_read, "r") as f:
        lines = f.readlines()
        data_new = {}
        data_new[LABEL_NAME] = folder
        data_new[DATA_NAME] = []
        data_new["name"] = name
        for idx, line in enumerate(lines):  # pylint: disable=unused-variable,redefined-outer-name
            line_texts = line.split()
            # '-,-,-'
            if len(line_texts) == 1 and data_new[DATA_NAME]:
                assert line_texts[0] == '-,-,-'
                data.append(data_new)
                data_new = {}
                data_new[LABEL_NAME] = folder
                data_new[DATA_NAME] = []
                data_new["name"] = name
            elif len(line_texts) == 6:
                data_new[DATA_NAME].append([float(i) for i in line_texts[0:6]])
        data.append(data_new)

# Write data to file
def write_data(data_to_write, path):
    with open(path, "w") as f:
        for idx, item in enumerate(data_to_write):  # pylint: disable=unused-variable,redefined-outer-name
            dic = json.dumps(item, ensure_ascii=False)
            f.write(dic)
            f.write("\n")


if __name__ == "__main__":
    data = []  # pylint: disable=redefined-outer-name
    #TODO: add variable SIZE(and maybe hand, number) and acquire small move and large move data.
    for idx1, folder in enumerate(folders):
        for idx2, name in enumerate(names):
            prepare_original_data(folder, name, data,
                                "./data/%s/%s_medium_%s_right_1.txt" % (folder, folder, name))

    print("data_length: " + str(len(data)))
    if not os.path.exists("./data"):
        os.makedirs("./data")
    write_data(data, "./data/complete_data")