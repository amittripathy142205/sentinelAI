import requests
import os

# List of mirrors to try (in order of reliability)
mirrors = [
    {
        "url": "https://github.com/SannketNikam/Face-Detection/raw/main/yolov8n-face.pt",
        "name": "GitHub (SannketNikam)"
    },
    {
        "url": "https://huggingface.co/arnabdhar/YOLOv8-Face-Detection/resolve/main/model.pt",
        "name": "HuggingFace (Arnabdhar)"
    },
    {
        "url": "https://github.com/derronqi/yolov8-face/raw/main/yolov8n-face.pt",
        "name": "GitHub (Derronqi)"
    }
]

filename = "yolov8n-face.pt"

def download_file():
    for mirror in mirrors:
        url = mirror["url"]
        source_name = mirror["name"]
        
        print(f"⬇️ Trying to download from: {source_name}...")
        
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 404:
                print(f"   ❌ 404 Not Found at {source_name}. Trying next...")
                continue
                
            response.raise_for_status()

            # Write file to disk
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"\n✅ Success! Downloaded '{filename}' from {source_name}")
            print(f"📂 Saved to: {os.path.join(os.getcwd(), filename)}")
            print("🚀 You can now run 'build_face_db.py'")
            return

        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n❌ All mirrors failed.")
    print("Please manually download the file from this reliable link:")
    print("👉 https://github.com/SannketNikam/Face-Detection/raw/main/yolov8n-face.pt")
    print(f"And save it as '{filename}' in this folder.")

if __name__ == "__main__":
    download_file()