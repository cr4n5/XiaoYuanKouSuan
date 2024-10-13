import subprocess

class ADBManager:
    @staticmethod
    def check_adb_installed():
        try:
            result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                raise RuntimeError(result.stderr)
        except FileNotFoundError:
            raise RuntimeError("ADB 未找到，请先安装 ADB 工具。")

    @staticmethod
    def connect(adb_ip):
        result = subprocess.run(["adb", "connect", adb_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "connected" not in result.stdout:
            raise RuntimeError(result.stderr)
        print(f"已连接到 {adb_ip}")

    @staticmethod
    def clear_and_restart_app(package_name):
        subprocess.run(["adb", "shell", "am", "force-stop", package_name])
        subprocess.run(["adb", "shell", "pm", "clear", package_name])
        subprocess.run(["adb", "shell", "am", "start", "-n", f"{package_name}/.activity.RouterActivity"])
        print(f"已清除缓存并重启应用: {package_name}")