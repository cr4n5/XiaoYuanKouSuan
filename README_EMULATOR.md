# 安卓模拟器

在电脑上使用安卓模拟器运行该项目

## 目录

- [必备软件和工具包](#必备软件和工具包)
- [安装安卓模拟器](#安装安卓模拟器)
- [安装ADB](#安装ADB)
- [安装KitsumeMask](#安装KitsumeMask(即app-debug.apk))
- [安装LSPosed](#安装LSPosed(即LSPosed-v1.9.2-7024-zygisk-release.zip))
- [安装TrustMeAlready](#安装TrustMeAlready(即TrustMeAlready-v1.11-release.apk))
- [配置模拟器网络环境](#配置模拟器网络环境)
- [运行代码](#运行代码)

## 必备软件和工具包
1. 安卓模拟器(笔者测试了Mumu模拟器)
2. platform-tools(adb.exe) [下载链接](https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/platform-tools-latest-windows.zip)
3. app-debug.apk [下载链接](https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/app-debug.apk)
4. TrustMeAlready-v1.11-release.apk [下载链接](https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/TrustMeAlready-v1.11-release.apk)
5. LSPosed-v1.9.2-7024-zygisk-release.zip [下载链接](https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/LSPosed-v1.9.2-7024-zygisk-release.zip)

## 安装安卓模拟器
1. 下载并安装你喜欢的安卓模拟器
2. 在模拟器设置中打开root权限, 打开读取电脑文件, 重启模拟器

## 安装ADB
1. 解压platform-tools-latest-windows.zip
2. 将platform-tools目录添加到系统环境变量(不会就百度)

## 安装KitsumeMask(即app-debug.apk)
1. 在模拟器中安装app-debug.apk
2. 打开Kitsume Mask
3. 点击Magisk右侧的安装键
<div align=center><img src="https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/111.png"></div>
4. 选择安装到Recovery, 选择直接安装
<div align=center><img src="https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/222.png"></div>
<div align=center><img src="https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/333.png"></div>
<div align=center><img src="https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/444.png"></div>
5. 出现All Done后直接关闭模拟器并重启(不要点击Kitsume Mask内的重启键)
<div align=center><img src="https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/555.png"></div>
6. 回到Kitsume Mask主页, 进入设置, 打开Magisk选项卡下的Zygisk和MagiskHide选项
<div align=center><img src="https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/666.png"></div>
7. 重启Kitsume Mask

## 安装LSPosed(即LSPosed-v1.9.2-7024-zygisk-release.zip)
1. 将LSPosed-v1.9.2-7024-zygisk-release.zip复制到模拟器内
2. 打开Kitsume Mask中的模块选项, 选择从本地安装
<div align=center><img src="https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/777.png"></div>
3. 出现Done后重启模拟器(不要点击Kitsume Mask内的重启键)
<div align=center><img src="https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/888.png"></div>
4. 解压出LSPosed-v1.9.2-7024-zygisk-release.zip中的manager.apk并安装到模拟器中

## 安装TrustMeAlready(即TrustMeAlready-v1.11-release.apk)
1. 直接在模拟器中安装TrustMeAlready-v1.11-release.apk
2. 打开LSPosed的模块选项卡
<div align=center><img src="https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/999.png"></div>
3. 进入TrustMeAlready的设置, 打开启用模块选项
<div align=center><img src="https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/10.png"></div>
<div align=center><img src="https://github.com/jhy354/READMEIMAGE/blob/master/XiaoYuanKouSuan/11.png"></div>

## 配置模拟器网络环境
1. 获取电脑的内网ip(不会就百度)
2. 进入模拟器的WLAN设置, 在高级设置中配置代理服务器为电脑内网ip, 端口为8080

## 运行代码
[详见README.md](https://github.com/cr4n5/XiaoYuanKouSuan/blob/main/README.md)
1. 安装依赖文件
2. 运行main.py