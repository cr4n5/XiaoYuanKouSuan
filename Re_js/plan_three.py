from mitmproxy import http
from mitmproxy.tools.main import mitmdump
import re
import argparse
import sys
def is_target_url(url):
    return re.search(r"leo\.fbcontent\.cn/bh5/leo-web-oral-pk/exercise_.*\.js", url)

def response(flow: http.HTTPFlow) -> None:

    global is_dialog_shown
    url = flow.request.url
    print(f"Response: {flow.response.status_code} {url}")

    if is_target_url(url):
        handle_target_response(flow, url)
    elif "https://xyks.yuanfudao.com/leo-game-pk/android/math/pk/match/v2?" in url:
        if not is_dialog_shown:
            is_dialog_shown = True

def handle_target_response(flow, url):
    print(f"匹配到指定的 URL: {url}")
    responsetext = flow.response.text
    funname = extract_function_name(responsetext)

    if funname:
        update_response_text(flow, responsetext, funname)
    else:
        print("未找到匹配的函数名，无法进行替换。")

def extract_function_name(responsetext):
    match = re.search(r"(?<=isRight:)[^,]*?\(.*?\).*?(?=\|)", responsetext)
    return match.group() if match else None

def update_response_text(flow, responsetext, funname):
    print(f"找到函数名: {funname}")
    updated_text = responsetext.replace(funname, f"{funname}||true")
    flow.response.text = updated_text
    
    # 保存js到exercise.js
    with open("exercise.js", "w", encoding="utf-8") as f:
        f.write(updated_text)
    
    print(f"替换后的响应: {updated_text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="运行 mitmdump")
    parser.add_argument("-P", "--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help="Host to listen on")
    args = parser.parse_args()

    # 运行mitmdump
    sys.argv = ["mitmdump", "-s", __file__, "--listen-host", args.host, "--listen-port", str(args.port)]
    mitmdump()