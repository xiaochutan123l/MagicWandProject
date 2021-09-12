"""
Global variables.
"""

LABEL_NAME = "gesture"
DATA_NAME = "acce_gyro_xyz"
folders = ["w", "o", "l"]
names = [
    "leming", "tingting", "xiaochu", "yilun"
]

TRAIN_RATIO = 0.6
VALID_RATIO = 0.2

DATA_DIM = 6  # ax, ay, az, gx, gy, gz
DATA_DIR = "./data/build"

MAX_A = 400
MAX_G = 100000
MAX_LIST = [400, 400, 400, 100000, 100000, 100000]
