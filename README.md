# UPC-nCoV-Auto-Submitter
中国石油大学（华东）疫情防控通自动填报python版本

## 说明
**本人不对因为滥用此程序造成的后果负责，请在合理且合法的范围内使用本程序。**

**本程序仅供研究交流使用，如果填报表中任意情况发生变化，比如地点发生变化，请务必在程序运行之前手动打卡。**

## 依赖库
```
requests
configparser
yagmail 
```

## 运行方法
1. 安装依赖库
2. 修改`info.ini`为自己的信息，`[Information]`中修改自己的账号，密码，邮件(可选，打卡完成邮件提醒),支持多账号打卡，填写时`,`隔开，`[SMTP]`处修改为自己的SMTP信息
3. 执行` python main.py `即可完成自动填报
4. 微信公众号推送需要[配置serverchan](https://sct.ftqq.com/)。修改程序中`SERVERCHAN_SECRETKEY`即可

## 服务器定时任务
参考crontab 定时任务的配置

## TODO
- [x] 基本功能
- [x] 邮件提醒
- [x] vx公众号提醒
- [ ] github action直接运行

## History
- 2020/12/8 基本功能和邮件功能实现
- 2021/03/25 微信公众号推送，修复了多账号可能存在的一些bug