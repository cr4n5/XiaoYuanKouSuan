import requests
import re

print("************************************************************")
print("项目地址:https://github.com/cr4n5/XiaoYuanKouSuan")
print("************************************************************")

url="https://leo.fbcontent.cn/bh5/leo-web-oral-pk/exercise.html#/"
response = requests.get(url)

pattern = r"https://leo\.fbcontent\.cn/bh5/leo-web-oral-pk/exercise_.*\.js"
match = re.search(pattern, response.text)

def extract_function_name(responsetext):
    match = re.search(r"(?<=isRight:)[^,]*?\(.*?\).*?(?=\|)", responsetext)
    return match.group() if match else None

def update_response_text(flow, responsetext, funname):
    print(f"找到函数名: {funname}")
    updated_text = responsetext.replace(funname, f"{funname}||true")
    
    # 保存js到exercise.js
    with open("exercise.js", "w", encoding="utf-8") as f:
        f.write(updated_text)
        print("exercise.js文件已保存。")


if match:
    print("匹配到指定的 URL:", match.group())
    js_url = match.group()
    js_response = requests.get(js_url)
    funname = extract_function_name(js_response.text)
    if funname:
        update_response_text(js_response, js_response.text, funname)
    else:
        print("未找到匹配的函数名，无法进行替换。")

input("Enter键退出...")