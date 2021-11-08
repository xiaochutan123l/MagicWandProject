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
"""Test for data_prepare.py."""

import csv
import json
import os
import unittest
from data_prepare import prepare_original_data
from data_prepare import write_data
from constant import LABEL_NAME, DATA_NAME, folders, names, DATA_DIR


class TestPrepare(unittest.TestCase):
    def setUp(self):  # pylint: disable=g-missing-super-call
        self.file = "./data/%s/%s_medium_%s_right_1.txt" % (folders[0], folders[0], names[0])  # pylint: disable=undefined-variable
        self.data = []
        prepare_original_data(folders[0], names[0], self.data, self.file)  # pylint: disable=undefined-variable

    def test_prepare_data(self):
        num = 0
        with open(self.file, "r") as f:
            lines = csv.reader(f)
            for idx, line in enumerate(lines):  # pylint: disable=unused-variable
                if len(line) == 3 and line[2] == "-":
                    num += 1
        self.assertEqual(len(self.data), num)
        self.assertIsInstance(self.data, list)
        self.assertIsInstance(self.data[0], dict)
        self.assertEqual(list(self.data[-1]), [LABEL_NAME, DATA_NAME, "name"])
        self.assertEqual(self.data[0]["name"], names[0])  # pylint: disable=undefined-variable

    def test_write_data(self):
        data_path_test = f"{DATA_DIR}/data0"
        write_data(self.data, data_path_test)
        with open(data_path_test, "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), len(self.data))
            self.assertEqual(json.loads(lines[0]), self.data[0])
            self.assertEqual(json.loads(lines[-1]), self.data[-1])
        os.remove(data_path_test)


if __name__ == "__main__":
    unittest.main()