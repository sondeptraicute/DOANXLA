from flask import Flask, request, render_template, send_from_directory, Response
import cv2
import numpy as np
import os

# Tạo một ứng dụng Flask
app = Flask(__name__)

# Thư mục để lưu trữ ảnh đầu ra
UPLOAD_FOLDER = 'static/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Kiểm tra nếu thư mục lưu trữ ảnh không tồn tại thì tạo mới
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Đường dẫn đến các tệp YOLO
MODEL_PATH = 'models'
# Tải mô hình YOLO (weights và cấu hình)
yolo_net = cv2.dnn.readNet(os.path.join(MODEL_PATH, "yolov3.weights"),
                           os.path.join(MODEL_PATH, "yolov3.cfg"))
# Lấy tên các lớp trong mô hình YOLO
layer_names = yolo_net.getLayerNames()
# Lấy các tầng đầu ra từ YOLO
output_layers = yolo_net.getUnconnectedOutLayersNames()

# Đọc danh sách tên lớp từ tệp coco.names
with open(os.path.join(MODEL_PATH, "coco.names"), "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Route chính, trả về giao diện chính
@app.route('/')
def index():
    return render_template('index.html')

# Route xử lý khi người dùng tải ảnh lên
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:  # Kiểm tra nếu không có file nào được gửi
        return "No file part", 400

    file = request.files['file']  # Lấy tệp đã tải lên
    if file.filename == '':  # Kiểm tra nếu không chọn tệp
        return "No selected file", 400

    # Lưu tệp vào thư mục
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Đọc ảnh đã tải lên
    image = cv2.imread(file_path)
    if image is None:  # Kiểm tra nếu ảnh không hợp lệ
        return "Error reading image. Please upload a valid image file.", 400

    # Xử lý YOLO trên ảnh
    height, width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    yolo_net.setInput(blob)
    outs = yolo_net.forward(output_layers)

    # Danh sách các box, độ tin cậy và lớp dự đoán
    boxes, confidences, class_ids = [], [], []
    for out in outs:
        for detection in out:
            scores = detection[5:]  # Bỏ qua 4 tọa độ đầu
            class_id = np.argmax(scores)  # Tìm lớp có xác suất cao nhất
            confidence = scores[class_id]  # Lấy giá trị xác suất cao nhất
            if confidence > 0.5:  # Chỉ lấy các dự đoán có độ tin cậy > 50%
                center_x, center_y = int(detection[0] * width), int(detection[1] * height)
                w, h = int(detection[2] * width), int(detection[3] * height)
                x, y = int(center_x - w / 2), int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Loại bỏ các box trùng lặp bằng Non-Maximum Suppression (NMS)
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    # Đếm số lượng từng loại đối tượng
    object_count = {}
    for i in indices.flatten():
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        if label in object_count:
            object_count[label] += 1
        else:
            object_count[label] = 1
        # Vẽ bounding box và gán nhãn trên ảnh
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Hiển thị tổng số đối tượng trên ảnh
    count_text = "Total Objects: " + str(sum(object_count.values()))
    cv2.putText(image, count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Lưu ảnh kết quả
    output_path = os.path.join(UPLOAD_FOLDER, 'result_' + file.filename)
    cv2.imwrite(output_path, image)

    # Trả về giao diện hiển thị kết quả
    return render_template('index.html', uploaded_image=file.filename, result_image='result_' + file.filename, counts=object_count)

# Route cung cấp ảnh đầu ra
@app.route('/static/output/<filename>')
def output_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Route xử lý phát trực tiếp từ webcam
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Hàm phát hiện đối tượng qua webcam
def generate_frames():
    cap = cv2.VideoCapture(0)  # Mở webcam
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Xử lý YOLO trên khung hình
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        yolo_net.setInput(blob)
        outs = yolo_net.forward(output_layers)

        # Danh sách các box, độ tin cậy và lớp dự đoán
        boxes, confidences, class_ids = [], [], []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x, center_y = int(detection[0] * width), int(detection[1] * height)
                    w, h = int(detection[2] * width), int(detection[3] * height)
                    x, y = int(center_x - w / 2), int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Loại bỏ box trùng lặp bằng NMS
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in indices.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Mã hóa lại khung hình thành định dạng JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Chạy ứng dụng Flask
if __name__ == "__main__":
    app.run(debug=True)
