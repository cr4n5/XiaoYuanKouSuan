# XiaoYuanKouSuan

方案三

## 所需 :hammer_and_wrench:

1. root 的安卓设备，虚拟机也可(lsposed,magisk 等) :iphone:
2. python3(非必须) :snake:
3. adb(非必须) :electric_plug:

## 使用 :hammer_and_wrench:

- [安卓模拟器使用教程](README_EMULATOR.md)

[软件及模块](https://xuanrandev.lanzouw.com/b00qc8yij) 密码：5qiw

1. 下载所有需要的软件以及模块，
2. 安装HttpCanary证书模块到Magisk并重启
3. 安装HttpCanary，证书那步安装失败先跳过去。
4. 打开爱玩机工具箱，在导航->应用相关->小黄鸟证书修复中修复小黄鸟证书问题。
5. 打开小黄鸟证书设置，选择添加根证书至系统，这里会申请root权限记得同意。
6. 安装好TrustMeAlready模块并勾选你要抓包的软件。
7. 重启

以上内容来自 酷安@XuanRan_Dev

以下使用方式二选一

### 运用HttpCanary

8. 进入设置，清除小猿口算缓存
    ![alt text](/doc/img/773b1be382d61dfe65f13b421a8e6f3b.png)

- 教程视频

https://github.com/cr4n5/XiaoYuanKouSuan/issues/31#issue-2579180244

1. 按照方案二教程视频 找到类似url重放修改为https://leo.fbcontent.cn/bh5/leo-web-oral-pk/exercise_*.js

2.  重放响应body中，采用上传文件的方式，上传仓库中的[exercise.js](/exercise.js)

3.  pk 场中任意答案都会判定正确，使用连点器即可 ps：有人提的 pr 把 adb shell 命令方式改了，有点影响速度，后续会修改，故此次更新不包含模拟点击

### 运用python

见[原文档](/README.md)
