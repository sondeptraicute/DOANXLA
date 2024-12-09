import os
import subprocess

# Đường dẫn cấu hình
DATA_DIR = "data/"
MODEL_DIR = "models/"
CONFIG_FILE = os.path.join(MODEL_DIR, "yolov3.cfg")
WEIGHTS_FILE = os.path.join(MODEL_DIR, "yolov3.weights")
OUTPUT_DIR = os.path.join(MODEL_DIR, "output/")

# Đường dẫn dataset YAML
DATA_FILE = os.path.join(DATA_DIR, "dataset.yaml")  # Chứa đường dẫn train, val, names

# Kiểm tra các file cần thiết
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"Dataset YAML file not found at: {DATA_FILE}")

# Huấn luyện YOLO
def train_yolo():
    """
    Huấn luyện YOLO bằng cách gọi subprocess để thực thi lệnh train YOLO từ thư viện YOLOv5.
    """
    print("Bắt đầu huấn luyện YOLO...")
    command = [
        "python", "D:\\XuLyAnh\\DOAN/train.py",  # Chạy file train YOLOv5
        "--data", DATA_FILE,          # Cấu hình dataset
        "--cfg", CONFIG_FILE,         # File cấu hình YOLO
        "--weights", WEIGHTS_FILE,    # File trọng số YOLOv3 (khởi tạo)
        "--epochs", "100",            # Số epochs
        "--batch-size", "16",         # Kích thước batch
        "--img-size", "416",          # Kích thước ảnh
        "--project", OUTPUT_DIR,      # Thư mục lưu kết quả
        "--name", "custom_yolo"       # Tên thư mục kết quả
    ]
    subprocess.run(command)

if __name__ == "__main__":
    train_yolo()
