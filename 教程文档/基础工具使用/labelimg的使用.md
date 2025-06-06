# labelimg 的使用
### 1、简介和安装
labelimg 是一个可视化的图像标定工具。它是用 Python 编写的，并将 Qt 用于其图形界面。批注以 PASCAL VOC 格式（ImageNet 使用的格式）另存为 XML 文件。此外，它还支持 YOLO 格式。Faster R-CNN，YOLO，SSD 等目标检测网络所需要的数据集，均需要借此工具标定图像中的目标。   
使用 anaconda 创建一个新的环境，打开 anaconda prompt，激活刚才创建的环境。首先确保安装 pip ，然后使用 pip 安装 labelimg 的依赖库，最后再安装 labelimg
```
pip install PyQt5
pip install pyqt5-tools
pip install lxml

pip install lebelimg
```
安装完成之后，在命令行输入 `labelimg` 即可启动 labelimg。

### 2、labelimg 的使用
labelimg 的使用比较简单，看图形界面即可了解，主要注意下面几点：
* labelimg 的标注模式分为 VOC 和 YOLO 两种，两种模式下生成的标注文件分别为 .xml 文件和 .txt 文件，因此在进行标注前需要优先选择好标注的模式。  
* 使用 labelimg 以 VOC 模式进行标注产生的标注文件如下，与 YOLO 标注模式产生的类别标签不同， .xml 标注文件不需要将类别文件单独进行存放，因为其中已经包含了标注锚框的位置信息和类别信息。  
* 使用 labelimg 以 YOLO 模式进行标注产生的标注文件如下， classes.txt 文件中存放的是类别标签，标签文件中以类别+锚框的位置坐标信息进行保存，文件中有几行则说明对应的标注图像中有几个锚框。  

### PASCAL VOC 格式和 YOLO 格式
1. VOC格式  
VOC 格式生成的标注文件是 .xml 文件，其内容如下。  
假如一张图中只有一种目标，且这种目标有两个，并且全部都进行了标注，那么就有 3 个 <object> ，<name>就是目标对应的类别，<bndbox> 中是所标注的矩形框的左上和右下坐标。
```
<annotation>
  <folder>image</folder>
  <filename>1.webp</filename>
  <path>C:\Users\世兰丁\Desktop\image\1.webp</path>
<source>
  <database>Unknown</database>
</source>
<size>
  <width>3840</width>
  <height>2160</height>
  <depth>3</depth>
</size>
<segmented>0</segmented>
<object>
  <name>0</name>
  <pose>Unspecified</pose>
  <truncated>0</truncated>
  <difficult>0</difficult>
<bndbox>
  <xmin>1305</xmin>
  <ymin>549</ymin>
  <xmax>1946</xmax>
  <ymax>2130</ymax>
</bndbox>
</object>
<object>
  <name>0</name>
  <pose>Unspecified</pose>
  <truncated>0</truncated>
  <difficult>0</difficult>
<bndbox>
  <xmin>1960</xmin>
  <ymin>513</ymin>
  <xmax>2619</xmax>
  <ymax>2130</ymax>
</bndbox>
</object>
</annotation>
```

2. YOLO 格式  
YOLO 格式生成的标签文件是 txt 格式的文本，每幅图对应一个 txt 文件，文件中一行内容对应一个目标，还有单独生成一个类别文档 classes.txt，其内容是所有内别，一行代表一个类别。  
比如有一幅图 img.jpg，其中有两个目标，类别是 0。标注后得到的 txt 文件就是 img.txt，内容如下。两行就代表两个目标，每行的第一列代表类别，第二和第三列代表这个目标的矩形框中心坐标 x 和 y 归一化后的值，第四和第五列代表的是矩形框的宽 width 和高 height 归一化后的值。其中 x 和 width 根据原图的 width 进行归一化，y 和 height 则根据原图的 height 进行归一化。
```
# 注释：类别、矩形框中心的 x 坐标归一化后的值、矩形框中心的 y 坐标归一化后的值、矩形框的宽 width 归一化后的值、矩形框的高 height 归一化后的值
0 0.423698 0.623380 0.165104 0.732870
0 0.596224 0.609259 0.170052 0.743519
```
还会生成类别文件 classes.txt ，其内容如下，有几个类别就有几行，每行就是类别。
```
0
1
```