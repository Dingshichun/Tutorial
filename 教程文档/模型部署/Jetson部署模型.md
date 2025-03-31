# 训练好的模型部署到 Jetson nano
## 一、环境配置与依赖安装
### 1. JetPack系统安装
- 使用 SD Card Formatter工具将官方镜像（如 JetPack 4.6+ ）烧录至TF卡，确保包含 CUDA 10.2 及TensorRT 7.1+ 环境
- 关键配置项：
  ```bash
  # 关闭自动熄屏（防止开发中断）
  gsettings set org.gnome.desktop.session idle-delay 0
  # 扩展 SWAP 内存（处理大模型必备）
  sudo fallocate -l 8G /swapfile && sudo chmod 600 /swapfile
  sudo mkswap /swapfile && sudo swapon /swapfile
  ```
### 2. 深度学习环境搭建
* 安装 PyTorch ARM 版本（需匹配 JetPack 版本）：
```bash
wget https://nvidia.box.com/shared/static/p57jwntv436lfrd78inwl7iml6p13fzh.whl
pip3 install torch-1.8.0-cp36-cp36m-linux_aarch64.whl
```
* 验证 CUDA 可用性：
```python
import torch
print(torch.cuda.is_available())  # 应返回 True
```
## 二、模型转换和优化流程
### 1、导出 ONNX 格式
* 使用 PyTorch 导出模型为 ONNX 格式：
```python
model = torch.load('mobilenet_v2.pth')
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(model, dummy_input, "mobilenet.onnx",
                 input_names=['input'], output_names=['output'],
                 dynamic_axes={'input': {0: 'batch'}, 'output': {0: 'batch'}})
```
* 关键验证步骤
```bash
polygraphy run mobilenet.onnx --trt
```
### 2、tensorRT 引擎生成
* 使用 trtexec 工具量化（Jetson Nano 建议 FP16）：
```bash
/usr/src/tensorrt/bin/trtexec \
  --onnx=mobilenet.onnx \
  --saveEngine=mobilenet_fp16.engine \
  --fp16 \
  --workspace=2048
```
* 如果使用 INT8 量化需校准数据集：
```bash
trtexec --onnx=mobilenet.onnx --int8 --calib=calibration_images/
```

## 三、部署实现方案
### 方案 1 :使用 jetson-inference 库
1、编译 C++ 接口
```bash
cd jetson-inference/build
cmake ../ -DCMAKE_INSTALL_PREFIX=~/.local
make -j$(nproc)
```
2、python 调用示例：
```pyhton
from jetson_inference import imageNet
net = imageNet(model="mobilenet_fp16.engine", labels="labels.txt")
class_id, confidence = net.Classify(image)
```
### 方案 2 :原生 TensorRT C++ 部署
```c++
#include <NvInferRuntime.h>
// 初始化推理引擎
nvinfer1::IRuntime* runtime = nvinfer1::createInferRuntime(logger);
nvinfer1::ICudaEngine* engine = runtime->deserializeCudaEngine(engineData, engineSize);
nvinfer1::IExecutionContext* context = engine->createExecutionContext();

// 内存分配
void* buffers[2];
cudaMalloc(&buffers[0], inputSize);
cudaMalloc(&buffers[1], outputSize);

// 执行推理
context->executeV2(buffers);
```
### 方案 3 ：Triton Server 部署
1、模型仓库配置
```
mobilenet/
├── config.pbtxt
└── model.engine
```
2、config.pbtxt 内容：
```protobuf
name: "mobilenet"
platform: "tensorrt_plan"
max_batch_size: 8
input { name: "input", data_type: TYPE_FP32, dims: [3, 224, 224] }
output { name: "output", data_type: TYPE_FP32, dims: [1000] }
```

## 四、常见问题解决
### 1、​模型精度下降

* 检查 ONNX 转换时的 opset 版本是否匹配
* 验证 TensorRT 的 FP16/INT8 量化是否引入误差
### 2、​内存不足错误

```bash
sudo rmmod nvgpu  # 临时释放显存
sudo swapoff /swapfile && sudo swapon /swapfile  # 重置交换空间
```
### 3、​低帧率问题

* 使用 NVIDIA Nsight Systems 分析推理耗时
* 启用 TensorRT 的 tactic 选择器优化：
```c
config->setTacticSelector(MyTacticSelector());
```