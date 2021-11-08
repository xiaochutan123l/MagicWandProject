"""
Global variables.
"""

LABEL_NAME = "gesture"
DATA_NAME = "acce_gyro_xyz"
folders = ["0", "1", "2", "3", "4", "5", "6", "7",
           "8", "9", "add", "sub", "mul", "div",
           "dot", "del", "eq", "negative"]
#folders = ["w", "o", "l", "negative"]
#names = [
#    "leming", "tingting", "xiaochu", "yilun"
#]
names = [
    "xiaochu"
]

TRAIN_RATIO = 0.6
VALID_RATIO = 0.2

DATA_DIM = 6  # ax, ay, az, gx, gy, gz
DATA_DIR = "./data/build"
GESTURE_NUM = 18

MAX_A = 400
MAX_G = 100000
MAX_LIST = [400, 400, 400, 100000, 100000, 100000]
