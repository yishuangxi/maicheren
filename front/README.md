# 糗事hybrid

@(糗事)


1. APP通过读取定义好的值来操作
**APP内调起分享：** 读取前端定义的三个值：
```javascript
window.shareImg = '图片URL'
window.shareTitle = '标题'
window.shareContent = '内容'
window.shareUrl = '分享链接'
```

2. APP通过改写前端的prompt函数来调用
```javascript
//前端通过拼接'__native_call=>'和一个JSON字符串的作为prompt的参数来调用prompt
function a (){}
var callback = function(){}
var json = {
    method:'reqNative',
    action:'',
    modul:'',
    callbackId:'callback', //前端定义的一个回调接口
    args:'', // 参数(也是JSON 字符串)
}
var jsonString = JSON.stringify(json)
prompt('__native_call=>'+jsonString)
```

2.1 账户相关

```javascript
modul:account
action:{
    info//(重新加载URL)
    open_user_profile//跳转个人主页
    login//（登录）
}
args: //［如果action是open_user_profile］
｛
    uid
 ｝

```

2.2 分享相关

```javascript
modul:share
action: {
    share_qzone
    share_qq
    share_weixin
}
args:
    //分享是［share_qzone， share_qq]的时候
    {
        title
        url
        description
        imgurl
    }
    //分享是［share_weixin]的时候
    {
        title
        url
        description
        imgurl,
        scene//（1分享到朋友圈，2分享给朋友）,
        thumbdata//(base64的图片)
    }
```

2.3 充值相关

```javascript
    action:'charge',
    modul:'charge',
```

2.4 跳转直播
```javascript
    action = 'live'
    modul = 'open_live'
```
