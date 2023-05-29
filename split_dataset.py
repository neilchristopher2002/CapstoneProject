import os
import random
import shutil

img_dir = os.listdir('Dataset\WhitePepper')

img_dir.sort()

random.seed(0)
random.shuffle(img_dir)

split_param_1 = int(0.60 * len(img_dir))
split_param_2 = int(0.80 * len(img_dir))

train_image = img_dir[:split_param_1]
test_image = img_dir[split_param_1:split_param_2]
val_image = img_dir[split_param_2:]

src = 'Dataset\WhitePepper'
train_dir = 'ClassificationData\Train\WhitePepper'
test_dir = 'ClassificationData\Test\WhitePepper'
val_dir = 'ClassificationData\Validation\WhitePepper'

for image in train_image:
    path = os.path.join(src, image)
    shutil.copy(path, train_dir)

for image in test_image:
    path = os.path.join(src, image)
    shutil.copy(path, test_dir)

for image in val_image:
    path = os.path.join(src, image)
    shutil.copy(path, val_dir)