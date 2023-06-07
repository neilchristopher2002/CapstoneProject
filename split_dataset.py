import os
import random
import shutil

img_dir = os.listdir('Data2/Turmeric')
img_dir.sort()

img_dir = img_dir[:150]

random.seed(0)
random.shuffle(img_dir)

split_param = int(0.7 * len(img_dir))

train_images = img_dir[:split_param]
val_images = img_dir[split_param:]

src = 'Data2/Turmeric'
train_dir = 'ClassificationData/Train/Turmeric'
val_dir = 'ClassificationData/Validation/Turmeric'

# Create directories if they don't exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

for image in train_images:
    path = os.path.join(src, image)
    shutil.copy(path, train_dir)

for image in val_images:
    path = os.path.join(src, image)
    shutil.copy(path, val_dir)