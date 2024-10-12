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

8. 进入设置，清除小猿口算缓存!!!（多多清除缓存!!!，有许多不成功的原因来自于此）
![alt text](/doc/img/773b1be382d61dfe65f13b421a8e6f3b.png)

- 教程视频

https://github.com/cr4n5/XiaoYuanKouSuan/issues/31#issue-2579180244

9. 按照方案二教程视频 找到类似url重放修改为https://leo.fbcontent.cn/bh5/leo-web-oral-pk/exercise_*.js

10.  重放响应body中，采用上传文件的方式，上传仓库中的[exercise.js](/exercise.js)

11.  pk 场中任意答案都会判定正确，使用连点器即可

### 运用python

见[原文档](/README.md)

## Q&A :question:

- 建议使用app version 3.93.2 [详情见](https://github.com/cr4n5/XiaoYuanKouSuan/issues/74)
- 运用HttpCanary时，出现白屏现象即仓库内exercise.js需要更新，可自行运行python进行更新exercise.js
