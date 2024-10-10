# XIaoYuanKouSuan

小猿口算

## 碎碎念

代码有点屎山哈哈哈哈，抛砖引玉, 有问题欢迎提issue

## 环境配置

1. root的安卓设备(lsposed等)
2. python3
3. adb

## 代码修改

```python
def str_to_xy(str):
    match str:
        case "1":
            return [[1480, 1050], [1440, 1470]]
        case "2":
            return [[1255, 1100], [1700, 1100], [1255, 1470], [1700, 1470]]
        case "3":
            return [[1344, 1040], [1600, 1200], [1270, 1323], [1635, 1379], [1249, 1588]]
        case "4":
            return [[1716, 1274],[1245,1296],[1450,1030],[1450,1466]]
        case "5":
            return [[1558,1020],[1290,1211],[160,1348],[1300.1472]]
        case "6":
            return [[1533,1027],[1265,1428],[1663,1439]]
        case ">":
            return [[[1350, 1080], [1545, 1172], [1295, 1297]]]
        case "<":
            return [[[1578,1058],[1308,1231],[1560,1292]]]
        case "=":
            return [[[1284, 1122], [1700, 1122]],[[1280, 1300], [1700, 1300]]]
```

根据设备分辨率修改坐标（同元组内坐标连续滑动）

```python
def answer_write(answer):
    
    for i in range(len(answer)):
        number_command.swipe_screen(answer[i])
        # time.sleep(0.16)
        time.sleep(0.3)
```

根据所需更改每个题目间隔时间

## 使用

1. 安装依赖

```shell
pip install -r requirements.txt
```

2. 配置root设备

采用trust me already禁用app ssl

3. 配置adb

- 打开开发者选项中的usb调试
    
```shell
adb devices
```

4. 配置安卓代理

WIFI设置代理为电脑ip和端口(8080)

5. 运行

```shell
python main.py
```
