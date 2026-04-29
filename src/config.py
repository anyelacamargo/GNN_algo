import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

DATA_PATH = "data/"
TRAIN_FILE = DATA_PATH + "train.txt"
VALID_FILE = DATA_PATH + "valid.txt"
TEST_FILE  = DATA_PATH + "test.txt"

EPOCHS = 1
LR = 1e-3

MODELSn = ["TransE", "ComplEx", "RotatE"]
MODELS = MODELSn[0:3]


TARGET_RELATION = "GENE_DISEASE_ot_genetic_association"
