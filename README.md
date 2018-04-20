## 关于 [ProcessOn](https://www.processon.com/i/5ad16f4be4b0518eacae31fb)

非常好用的思维导图网站，不仅支持思维导图，还支持流程图、原型图、UML 等。比我之前用的百度脑图强多了。

直接登录网站就可以编辑，非常适合我在图书馆公用电脑学习使用。

但是，它是付费的，免费用户只能存放 9 个文件。

## 扩充文件数思路

我发现在用户的账号中心有这样的东西：

![邀请链接](https://upload-images.jianshu.io/upload_images/5690299-8c3228ba522c1855.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

当然，可以找别人通过自己链接注册，然而，最后还是自己动手，丰衣足食。

我细细观察，又发现注册只需邮箱，然后它会发一条验证链接给注册邮箱，只要点击链接后就注册完成，而邀请链接的用户就可以增加 3 个文件数了！

所以，我找了一个临时邮箱网站，[https://temp-mail.org/zh/](https://temp-mail.org/zh/)，它会给你一个邮箱账号，然后拿这个邮箱账号去注册，再回到临时邮箱网站验证就可以了。

## 编程思路

1. 先来看看注册表单

![注册](https://upload-images.jianshu.io/upload_images/5690299-892570595b743eed.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

用户名我用随机生成的 7 位数加上邮箱后缀，密码、昵称都是随机产生的 7 位数。

```python
'email': user + '@carbtc.net',
'pass': str(random.randint(1000000, 9999999)),
'fullname': str(random.randint(1000000, 9999999))
```

需要注意网站通过 cookies 识别出邀请链接，所以在提交表单前需要 get(邀请链接url)，再 post 提交表单，两次请求在同一个 session，这样才能共享 cookies 。

2. 更改 temp mail 邮箱

![更改邮箱表单](https://upload-images.jianshu.io/upload_images/5690299-75166eb422410257.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

抓包发现：post 表单数据需要 csrf 字段。所以 post 前先用 get 方法，从响应中提取 csrf 字段值。

3. 获取注册验证链接

这步比较简单，在 temp mail 的「刷新」标签获取到邮件，get 请求进去，在中响应中提取出注册验证链接，最后请求注册验证链接即可。

需要注意的是注册验证邮件 temp mail 不一定马上就能收到，所以我写了个死循环，不断检测是否收到邮件，当收到邮件时才跳出。