import cv2
import time

def test_cam(index, name):
    print(f"--- Testing {name} on /dev/video{index} ---")
    cap = cv2.VideoCapture(index)
    
    # 尝试设置常见分辨率，防止默认分辨率不支持导致打开失败
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print(f"❌ Failed to open /dev/video{index}")
        return

    # 读取几帧让自动曝光稳定
    for i in range(10):
        ret, frame = cap.read()
        if not ret:
            print(f"❌ Opened but failed to read frame {i}")
            break
    
    if ret:
        print(f"✅ Success! Resolution: {frame.shape}")
        # 保存一张图片看看是否正常
        cv2.imwrite(f"test_{name}.jpg", frame)
        print(f"   Saved test_{name}.jpg")
    
    cap.release()

# 根据你的 ls -l 结果：
# OG000209 -> /dev/video18
# OG000228 -> /dev/video20
test_cam(18, "OG000209")
test_cam(20, "OG000228")