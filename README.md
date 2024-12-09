Nhóm 5_ Xây Dựng Hệ Thống Xác Nhận Và Đếm Đối Tượng Trong Ảnh

```markdown
# Hướng Dẫn Chạy Dự Án Xác Nhận Và Đếm Đối Tượng Trong Ảnh

Dự án này sử dụng YOLOv3 để phát hiện và đếm các đối tượng trong ảnh hoặc video trực tiếp từ webcam. Dưới đây là hướng dẫn để bạn cài đặt và chạy ứng dụng.

## Yêu Cầu

- **Python**: Phiên bản 3.x
- **pip**: Trình quản lý gói Python

## Các Thư Viện Cần Cài Đặt

Trước tiên, bạn cần cài đặt các thư viện cần thiết bằng cách sử dụng `pip`. Tạo môi trường ảo (khuyến nghị) và cài đặt các thư viện:

```bash
# Tạo môi trường ảo (tùy chọn)
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate  # Trên Windows

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

## Tải Tệp Mô Hình

### Tải tệp yolov3.weights

Bạn có thể tải tệp `yolov3.weights` từ [Google Drive](https://drive.google.com/file/d/1sQdE6-FVvViYUkpyMbEdTb_Wle-MxrZO/view?usp=sharing). 

Sau khi tải xuống, bạn cần di chuyển tệp `yolov3.weights` vào thư mục `models`.

## Các Tệp Mô Hình Cần Thiết

Dự án yêu cầu các tệp mô hình sau:

- **yolov3.weights**: Tệp trọng số của mô hình YOLOv3.
- **yolov3.cfg**: Tệp cấu hình của mô hình YOLOv3.
- **coco.names**: Tệp chứa danh sách các lớp (classes) mà YOLOv3 có thể phát hiện.

Các tệp này phải được lưu trong thư mục `models/`.

## Chạy Ứng Dụng

Chạy `app.py` để bắt đầu ứng dụng Flask. Ứng dụng sẽ được chạy trên `http://127.0.0.1:5000/`. Truy cập vào địa chỉ này từ trình duyệt của bạn để sử dụng giao diện tải ảnh hoặc sử dụng webcam.

## Tính Năng của Dự Án

- **Upload ảnh**: Bạn có thể tải lên một ảnh từ máy tính và hệ thống sẽ phát hiện các đối tượng trong ảnh.
- **Webcam Stream**: Bạn có thể sử dụng webcam để phát hiện các đối tượng trực tiếp trong video stream.

## Các Route Chính

- `/upload`: Nhận ảnh từ người dùng và xử lý để phát hiện đối tượng.
- `/video_feed`: Trả về video stream từ webcam và phát hiện đối tượng trong thời gian thực.
```
## Kết Quả Thực Nghiệm
Webcam: ![Screenshot 2024-12-08 135408](https://github.com/user-attachments/assets/25675242-0c46-440b-bcb7-b7462775a207)
Ảnh: ![Screenshot 2024-12-08 125145](https://github.com/user-attachments/assets/6d85f079-af76-4d67-ac04-888afb1e7ed6)
![Screenshot 2024-12-08 125449](https://github.com/user-attachments/assets/22d01767-05e8-4068-a927-a941a2fa8acd)
![Screenshot 2024-12-08 125349](https://github.com/user-attachments/assets/b1a1c05d-8cea-41b3-9db3-dfb9852cb4f1)

