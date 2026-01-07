import cv2
import numpy as np
import  os

def calculate_red_area(image_path):
    # 0. 先檢查檔案是否存在
    if not os.path.exists(image_path):
        print(f"錯誤：找不到檔案！請檢查路徑：{image_path}")
        return 0, 0

    # 1. 讀取圖片
    img = cv2.imread(image_path)
    
    # 防呆：確認是否讀取成功
    if img is None:
        print("錯誤：檔案存在但 OpenCV 無法讀取 (可能是格式不支援或路徑含中文)")
        return 0, 0
    
    # 2. 轉換到 HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 3. 定義紅色的範圍 (紅色在 HSV 會跨越 0 和 180，所以要設兩組)
    # 下限紅色
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    # 上限紅色
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    
    # 4. 產生遮罩
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2
    
    # 5. 計算紅色像素點數量
    red_pixels = cv2.countNonZero(mask)
    
    # 6. 換算面積 (假設圖片寬度 = A4 21cm)
    img_height, img_width = img.shape[:2]
    
    # 計算一個像素代表幾公分 (Scaling Factor)
    pixel_per_cm = img_width / 21.0
    area_per_pixel = (1 / pixel_per_cm) ** 2
    
    # 總面積
    real_area = red_pixels * area_per_pixel
    
    return real_area, img_width

# 使用範例
area, width = calculate_red_area('test1.jpg')
print(f"圖片寬度: {width} px")
print(f"紅色墨水面積約: {area:.2f} cm^2")