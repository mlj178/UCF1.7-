通过IDA反编译，发现 0x123740 是另一个不相关的函数，而不是 Transform.get_position
通过IDA找到了真正的RVA
之前 transformGetPos 崩溃的根本原因是 RVA 地址错了— 用了 0x123740 而不是 dump.cs 中的 0x3F42B0。IDA 反编译的 0x10123740 根本不是 Transform.get_position，而是另一个不相关的函数。




思路混乱了，最后还是参考DLL的小工具代码

根本不知道哪个类，哪个属性，存放了yaw和pitch。


请问我们完成了哪些功能，都是通过什么方法完成的。

已完成的核心功能：
    鼠标开镜检测

        方法：调用游戏内置的 Input_GetMouse 函数（RVA 0xACFB20）判断左键状态。

    敌我识别

    玩家与世界坐标获取

    锁敌角度计算

    视角写入

    真实 Yaw 定位







