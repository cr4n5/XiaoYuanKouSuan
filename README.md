# XIaoYuanKouSuan

小猿口算, 采用抓包方式获取题目和答案, 通过 adb 模拟滑动操作，比机器视觉识别更快更准确！

![Language](https://img.shields.io/badge/language-python-blue?logo=python)
![Stars](https://img.shields.io/github/stars/cr4n5/XiaoYuanKouSuan.svg)
![Forks](https://img.shields.io/github/forks/cr4n5/XiaoYuanKouSuan.svg)
![Issues](https://img.shields.io/github/issues/cr4n5/XiaoYuanKouSuan.svg)
![Platform](https://img.shields.io/badge/platform-Android-green?logo=android)

## 目录

- [演示视频](#演示视频):movie_camera:
- [碎碎念 :thought_balloon:](#碎碎念-thought_balloon)
- [环境配置 :hammer_and_wrench:](#环境配置-hammer_and_wrench)
- [代码修改 :pencil2:](#代码修改-pencil2)
- [使用 :hammer_and_wrench:](#使用-hammer_and_wrench)
- [Q&A :question:](#Q&A-question)
- [贡献 :sparkles:](#贡献-sparkles)

## 演示视频:movie_camera:

https://github.com/user-attachments/assets/e9ccfa25-4bdd-4b43-855c-af4a045dcb00

## 碎碎念 :thought_balloon:

代码有点屎山哈哈哈哈，抛砖引玉, 有问题欢迎提 issue :bug:

## 环境配置 :hammer_and_wrench:

1. 已 root 的安卓设备(lsposed 等) :iphone:
2. python3​ (version >= 3.10) :snake:
3. adb :electric_plug:

## 代码修改 :pencil2:

> [!NOTE]
>
> 我们已在 [8d05233](https://github.com/cr4n5/XiaoYuanKouSuan/commit/8d0523390cdb09cbcb52bb7f80b8a9c795043f4c) 变更中增进了对不同分辨率设备的`实验性`支持，将借助 adb 自动获取设备当前分辨率并计算以进行适当缩放，因为您可以不用变更 `str_to_xy()` 函数；若该实验性支持未正常运作，请尝试性变更 [number_command.py](https://github.com/cr4n5/XiaoYuanKouSuan/blob/main/number_command.py) 中的 `BASE_COORDINATES ` 值，并将 `swipe_screen(command_str, base_resolution)` 函数中的 `base_resolution` 替换为您的设备当前分辨率。

根据设备分辨率修改坐标（同元组内坐标连续滑动）

```python
BASE_COORDINATES = {
    "1": [[1480, 1050], [1440, 1470]],
    "2": [[1255, 1100], [1700, 1100], [1255, 1470], [1700, 1470]],
    "3": [[1344, 1040], [1600, 1200], [1270, 1323], [1635, 1379], [1249, 1588]],
    "4": [[1716, 1274], [1245, 1296], [1450, 1030], [1450, 1466]],
    "5": [[1558, 1020], [1290, 1211], [1600, 1348], [1300, 1472]],
    "6": [[1533, 1027], [1265, 1428], [1663, 1439]],
    ">": [[[1350, 1080], [1545, 1172], [1295, 1297]]],
    "<": [[[1578, 1058], [1308, 1231], [1560, 1292]]],
    "=": [[[1284, 1122], [1700, 1122], [1280, 1300], [1700, 1300]]]
}
```

借助 adb 获取、修改、恢复当前设备分辨率：

```shell
# 查看当前分辨率
adb shell wm size
#还原默认分辨率
adb shell wm size reset
# 更改分辨率为 1800x2880
adb shell wm size 1800x2880
```

根据所需更改每个题目间隔时间

```python
def answer_write(answer):

    for i in range(len(answer)):
        number_command.swipe_screen(answer[i])
        # time.sleep(0.16)
        time.sleep(0.3)
```

## 使用 :hammer_and_wrench:

1. 安装依赖

   ```shell
   pip install -r requirements.txt
   ```

2. 配置已 root 设备

   借助 [TrustMeAlready](https://github.com/ViRb3/TrustMeAlready/releases) 模块禁用 app 的 SSL 加密连接以获得始文

3. 配置 adb

   打开设置-开发者选项- usb 调试后，键入指令

   ```shell
   adb devices
   ```

   ```shell
   # 正确返回以下格式
   List of devices attached
   98c54df9        device
   ```

   以确认 adb 是否在本机正确配置成功并连接

4. 配置设备代理

   通过这种方式，可以将移动设备的网络请求全部转发至脚本端。

   - 确保脚本端设备与移动端设备在同一局域网下

   - 获取脚本端设备 ip 地址

     （下文中，脚本端设备以 Windows 为例，移动端设备以 Xiaomi MIUI 为例）

     键入指令

     ```shell
     ipconfig
     ```

     返回内容中，`无线局域网适配器 WLAN ` 下的 `IPv4`  地址即为脚本端设备 ip 地址。

     例如：`192.168.31.113`（下文以此为例）。

   - 设置移动端网络

     对移动端 WiFi 项进行设置，更改其代理为 `手动`，并键入主机名为上面获取到的 ip 地址（如 192.168.31.113），端口为 `8080`，保存即可。

5. 运行脚本

   运行格式为：

   ```shell
   python main.py -H <host> -P <port>
   ```

   绝大部分情况下，直接运行以下即可：

   ```shell
    python main.py -H 0.0.0.0 -P 8080
   ```

   正常情况下，您将看到控制台开始输出大量请求日志，那么您应该离成功不远了。

   至此，您可以操作移动端设备给对方来点小小的技术震撼了lol。

## Q&A :question:

- 运行提示 `ADB 未找到，请先安装 ADB 工具`？

  请检查当前设备是否正确安装 adb 工具，需将 adb 添加至设备环境变量（亦可以修改代码手动指定 adb 路径）。
## 贡献 :sparkles:

本库仍在不断更新完善与丰富功能当中，欢迎您共同参与！

感谢以下贡献者对项目的支持与付出：

<p align="center">
    <a href="https://github.com/krahets/hello-algo/graphs/contributors">
        <img width="770" src="https://contrib.rocks/image?repo=cr4n5/XiaoYuanKouSuan&max=100&columns=16" />
    </a>
</p>