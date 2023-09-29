# build.py

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile, QIODevice
import subprocess
import os

def copy_resources():
    # 复制配置文件、图标和样式文件到临时目录
    subprocess.run(['cp', '-r', 'config', 'dist'])
    subprocess.run(['cp', '-r', 'icon', 'dist'])
    subprocess.run(['cp', '-r', 'style', 'dist'])

def main():
    # 执行pyinstaller打包命令
    subprocess.run(['pyinstaller', '--onefile', '--noconsole', 'campuslogin.py'])

    # 复制相关资源文件
    copy_resources()

    # 创建软链接以访问配置文件
    os.symlink(os.path.join('dist', 'config'), os.path.join('dist', 'config'))

if __name__ == "__main__":
    main()
