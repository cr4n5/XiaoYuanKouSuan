from mitmproxy.tools.main import mitmdump
import argparse
import sys
import adb_manager
import config

def main():
    # 检查 ADB 是否安装
    adb_manager.ADBManager.check_adb_installed()

    # 参数解析
    parser = argparse.ArgumentParser(description="Mitmproxy script")
    parser.add_argument("-P", "--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help="Host to listen on")
    parser.add_argument("-AI", "--adb-ip", type=str, help="IP and port for ADB wireless connection (e.g., 192.168.0.101:5555)")
    parser.add_argument("-CD", "--clear-data", action='store_true', help="To clear app's all data")
    args = parser.parse_args()

    # 无线调试
    if args.adb_ip:
        try:
            adb_manager.ADBManager.connect(args.adb_ip)
        except Exception as e:
            print(f"ADB 连接失败: {e}")
            sys.exit(1)

    # 清除数据
    if args.clear_data:
        try:
            adb_manager.ADBManager.clear_and_restart_app(config.APP_PACKAGE_NAME)
        except Exception as e:
            print(f"清除应用数据失败: {e}")
            sys.exit(1)

    sys.argv = ["mitmdump", "-s", "response_handler.py", "--listen-host", args.host, "--listen-port", str(args.port)]
    mitmdump()

if __name__ == "__main__":
    main()