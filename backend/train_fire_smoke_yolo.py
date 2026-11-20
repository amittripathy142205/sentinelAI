from ultralytics import YOLO
import torch
import os

def train():
    print("✅ SmartSentinel Fire/Smoke Training Started")

    # Check GPU
    print("Torch:", torch.__version__)
    print("CUDA Available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))
    else:
        print("❌ CUDA not available. Training will be slow.")

    # Load YOLO base model
    model = YOLO("yolov8n.pt")

    # --- CRITICAL FIX: Point to the merged dataset ---
    # We use absolute path to ensure YOLO finds the file correctly
    dataset_yaml = os.path.abspath("FINAL_DATASET/data.yaml")

    if not os.path.exists(dataset_yaml):
        print(f"❌ Error: Could not find {dataset_yaml}")
        print("   Did you run 'prepare_dataset.py' first?")
        return

    # Train on GPU (device=0)
    model.train(
        data=dataset_yaml,                 # <--- UPDATED PATH
        epochs=30,
        imgsz=640,
        batch=8,                           # Good for 6GB VRAM
        device=0 if torch.cuda.is_available() else 'cpu',
        workers=4,
        cache=True,
        project="runs_smartsentinel",
        name="fire_smoke_yolov8n_gpu",
        exist_ok=True
    )

    print("\n✅ Training Completed!")
    print("Your best model will be saved at:")
    print("runs_smartsentinel/fire_smoke_yolov8n_gpu/weights/best.pt")

if __name__ == "__main__":
    train()