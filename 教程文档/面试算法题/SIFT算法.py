# SIFT 算法特征匹配
# SIFT (Scale-Invariant Feature Transform) 是一种用于检测和描述局部特征的算法
# 它具有尺度不变性和旋转不变性，适用于图像匹配、物体识别等任务
# SIFT 算法在 OpenCV 中实现时可能需要额外安装 opencv-contrib-python 库
# 安装命令：pip install opencv-contrib-python

import numpy
import cv2

image1 = cv2.imread("dsc.jpg", cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread("dsc.jpg", cv2.IMREAD_GRAYSCALE)

sift = cv2.SIFT_create()  # 创建 SIFT 对象
keypoints1, descriptors1 = sift.detectAndCompute(image1, None)  # 检测关键点和计算描述符
keypoints2, descriptors2 = sift.detectAndCompute(image2, None)  # 检测关键点和计算描述符

# 使用FLANN匹配器进行特征匹配
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(descriptors1, descriptors2, k=2)

# 筛选匹配点（使用最近邻与次近邻比值）
good_matches = []
for match1, match2 in matches:
    if match1.distance < 0.75 * match2.distance:
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
cv2.imshow("SIFT Feature Matching", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存结果
cv2.imwrite("sift_matching_result.jpg", result)
