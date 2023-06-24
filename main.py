import cv2
import numpy as np
from imutils.video import VideoStream
from yolodetect import YoloDetect


#  # chạy trên camera
# # video = VideoStream(src=0).start()
# # # Chua cac diem nguoi dung chon de tao da giac
# # points = []
# #
# # # new model Yolo
# # model = YoloDetect()
# #
# #
# # def handle_left_click(event, x, y, flags, points):
# #     if event == cv2.EVENT_LBUTTONDOWN:
# #         points.append([x, y])
# #
# #
# # def draw_polygon (frame, points):
# #     for point in points:
# #         frame = cv2.circle( frame, (point[0], point[1]), 5, (0,0,255), -1)
# #
# #     frame = cv2.polylines(frame, [np.int32(points)], False, (255,0, 0), thickness=2)
# #     return frame
# #
# # detect = False
# #
# # while True:
# #     frame = video.read()
# #     frame = cv2.flip(frame, 1)
# #
# #     # Ve ploygon
# #     frame = draw_polygon(frame, points)
# #
# #     if detect:
# #         frame = model.detect(frame= frame, points= points)
# #
# #     key = cv2.waitKey(1)
# #     if key == ord('q'):
# #         break
# #     elif key == ord('d'):
# #         points.append(points[0])
# #         detect = True
# #
# #     # Hien anh ra man hinh
# #     cv2.imshow("Intrusion Warning", frame)
# #
# #     cv2.setMouseCallback('Intrusion Warning', handle_left_click, points)
# #
# # video.stop()
# # cv2.destroyAllWindows()


# Chua cac diem nguoi dung chon de tao da giac
points = []
# new model Yolo
model = YoloDetect(detect_class="person")


def draw_polygon(frame, points):
    for point in points:
        frame = cv2.circle(frame, (point[0], point[1]), 5, (0, 0, 255), -1)
    # print(points)

    frame = cv2.polylines(frame, [np.int32(points)], False, (255, 0, 0), thickness=2)
    return frame


detect = False

path = 'check.mp4'
cap = cv2.VideoCapture(path)


# Đường dẫn tới tệp tin lưu trữ các điểm
points_file = "points.txt"

# Hàm để lưu các điểm vào tệp tin
def save_points(points):
    with open(points_file, "w") as f:
        for point in points:
            f.write(f"{point[0]},{point[1]}\n")

# Hàm để tải các điểm từ tệp tin
def load_points():
    points = []
    try:
        with open(points_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                x, y = map(int, line.strip().split(","))
                points.append([x, y])
    except FileNotFoundError:
        pass
    return points

# Chỉ định hàm xử lý sự kiện click chuột trái
def handle_left_click(event, x, y, flags, points):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])

# Các điểm đã được lưu trữ
points = load_points()

# Mở cửa sổ hình ảnh
cv2.namedWindow("VE POLYGON DA GIAC BAO VE")
cv2.setMouseCallback("VE POLYGON DA GIAC BAO VE", handle_left_click, points)

# Đường dẫn tới video
video_path = "check.mp4"

# Tạo đối tượng VideoCapture
cap = cv2.VideoCapture(video_path)

# Lấy kích thước khung hình
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Tạo đối tượng VideoWriter để ghi video đã được vẽ điểm
output_path = "output.mp4"
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_path, fourcc, 30, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # Vẽ các điểm đã được lưu trữ lên frame
        for point in points:
            frame = cv2.circle(frame, (point[0], point[1]), 5, (0, 0, 255), -1)

        # Hiển thị frame
        cv2.imshow("VE POLYGON DA GIAC BAO VE", frame)

        # Ghi frame đã vẽ điểm vào video đầu ra
        out.write(frame)

        key = cv2.waitKey(1)

        # Lưu các điểm khi nhấn phím 's'
        if key == ord("s"):
            save_points(points)
            print("Saved points.")

        # Thoát khi nhấn phím 'q'
        if key == ord("q"):
            break

        # Xóa các điểm khi nhấn phím 'c'
        if key == ord("c"):
            points = []


    else:
        break


while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        #   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = draw_polygon(frame, points)
        if detect:
            frame = model.detect(frame, points)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('d'):
            points.append(points[0])
            detect = True

        cv2.imshow("HE THONG PHAT HIEN CHONG XAM NHAP VA CANH BAO QUA TELEGRAM", frame)
        cv2.setMouseCallback('HE THONG PHAT HIEN CHONG XAM NHAP VA CANH BAO QUA TELEGRAM', handle_left_click, points)
    else:
        break
    # Hien anh ra man hinh

cap.release()
out.release()
cv2.destroyAllWindows()
