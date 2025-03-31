# 使用 pytorch 实现剪枝

import torch
import torch.nn as nn
import torchvision.models as models

model = models.mobilenet_v3_small(pretrained=True)
model.eval()  # 切换到评估模式


# 方法 1 ：将低于阈值的权重置零。权重剪枝，手动实现
"""
def prune_weights(model, threshold=0.1):
    for name, param in model.named_parameters():
        if "weight" in name:
            mask = torch.abs(param) > threshold
            param.data *= mask  # 将低于阈值的权重置零


prune_weights(model.fc, threshold=0.2)  # 示例：剪枝全连接层权重
"""

# 方法 2 ：通道剪枝（卷积层专用）
"""
import torch.nn.utils.prune as prune

# 对第一个卷积层进行 30% 通道剪枝
# ln_structured实现结构化剪枝，适用于卷积层
prune.ln_structured(
    model.conv1, 
    name="weight", 
    amount=0.3, 
    n=2,      # 每 2 个通道保留 1 个
    dim=0     # 按通道维度剪枝
)
"""

# 方法 3 ：随机剪枝（pytorch 内置）
"""
import torch.nn.utils.prune as prune

prune.random_unstructured(
    model.fc2, 
    name="weight", 
    amount=0.1  # 随机剪枝 10% 权重
)
"""

# 剪枝后处理。包括模型微调、剪枝后模型保存等
# 1、剪枝可能导致精度下降，需在少量数据上微调：
"""
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

for epoch in range(5):
    for inputs, labels in dataloader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
"""

# 2、在测试集上验证准确率、稀疏性等指标：
"""
total = 0
correct = 0
with torch.no_grad():
    for data in test_loader:
        images, labels = data
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print(f"Accuracy: {100 * correct / total:.2f}%")
"""