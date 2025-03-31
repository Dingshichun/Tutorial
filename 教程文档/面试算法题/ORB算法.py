# ORB算法特征匹配示例代码
# ORB (Oriented FAST and Rotated BRIEF) 是一种高效的特征检测和描述算法
# 它结合了 FAST 特征检测器和 BRIEF 描述符，具有旋转不变性和尺度不变性
# 适用于实时应用和资源受限的环境

import cv2
import numpy as np

# 读取图像
img1 = cv2.imread("dsc.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("dsc.jpg", cv2.IMREAD_GRAYSCALE)

# 创建ORB对象
orb = cv2.ORB_create()

# 检测关键点并计算描述符
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# 使用Brute Force匹配器进行特征匹配
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)

# 根据距离排序
matches = sorted(matches, key=lambda x: x.distance)

# 绘制匹配结果
img3 = cv2.drawMatches(
    img1,
    kp1,
    img2,
    kp2,
    matches[:10],
    None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
)

# 显示结果
cv2.imshow("ORB Feature Matching", img3)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存结果
cv2.imwrite("orb_matching_result.jpg", img3)
