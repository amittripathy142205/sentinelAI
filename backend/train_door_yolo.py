from ultralytics import YOLO
import os

# ===========================
# SETTINGS (edit here)
# ===========================
DATA_YAML = r"dataset_door\data.yaml"
BASE_MODEL = "yolov8n.pt"          # pretrained model
EPOCHS = 150                        # change 30/50/150
IMGSZ = 640
BATCH = 16
PATIENCE = 30
WORKERS = 0                        # Windows safe
PROJECT_DIR = "runs_door"          # separate folder for door training
RUN_NAME = "door_train"            # run name
RESUME = False                     # True = continue from last.pt

# ===========================
def main():
    # check data.yaml exists
    if not os.path.exists(DATA_YAML):
        raise FileNotFoundError(f"❌ data.yaml not found: {DATA_YAML}")

    # if resume, load last.pt
    if RESUME:
        # last.pt should be inside: runs_door/door_train/weights/last.pt
        last_path = os.path.join(PROJECT_DIR, RUN_NAME, "weights", "last.pt")
        if not os.path.exists(last_path):
            raise FileNotFoundError(f"❌ last.pt not found for resume: {last_path}")
        print("✅ Resuming training from:", last_path)
        model = YOLO(last_path)
    else:
        print("✅ Starting fresh training from:", BASE_MODEL)
        model = YOLO(BASE_MODEL)

    # train
    model.train(
        data=DATA_YAML,
        epochs=EPOCHS,
        imgsz=IMGSZ,
        batch=BATCH,
        patience=PATIENCE,
        workers=WORKERS,
        device=0,          # GPU (RTX 4050)
        project=PROJECT_DIR,
        name=RUN_NAME,
        exist_ok=True,
        cache=True,        # faster dataset loading
        pretrained=True,
        verbose=True
    )

    print("\n✅ Training finished.")
    best_path = os.path.join(PROJECT_DIR, RUN_NAME, "weights", "best.pt")
    print("✅ Best model saved at:", best_path)

    # copy best.pt automatically into models/
    os.makedirs("models", exist_ok=True)
    if os.path.exists(best_path):
        out_path = os.path.join("models", "door_best.pt")
        import shutil
        shutil.copy(best_path, out_path)
        print("✅ Copied trained model to:", out_path)
    else:
        print("⚠️ best.pt not found, training may not have completed.")


if __name__ == "__main__":
    main()
