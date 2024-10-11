
import base64
from mitmproxy import http
import execjs
import json
from mitmproxy.tools.main import mitmdump
import sys
import argparse

from mitmproxy import http

def response(flow: http.HTTPFlow) -> None:
    # 检查 URL 是否匹配特定的模式
    if flow.request.pretty_url.startswith("https://leo.fbcontent.cn/bh5/leo-web-oral-pk/exercise_") and flow.request.pretty_url.endswith(".js"):
        # 检查响应的内容类型是否为 JavaScript
        if "text/javascript" in flow.response.headers.get("Content-Type", ""):
            # 获取原始的 JavaScript 内容
            original_js = flow.response.text
            
            # 保存原始的 JavaScript 内容
            with open("original.js", "w") as f:
                f.write(original_js)
            # 在这里修改 JavaScript 内容
            # 查询 isRight: 后的字符串
            modified_js = original_js.replace("originalFunction", "modifiedFunction")
            
            # 设置修改后的 JavaScript 内容
            flow.response.text = modified_js

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mitmproxy script")
    parser.add_argument("-P", "--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help="Host to listen on")
    args = parser.parse_args()

    sys.argv = ["mitmdump", "-s", __file__, "--listen-host", args.host, "--listen-port", str(args.port)]

    mitmdump()
