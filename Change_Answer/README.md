# XIaoYuanKouSuan

## 所需 :hammer_and_wrench:

1. root 的安卓设备，虚拟机也可(lsposed,magisk 等) :iphone:
2. python3(非必须) :snake:
3. adb(非必须) :electric_plug:

## 使用 :hammer_and_wrench:

[软件及模块](https://xuanrandev.lanzouw.com/b00qc8yij) 密码：5qiw

1. 下载所有需要的软件以及模块，
2. 安装HttpCanary证书模块到Magisk并重启
3. 安装HttpCanary，证书那步安装失败先跳过去。
4. 打开爱玩机工具箱，在导航->应用相关->小黄鸟证书修复中修复小黄鸟证书问题。
5. 打开小黄鸟证书设置，选择添加根证书至系统，这里会申请root权限记得同意。
6. 安装好TrustMeAlready模块并勾选你要抓包的软件。
7. 重启

以上内容来自 酷安@XuanRan_Dev

- 教程视频

https://github.com/cr4n5/XiaoYuanKouSuan/issues/31#issue-2579180244

- pk url头
https://xyks.yuanfudao.com/leo-game-pk/android/math/pk/match?

- 练习场 url头
https://xyks.yuanfudao.com/leo-math/android/exams?

### 替换所有题目答案为1

- 正则表达式匹配(pk与练习场同理)
- `"answer":\s*".*?"` 匹配为 `"answer": "1"`
- `"answers":\s*\[.*?\]` 匹配为 `"answers": ["1"]`

### 将题目减少到1题，答案为1，一直滑动手指即可0.01s！！！

- 正则表达式匹配(pk与练习场同理)
- `"questionCnt":\s*\d+` 匹配为 `"questionCnt": 1`
- `"questions":\s*\[.*\],` 匹配为 `"questions": [{"id": 1,"content": "9+\\\\square=12","answer": "1","userAnswer": null,"answers": ["1"],"script": null,"wrongScript": null,"status": 0,"errorState": 0,"costTime": 0}],`