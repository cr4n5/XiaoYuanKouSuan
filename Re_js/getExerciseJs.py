import re


def replace_and_change_js(file_input, file_output):
    with open(file_input, "r", encoding="utf-8") as f:
        original_js = f.read()
    
    # 查询 isRight: 所在的位置并匹配后面的模式
    pattern = re.compile(r'isRight:\s*([a-zA-Z]{2}\(t\))')
    lines = original_js.splitlines()
    for i, line in enumerate(lines, start=1):
        match = pattern.search(line)
        if match:
            mode = match.group(1)
            print(f"匹配到的模式: {match.group(1)}")
            break
    modified_js = original_js.replace(mode, mode + "|| true")
    with open(file_output, "w", encoding="utf-8") as f:
        f.write(modified_js)

if __name__ == "__main__":
    replace_and_change_js("original.js", "exercise.js")