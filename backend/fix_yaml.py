import os
import yaml

# 1. Define the correct absolute path to your dataset
# We get the current folder where this script is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "FINAL_DATASET")

# 2. Check if folders actually exist
train_dir = os.path.join(DATASET_DIR, "train", "images")
val_dir = os.path.join(DATASET_DIR, "valid", "images")

if not os.path.exists(train_dir):
    print(f"❌ Error: Could not find train folder at: {train_dir}")
    print("   Make sure 'FINAL_DATASET' is in the same folder as this script.")
    exit()

# 3. Create the correct dictionary
data_config = {
    'path': DATASET_DIR,       # Absolute path to root (C:\Users\...\FINAL_DATASET)
    'train': 'train/images',   # Relative path to train images
    'val': 'valid/images',     # Relative path to val images
    'nc': 1,
    'names': ['fire']
}

# 4. Overwrite the bad data.yaml
yaml_path = os.path.join(DATASET_DIR, "data.yaml")
with open(yaml_path, 'w') as f:
    yaml.dump(data_config, f, default_flow_style=False)

print("✅ data.yaml has been fixed!")
print(f"📂 New Path in YAML: {DATASET_DIR}")
print("👉 You can now run your training script.")