# SURF (Speeded Up Robust Features) 算法特征匹配示例
# 该示例使用 OpenCV 的 xfeatures2d 模块来实现 SURF 特征检测和描述
# SURF 算法在 OpenCV 中实现时可能需要额外安装 opencv-contrib-python 库

import cv2
import numpy as np

# 读取图像
image1 = cv2.imread("dsc.jpg", cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread("dsc.jpg", cv2.IMREAD_GRAYSCALE)

# 创建SURF对象
surf = cv2.xfeatures2d.SURF_create(hessianThreshold=400)

# 检测关键点和计算描述子
keypoints1, descriptors1 = surf.detectAndCompute(image1, None)
keypoints2, descriptors2 = surf.detectAndCompute(image2, None)

# 使用FLANN匹配器进行特征匹配
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(descriptors1, descriptors2, k=2)

# 筛选良好匹配
good_matches = []
for match1, match2 in matches:
    if match1.distance < 0.7 * match2.distance:
        good_matches.append(match1)

# 绘制匹配结果
result = cv2.drawMatches(
    image1,
    keypoints1,
    image2,
    keypoints2,
    good_matches,
    None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
)

# 显示结果
cv2.imshow("SURF Feature Matching", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存结果
cv2.imwrite("surf_matching_result.jpg", result)
