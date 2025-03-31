import cv2
import numpy as np

# 生成测试图像（孤立点位于中心）
image = np.zeros((5, 5), dtype=np.uint8)
image[2, 2] = 1  # 孤立点

# 定义结构元素 E（击中）和 F（击不中）
E = np.array([[0, 0, 0],
              [0, 1, 0],
              [0, 0, 0]], dtype=np.uint8)

F = np.array([[1, 1, 1],
              [1, 0, 1],
              [1, 1, 1]], dtype=np.uint8)

# 腐蚀操作
hit = cv2.erode(image, E)
miss = cv2.erode(1 - image, F)  # 补集腐蚀

# 击中与击不中变换
result = hit & miss

print("原图像：\n", image)
print("击中区域：\n", hit)
print("击不中区域：\n", miss)
print("最终结果：\n", result)