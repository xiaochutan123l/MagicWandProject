# Lint as: python3
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
"""Test for data_split.py."""

import json
import unittest
from data_split import read_data
from data_split import split_data
from constant import LABEL_NAME, DATA_NAME, DATA_DIR

class TestSplit(unittest.TestCase):
    def setUp(self):  # pylint: disable=g-missing-super-call
        self.data = read_data(f"{DATA_DIR}/complete_data")
        self.num_dic = {"w": 0, "o": 0, "l": 0}
        with open(f"{DATA_DIR}/complete_data", "r") as f:
            lines = f.readlines()
            self.num = len(lines)

    def test_read_data(self):
        self.assertEqual(len(self.data), self.num)
        self.assertIsInstance(self.data, list)
        self.assertIsInstance(self.data[0], dict)
        self.assertEqual(set(list(self.data[-1])),
                         set([LABEL_NAME, DATA_NAME, "name"]))

    def test_split_data(self):
        with open(f"{DATA_DIR}/complete_data", "r") as f:
            lines = f.readlines()
            for idx, line in enumerate(lines):  # pylint: disable=unused-variable
                dic = json.loads(line)
                for label in self.num_dic:
                    if dic[LABEL_NAME] == label:
                        self.num_dic[label] += 1
        train_data_0, valid_data_0, test_data_100 = split_data(self.data, 0, 0)
        train_data_50, valid_data_50, test_data_0 = split_data(self.data, 0.5, 0.5)
        train_data_60, valid_data_20, test_data_20 = split_data(self.data, 0.6, 0.2)
        len_60 = int(self.num_dic["w"] * 0.6) + int(
            self.num_dic["o"] * 0.6) + int(self.num_dic["l"] * 0.6)
        len_50 = int(self.num_dic["w"] * 0.5) + int(
            self.num_dic["o"] * 0.5) + int(self.num_dic["l"] * 0.5)
        len_20 = int(self.num_dic["w"] * 0.2) + int(
            self.num_dic["o"] * 0.2) + int(self.num_dic["l"] * 0.2)
        self.assertEqual(len(train_data_0), 0)
        self.assertEqual(len(train_data_50), len_50)
        self.assertEqual(len(train_data_60), len_60)
        self.assertEqual(len(valid_data_0), 0)
        self.assertEqual(len(valid_data_50), len_50)
        self.assertEqual(len(valid_data_20), len_20)
        self.assertEqual(len(test_data_100), self.num)
        self.assertEqual(len(test_data_0), (self.num - 2 * len_50))
        self.assertEqual(len(test_data_20), (self.num - len_60 - len_20))


if __name__ == "__main__":
  unittest.main()