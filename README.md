## 关于 [ProcessOn](https://www.processon.com/i/5ad16f4be4b0518eacae31fb)

非常好用的思维导图网站，不仅支持思维导图，还支持流程图、原型图、UML 等。比我之前用的百度脑图强多了。

直接登录网站就可以编辑，非常适合我在图书馆公用电脑学习使用。

但是，它是付费的，免费用户只能存放 9 个文件。

本程序实现自动增加你的文件数量，理论上可以无限增加，哈哈。

效果图：

![pic.gif](https://upload-images.jianshu.io/upload_images/5690299-dccea23b5bc05529.gif?imageMogr2/auto-orient/strip)

增加到 100 个左右就够了，不要搞太多，以免引起官方注意。
请低调使用，不要涉及商业行为。

--------------

三个月后，果然引起官方注意，现在注册时，需要通过[腾讯验证码](https://007.qq.com/online.html?ADTAG=capt.head)。

没有找到完美的解决方案。

目前，用  selenium 模拟注册时，需要手动滑动验证码。

但是，这腾讯滑动验证码很智能：同一IP，短时间内，连续 4 次注册后，就无法通过验证码了。所以，必须引入 IP 代理池（目前没引入）。

## 用法

- 安装依赖: pip install requests bs4 selenium
- 将项目中的 chromedriver.exe 放到你的 Python 安装目录下的 Script 文件夹中。
- 在你的 processon 的账号中心找到你的邀请链接 url。
- 运行脚本 python processon.py 。

## 扩充文件数思路

我发现在用户的账号中心有这样的东西：

![邀请链接](https://upload-images.jianshu.io/upload_images/5690299-8c3228ba522c1855.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

当然，可以找别人通过自己链接注册，然而，还是自己动手，丰衣足食。

我细细观察，又发现注册只需邮箱，然后它会发一条验证链接给注册邮箱，只要点击链接后就注册完成，而邀请链接的用户就可以增加 3 个文件数了！

所以，我找了一个临时邮箱网站，[https://temp-mail.org/zh/](https://temp-mail.org/zh/)，它会给你一个邮箱账号，类似 free sms online。然后拿这个邮箱账号去注册，再回到临时邮箱网站验证就可以了。

## 编程思路

### 1. 先来看看注册表单

![注册](https://upload-images.jianshu.io/upload_images/5690299-892570595b743eed.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

用户名我用随机生成的 7 位数加上邮箱后缀，密码、昵称都是随机产生的 7 位数。

```python
user = str(random.randint(1000000, 9999999))
fullname = str(random.randint(1000000, 9999999))
password = str(random.randint(1000000, 9999999))
```

### 2. 更改 temp mail 邮箱

![更改邮箱表单](https://upload-images.jianshu.io/upload_images/5690299-75166eb422410257.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

抓包发现：post 表单数据需要 csrf 字段。所以 post 前先用 get 方法，从响应中提取 csrf 字段值。

### 3. 获取注册验证链接

这步比较简单，在 temp mail 的「刷新」标签获取到邮件，get 请求进去，在中响应中提取出注册验证链接，最后请求注册验证链接即可。

需要注意的是注册验证邮件 temp mail 不一定马上就能收到，所以我写了个死循环，不断检测是否收到邮件，当收到邮件时才跳出。

### 4. 存在问题

速度太慢了，而且需要手动验证腾讯滑动验证码。

连续第 4 次注册之后，这个 ip 就暂时无法通过验证码（这个，引入 IP 代理池后，应该得到解决）。