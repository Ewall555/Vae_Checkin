# Vae_Checkin
许嵩个人app Vae+的自动签到脚本

## 功能描述
1. 每日自动进行签到
2. 支持多用户签到，多个Cookie之间采用`&&`手动分割
3. 【可选】支持将签到消息推送至Server酱，Pushplus，Bark， Wxpusher

## 使用方法

### 1. 添加 Cookie 至 Secrets
- 手机使用抓包工具抓取Cookie
- 在项目页面，依次点击`Settings`-->`Secrets`-->`Actions`-->`New repository secret`
- 建立名为`VAE_COOKIE`的 secret，值为抓取的Cookie(例如：JSESSID=xxxxxxxx)，点击`Add secret`添加
- 多用户签到，多个Cookie之间采用`&&`分割填入

### 2. 启用 Actions
- 在项目页面，依次点击`Actions`-->`Vae`-->`Run workflow`-->`Run workflow`以激活Actions

- Workflow开启后，每日0时00分自动执行。

## 3. 消息推送 （可选）
本项目支持将签到消息推送至第三方平台。
### 3.1 Pushplus
将消息推送至[Pushplus](https://www.pushplus.plus) 需配置`token`，在本仓库创建名为`PUSHPLUS_TOKEN`的secret，将`token填入

### 3.2 Server酱
将消息推送至[Server酱](https://sct.ftqq.com/sendkey) 需配置`SendKey`，在本仓库创建名为`SERVERCHAN_SENDKEY`的secret，将`SendKey`填入

### 3.4 Bark
将消息推送至[Bark](https://github.com/Finb/Bark) 需配置`DeviceKey`，在本仓库创建名为`BARK_DEVICEKEY`的secret，将`DeviceKey`填入

### 3.5 Wxpusher
将消息推送至[Wxpusher](https://wxpusher.zjiecode.com) 需配置`apptoken`，在本仓库创建名为`WXPUSHER_APPTOKEN`的secret，将`apptoken`填入

另需配置uid将消息推送至你指定的Wxpusher用户上，在本仓库创建名为`WXPUSHER_UID`的secret，将`uid`填入。
