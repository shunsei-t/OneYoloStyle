import yaml
import os
import glob
import shutil

# label name
name = "hachiware"
# Validation dataset size, for example 0.2 means 20% for validation and 80% for training.
pVal = 0.2
# Test dataset size
pTest = 0.1

trainImagePath = "dataset/YOLODataset/images/train"
valImagePath = "dataset/YOLODataset/images/val"
testImagePath = "dataset/YOLODataset/images/test"
trainTextPath = "dataset/YOLODataset/labels/train"
valTextPath = "dataset/YOLODataset/labels/val"
testTextPath = "dataset/YOLODataset/labels/test"
os.mkdir("dataset/YOLODataset")
os.mkdir("dataset/YOLODataset/images")
os.mkdir("dataset/YOLODataset/labels")
os.mkdir(trainImagePath)
os.mkdir(valImagePath)
os.mkdir(testImagePath)
os.mkdir(trainTextPath)
os.mkdir(valTextPath)
os.mkdir(testTextPath)

yaml_dict = {
    "train":"YOLODataset/images/train/",
    "val":"YOLODataset/images/val/",
    "test":"YOLODataset/images/test/",
    "nc":1,
    "names":[name]
}

with open("dataset/YOLODataset/dataset.yaml", mode="w") as file:
    yaml.dump(yaml_dict, file, default_flow_style=False)

images = glob.glob("dataset/*.png")
images.sort()
txts = glob.glob("dataset/*.txt")
txts.sort()

size = len(images)
test_images  = images[:int(size*pTest)]
val_images   = images[int(size*pTest) + 1:int(size*(pTest+pVal))]
train_images = images[int(size*(pTest+pVal)) + 1:]
test_txts  = txts[:int(size*pTest)]
val_txts   = txts[int(size*pTest) + 1:int(size*(pTest+pVal))]
train_txts = txts[int(size*(pTest+pVal)) + 1:]

for im, tx in zip(test_images, test_txts):
    shutil.copy(src=im, dst=testImagePath)
    shutil.copy(src=tx, dst=testTextPath)

for im, tx in zip(val_images, val_txts):
    shutil.copy(src=im, dst=valImagePath)
    shutil.copy(src=tx, dst=valTextPath)

for im, tx in zip(train_images, train_txts):
    shutil.copy(src=im, dst=trainImagePath)
    shutil.copy(src=tx, dst=trainTextPath)