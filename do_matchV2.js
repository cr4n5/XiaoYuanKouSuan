console.log("Script loaded successfully ");
var WebView = Java.use('android.webkit.WebView')
WebView.loadUrl.overload('java.lang.String').implementation = function(url) {
    if (url.startsWith("javascript:") && url.includes("dataDecrypt")) {
        var base64EncodedString = url.match(/"([^"]+)"/)[1]; // 匹配出Base64字符串
        // 我知道有两个地方会获得超长字符串，一个是pk题目及答案，另一个没记下来，带有dataDecrypt的是pk题目及答案
        // 当字数超过1000时说明有可能是试题，输出出来
        if(base64EncodedString.length > 100){
            send(base64EncodedString)
            // 此处获取python传过来的数据, 并替换掉原来的url的base64EncodedString部分
            var data = recv('input', function(value) {
                // py这样写的script.post({'type': 'input', 'payload': result}), 这里显示Received: [object Object],所以这里要取value.payload
                url = url.replace(base64EncodedString, value.payload);
                console.log('Replaced: ' + url);
            });
        }
    }
    // 继续执行原来的 loadUrl 方法
    return this.loadUrl(url)
}