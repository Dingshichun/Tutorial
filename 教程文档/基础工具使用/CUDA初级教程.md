# CUDA 初级教程
### (1) CUDA 简介
​1. ​什么是 CUDA(Compute Unified Device Architecture，统一计算设备架构)​​：是 NVIDIA 推出的并行计算平台和编程模型，允许开发者利用 GPU 的并行处理能力加速计算。
​​核心概念​​：
* ​主机（Host）​​：CPU 及其内存。
* ​​设备（Device）​​：GPU 及其显存。
* ​​线程（Thread）​​：GPU 上的最小执行单元。
* ​​线程块（Block）​​：一组线程的集合。
* ​​网格（Grid）​​：多个线程块的集合（本文指的都是一维网格）。一个核函数（kernel）所启动的所有线程称为一个网格（grid），同一个网格上的线程共享相同的全局内存空间，网格是线程结构的第一层次。网格又分为很多线程块（block），一个线程块包含很多线程，这是第二个层次。32 个线程为一组 warp，这是第三个层次。
* ​​核函数（Kernel）​​：在 GPU 上运行的并行函数。核函数的声明包括 `__global__ ，__device__ , __host__` 。`__global__`声明的核函数在 device 上执行，在主机 host 上调用，调用时需要使用<<<grid,block>>>来指定核函数要执行的线程数量，比如调用核函数 helloworld<<<2,3>>>()，表示网格中有 2 个线程块，每个线程块包含 3 个线程。每一个线程都要执行核函数，并且每个线程会分配唯一的线程号 thread ID，这个 ID 值可以通过核函数的内置变量 threadIdx 来获得。核函数的返回类型只能是 void ，不支持可变参数。**使用 `__global__` 定义的核函数是异步的，意味着主机 host 不会等待核函数执行完毕就会执行下一步。**
`__device__`声明的是在 device 上执行，且仅可以从 device 中调用，不可以和`__global__`同时使用。
`__host__`声明的在 host 上执行，仅可以从 host 上调用，一般省略不写，不可以和`__global__`同时使用，但是可以和`__device__`一起使用，此时函数会在 host 和 device 都编译。  
当数据被转移到 GPU 的全局内存之后，主机端调用核函数在 GPU 上进行计算。一旦内核被调用，控制权立刻被传回主机，所以，核函数在 GPU 上运行时，主机可以执行其它函数。因此，内核和主机是异步的。可以使用 `cudaDeviceSynchronize();` 进行同步，即等待内核执行完毕才将控制权传回主机。
* 网格上的索引。
整个网格被分为不同的块，每个块内又分为不同的线程，相当于矩阵的嵌套，包括一维和二维矩阵。同一个块中的线程可以相互协作，不同块的则不能。  
CUDA 有一些 dim3 类型的变量，是基于 uint3 定义的整数型向量，用来表示维度，如下：  
blockIdx 是线程块在网格中的索引，包含 blockIdx.x、blockIdx.y、blockIdx.z  
threadIdx 是每个块内的线程索引，包含 threadIdx.x、threadIdx.y、threadIdx.z  
blockDim 是线程块的维度，包含 blockDim.x、blockDim.y、blockDim.z  
gridDim 是网格的维度。  
比如网格大小定义为 3 行 2 列，那么 gridDim.x = 2,gridDim.y = 3,未定义的 gridDim.z 默认为 1。  
知道网格的大小和每个块所包含的线程数，就可以根据上面的变量计算出每个线程在整个网格中的索引，线程在网格中的索引也是从 0 开始的。  
上面这些是 dim3 类型的变量，是基于 uint3 定义的整数型向量，用来表示维度
```c++
// 文件名为 checkIndex.cu
__global__ void checkIndex()
{
    printf("threadIdx:(%d, %d, %d)  blockIdx(%d, %d, %d) blockDim(%d, %d, %d) gridDim(%d, %d, %d)\n",
    threadIdx.x, threadIdx.y, threadIdx.z, blockIdx.x, blockIdx.y, blockIdx.z, 
    blockDim.x, blockDim.y, blockDim.z, gridDim.x, gridDim.y, gridDim.z);
}
int main()
{
    int nElem = 6; // 定义总的线程数
    // 定义网格和块结构
    dim3 block(3); // 每个块包含三个线程，一维数据，即一行三列
    dim3 grid((nElem+block.x-1)/block.x); // 计算网格结构，这里是块的数量，结果为 2

    // 检查网格和块的维度
    printf("grid.x %d, grid.y %d,grid.z %d \n",grid.x,grid.y,grid.z);
    printf("block.x %d, block.y %d,block.z %d \n",block.x,block.y,block.z);
    checkIndex<<<grid,block>>>(); // 调用核函数，必须指定网格大小和块大小
    cudaDeviceReset(); // 重设，清理内存
    return 0;
}
// 使用 nvcc checkIndex -o checkIndex 编译后得到可执行文件 checkIndex.exe(windows中)
// 运行的结果如下：没懂为什么 blockIdx 先是 blockIdx(1, 0, 0) 而不是 blockIdx(0, 0, 0)
// grid.x 2, grid.y 1,grid.z 1 
// block.x 3, block.y 1,block.z 1
// threadIdx:(0, 0, 0)  blockIdx(1, 0, 0) blockDim(3, 1, 1) gridDim(2, 1, 1)
// threadIdx:(1, 0, 0)  blockIdx(1, 0, 0) blockDim(3, 1, 1) gridDim(2, 1, 1)
// threadIdx:(2, 0, 0)  blockIdx(1, 0, 0) blockDim(3, 1, 1) gridDim(2, 1, 1)
// threadIdx:(0, 0, 0)  blockIdx(0, 0, 0) blockDim(3, 1, 1) gridDim(2, 1, 1)
// threadIdx:(1, 0, 0)  blockIdx(0, 0, 0) blockDim(3, 1, 1) gridDim(2, 1, 1)
// threadIdx:(2, 0, 0)  blockIdx(0, 0, 0) blockDim(3, 1, 1) gridDim(2, 1, 1)
```

```c++
#include <stdio.h>

__global__ void helloworld()
{
    // 只针对一维网格
    const int gdim=gridDim.x; // 网格的维度
    const int bdim=blockDim.x; // 线程块的维度
    const int bid=blockIdx.x; //线程块的索引值
    const int tid=threadIdx.x; // 单个线程块中线程的索引值
    const int id=threadIdx.x+blockIdx.x*blockDim.x; // 整个网格中线程的索引值
}
int main()
{
    // 调用核函数要指定 grid_size 和 block_size，比如：helloworld <<<grid_size,block_size>>> ();
    // 一维网格中 grid_size = gridDim.x，block_size = blockDim.x，没有指定的维度默认为 1，
    // 比如 gridDim.y = gridDim.z = 1,blockDim.y = blockDim.z = 1
    
    // "helloworld << <2, 3 >> > ();"表示有两个 block ，每个 block 中有三个线程，
    // 那么线程块的索引值就是 0,1，
    // 单个线程块中线程的索引值就是 0,1,2，整个网格中就有 2X3=6 个索引值，
    // 整个网格中线程的索引值就是 0,1,2,3,4,5。
	helloworld << <2, 3 >> > (); 
	cudaDeviceSynchronize(); //同步函数，强制主机端程序等待所有的核函数执行结束
	return 0;
}
```

2. 环境配置  
* 安装 NVIDIA 驱动​​：确保 GPU 支持 CUDA。  
* 安装 CUDA Toolkit​(​验证安装：命令行运行 nvidia-smi 和 nvcc --version)
* IDE 配置​​：推荐使用 Visual Studio（Windows）或 VS Code（Linux）

### (2) GPU 内存
1. 内存简介  
* 每一个线程有自己的私有本地内存（Local Memory），所有线程都可以访问全局内存（global memory）。
* 共享内存定义在线程块中，每个线程块包含共享内存（shared memory），可以被线程块中所有线程共用，其生命周期和线程块一致。
* 可编程内存是可以编程来控制的内存，还有不可编程内存。
* 所有线程都可以访问、读取常量内存和纹理内存，但是不能写，因为这些内存是只读的。
* 寄存器是速度最快的内存空间，核函数内不加修饰地声明的变量就储存在寄存器中，核函数中定义的有常数长度的数组也存储在寄存器上。如果一个线程的变量太多，寄存器就会溢出，就会使用到本地内存（就是常说的显存）来帮忙存储多出来的变量，会严重降低效率。
* 共享内存是线程块内所有线程都可见的，所以就存在竞争问题，也可以通过共享内存进行通信，为了避免内存竞争，可以使用 `void __syncthreads();`，相当于在线程块执行时的一个障碍点，当线程块内所有线程都执行到此障碍点时才能进行下一步的计算。但是频繁使用会影响内核执行效率。
* 共享内存被划分为相同大小的内存块，实现高速并行访问。bank 是其中一种划分方式，每个内存块就是 banks。在 cpu 中，访问内存是访问某个地址，获得地址上的数据。但是在这里，是一次性访问 banks 数量的地址，获得这些地址上的所有数据，并逻辑映射到不同的 bank 上，类似内存读取的控制。

2. 内存管理  
CUDA 会使用到 CPU 和 GPU 内存，CPU 内存的分配和释放是标准的，比如 new 和 delete ，malloc 和 free。GPU 上的内存分配和释放则使用 CUDA 提供的库函数。这里主要涉及全局内存（显存）和共享内存的管理。
```c++
// GPU 全局内存分配和释放
cudaError_t cudaMalloc(void **devPtr,size_t size); // GPU 内存分配
cudaError_t cudaFree(void **devPtr); // GPU 内存释放

// Host 内存分配和释放，Host 内存属于 CPU 内存，传输速度比普通 CPU 内存快很多
cudaError_t cudaMallocHost(void **devPtr,size_t size); // Host 内存分配
cudaError_t cudaFreeHost(void **devPtr); // Host 内存释放

// 统一（Unified）内存分配和释放，该内存可以同时被 CPU 和 GPU 访问
cudaError_t cudaMallocManaged(void **devPtr,size_t size,unsigned int flags=cudaMemAttachGlobal); 
// flags=cudaMemAttachGlobal 表示内存可以被任意处理器访问，即包括 GPU 和 CPU 
// flags=cudaMemAttachHost 表示内存只可以被 CPU 访问
cudaError_t cudaFree(void **devPtr); // 内存释放
```

3. 流式多处理器  
* GPU 硬件的核心是流式多处理器 SM（streaming multiprocessor），SM 的核心组件包括 CUDA 核心、共享内存、寄存器等，可以并发执行上百个线程，并发能力取决于 SM 所拥有的资源数。 
* 当一个 kernel 被执行时，它 grid 中的线程块被分配到 SM 上，一个线程块只能在一个 SM 上被调度。SM 一般可以调度多个线程块，有可能一个 kernel 的各个线程块被分配多个 SM ，所以 grid 只是逻辑层，SM 才是执行的物理层。

### (3) nvcc 编译流程
1. nvcc 分离全部源代码为：主机（Host）代码和设备（device）代码。主机代码是 C/C++ 代码，设备代码是 C/C++ 拓展语言编写。
2. nvcc 先将设备代码编译为 PTX（parallel thread execution）伪汇编代码，再将 PTX 代码编译为二进制的 cubin 目标代码。 PTX 是 CUDA 平台为基于 GPU 的通用计算而定义的虚拟机和指令集。 
在将源代码编译为 PTX 代码时，需要用选项 `-arch=compute_XY` 指定一个虚拟架构的计算能力，用以确定代码中能够使用的 CUDA 功能，X、Y 分别代表计算能力的主、次版本号，指定的计算能力应该小于等于自己 GPU 的计算能力，否则不能编译。  
在将 PTX 代码编译为 cubin 代码时，需要用选项 `-code=sm_ZW` 指定一个真实架构的计算能力，用以确定可执行文件能够使用的 GPU 。  
虚拟架构更像是对应用所需的 GPU 功能的声明，虚拟架构应尽可能选择低的以适配更多实际 GPU，真实架构应该尽可能选择高以充分发挥 GPU 的性能。
3. 可以指定多个 GPU 版本编译，使得编译出的可执行文件可以在多 GPU 执行。执行方法是 `-gencode arch=compute_XY -code=sm_XY` ，注意这里是 `-code=sm_XY`， 执行该指令需要 CUDA 版本支持 7.0 以上的计算能力，否则会报错。过多地指定计算能力，会增加编译时间和可执行文件的大小。
### (4) CUDA 程序的基本框架
1. 包含头文件以及定义核函数
2. 定义主函数。主函数中要实现内存的分配和释放等操作。
2.1 设置 GPU 设备  
2.2 分配主机和设备内存  
2.3 初始化主机中的数据  
2.4 数据从主机复制到设备  
2.5 调用核函数在设备中进行计算  
2.6 将计算得到的数据从设备传给主机  
2.7 释放主机和设备内存  

```c++
// 2.1 设置 GPU
#include <stdio.h>
// 核函数不支持 C++ 的 iostream，只支持 C 语言的 stdio

int main()
{
    // 检测计算机 GPU 数量
    int iDeviceCount=0; 
    cudaError_t error=cudaGetDeviceCount(&iDeviceCount); 
    if(error != cudaSuccess || iDeviceCount==0)
    {
        printf(" no CUDA campatable GPU found\n");
        exit(-1);
    }
    else 
    {
        printf("the count of GPU is :%d \n",iDeviceCount);
    }

    // 设置执行的 GPU 设备
    int iDev=0;
    error=cudaSetDevice(iDev);
    if(error != cudaSuccess)
    {
        printf("fail to set GPU 0 for computing \n");
        exit(-1);
    }
    else
    {
        printf("set GPU 0 for computing \n");
    }
    return 0;
}
```

```c++
// cuda 内存管理函数和标准 C 语言类似，标准 c 语言有 malloc、memcpy、memset、free，cuda 对应的是 cudaMalloc、cudaMemcpy、cudaMemset、cudaFree。
```

### (5) CUDA 的线程索引
1. 线程索引简介
cuda 中的 block 和 grid 就相当于把线程划分为一些相同大小的矩阵，比如网格中 grid=2,block=2 就表示有两个 block 线程块，每个 block 中的线程数量为 2，所以总的线程数就是 2X2=4 。如果 grid=(3,3),block=(2,2),表示网格中有 3X3=9 个 block，每个 block 中有 2X2=4 个线程，总的线程数就是 3X3X2X2=36 个。作图很容易理解。  
2. 网格循环
GPU 提供的网格大小远远小于实际数据的大小时候，就要使用循环来依次处理数据的不同位置。比如一张 16X16 的图像，网格的线程数只有 4X4(假设 grid=(2,2),block=(2,2))，所以这个网格一次只能处理图像的一小部分，需要处理 16 次。
```c++
// 线程在整个网格中的索引
int tx=cuda.blockIdx.x*cuda.blockDim.x+cuda.threadIdx.x
int ty=cuda.blockIdx.y*cuda.blockDim.y+cuda.threadIdx.y

// x、y 方向上一次循环要移动的长度
int stride_x=blockDim.x*gridDim.x
int stride_y=blockDim.y*gridDim.y

// 循环处理
for(int y=ty;y<height;y+=stride_y)
{
    for(int x=tx;x<width;x+=stride_x)
    {
        // 要执行的操作
    }
}
```

### (6)核函数
**注意**：不同于 C 语言的调用，所有 CUDA 核函数的启动都是异步的。CUDA 内核调用完成后，控制权立刻返回给 CPU。  
**核函数类型限定符**：`__global__`（在设备端执行，可从主机端调用，也可从有一定计算能力的设备端调用）、`__device__`（在设备端执行，仅能从设备端调用）、`__host__`（主机端执行，仅能在主机端调用），`__device__ 和 __host__`可以一起使用，这样的函数可以同时在主机和设备端进行编译。  
**核函数的限制**：只能访问设备内存；必须具有 void 返回类型；不支持可变数量的参数；不支持静态变量；显示异步行为。
**核函数的性能**：改变网格和块的大小配置会影响内核性能；传统的核函数实现一般不能获得最佳性能；对于给定的核函数，尝试不同的网格和线程块大小可能获得更好的性能。

