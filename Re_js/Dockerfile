# 使用官方的 Python 基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到工作目录
COPY ./plan_three.py /app

# 安装所需的 Python 包
RUN pip install --no-cache-dir mitmproxy

# 暴露端口
EXPOSE 8080


# 运行脚本
CMD ["python", "plan_three.py", "--host", "0.0.0.0", "--port", "8080"]