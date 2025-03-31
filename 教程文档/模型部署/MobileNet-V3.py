import torch

model = torch.load("MB-v3-15-all.pth")
model.eval()
# scripted_model = torch.jit.script(model)
# scripted_model.save("MB-V3.pt")


from torch.quantization import get_default_qconfig

qconfig = get_default_qconfig("fbgemm")  # CPU量化推荐fbgemm[6](@ref)
model.qconfig = qconfig

torch.quantization.prepare(model, inplace=True)  # [1,6](@ref)

from torch.utils.data import DataLoader

# 准备校准数据集（需包含模型输入分布特征）
calib_dataset = ...  # 校准数据集，这里没有具体实现
calib_loader = DataLoader(calib_dataset, batch_size=32, shuffle=False)

with torch.no_grad():
    for inputs, _ in calib_loader:
        model(inputs)  # 前向传播自动收集量化参数[6](@ref)

torch.quantization.convert(model, inplace=True)  # [1,6](@ref)

torch.save(model.state_dict(), "quantized_model.pth")  # [1,6](@ref)
