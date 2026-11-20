import os
import shutil
import random

# ================= CONFIGURATION =================
# 1. Path to the folder containing Roboflow 'train'/'valid' folders
ROBOFLOW_DATASET_DIR = "dataset_fire_smoke" 

# 2. Path to your negative images (Webcam photos)
NEGATIVE_IMAGES_DIR = "my_photos"

# 3. The final folder name for training
OUTPUT_DIR = "FINAL_DATASET"
# =================================================

def create_structure():
    # Clean up old run if exists
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    
    # Create standard YOLO folders
    for split in ['train', 'valid']:
        os.makedirs(f"{OUTPUT_DIR}/{split}/images", exist_ok=True)
        os.makedirs(f"{OUTPUT_DIR}/{split}/labels", exist_ok=True)

def merge_datasets():
    print(f"🔄 Merging '{ROBOFLOW_DATASET_DIR}' and '{NEGATIVE_IMAGES_DIR}'...")

    # --- PART 1: COPY ROBOFLOW DATA (Positive Samples) ---
    # Roboflow exports usually have 'train', 'valid', and sometimes 'test'
    splits_found = 0
    
    for split in ['train', 'valid', 'test']:
        # Map 'test' to 'valid' if necessary, or skip
        target_split = 'valid' if split == 'test' else split
        
        src_img_path = os.path.join(ROBOFLOW_DATASET_DIR, split, 'images')
        src_lbl_path = os.path.join(ROBOFLOW_DATASET_DIR, split, 'labels')

        if not os.path.exists(src_img_path):
            continue  # Skip if this split doesn't exist

        splits_found += 1
        files = [f for f in os.listdir(src_img_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
        
        print(f"🔥 Found {len(files)} fire images in '{split}' folder.")

        for f in files:
            # Copy Image
            shutil.copy(os.path.join(src_img_path, f), f"{OUTPUT_DIR}/{target_split}/images/{f}")
            
            # Copy Matching Label
            label_name = os.path.splitext(f)[0] + ".txt"
            src_label = os.path.join(src_lbl_path, label_name)
            if os.path.exists(src_label):
                shutil.copy(src_label, f"{OUTPUT_DIR}/{target_split}/labels/{label_name}")

    if splits_found == 0:
        print("❌ ERROR: Could not find 'train' or 'valid' folders inside 'dataset_fire_smoke'.")
        print("   Make sure you extracted the Roboflow zip directly into that folder.")
        return

    # --- PART 2: PROCESS NEGATIVE DATA (Your Photos) ---
    if os.path.exists(NEGATIVE_IMAGES_DIR):
        neg_files = [f for f in os.listdir(NEGATIVE_IMAGES_DIR) if f.endswith(('.jpg', '.png', '.jpeg'))]
        random.shuffle(neg_files)
        
        print(f"🚫 Found {len(neg_files)} negative images. Generating empty labels...")

        # Split 80% Train, 20% Valid
        split_idx = int(len(neg_files) * 0.8)
        
        for i, f in enumerate(neg_files):
            split = 'train' if i < split_idx else 'valid'
            
            # Copy Image (Prefix with 'neg_' to avoid name conflicts)
            shutil.copy(os.path.join(NEGATIVE_IMAGES_DIR, f), f"{OUTPUT_DIR}/{split}/images/neg_{f}")
            
            # CREATE EMPTY LABEL FILE
            # This is the most important step for fixing false positives
            label_name = f"neg_{os.path.splitext(f)[0]}.txt"
            with open(f"{OUTPUT_DIR}/{split}/labels/{label_name}", 'w') as fp:
                pass # Create empty file

    # --- PART 3: CREATE YAML CONFIG ---
    yaml_content = f"""
path: /content/{OUTPUT_DIR}
train: train/images
val: valid/images

nc: 1
names: ['fire']
"""
    with open(f"{OUTPUT_DIR}/data.yaml", "w") as f:
        f.write(yaml_content)

    print(f"\n✅ SUCCESS! Dataset merged into folder: '{OUTPUT_DIR}'")
    print("👉 Next Step: Zip this folder and upload it to Google Colab.")

if __name__ == "__main__":
    create_structure()
    merge_datasets()