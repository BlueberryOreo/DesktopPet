@echo off
setlocal

rem 检测是否安装了Python 3.9
python --version 2>NUL
if %errorlevel% neq 0 (
    echo 没有检测到安装的Python 3.9。
    echo 请按以下步骤安装Python 3.9：

    echo 1. 访问 https://www.python.org/downloads/release/python-390/
    echo 2. 下载并运行Python 3.9的安装程序。
    echo 3. 在安装过程中，请确保勾选“Add Python 3.9 to PATH”选项。
    echo 4. 完成安装后，重新运行此批处理文件以继续。

    pause
    exit
) else (
    rem 检测是否安装了pip
    pip --version 2>NUL
    if %errorlevel% neq 0 (
        echo 没有检测到安装的pip。
        echo 正在为您安装pip，请稍等...

        rem 下载并运行get-pip.py以安装pip
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python get-pip.py

        rem 安装完成后删除get-pip.py
        del get-pip.py
    ) else (
        echo 已检测到安装的Python 3.9和pip。
    )

    rem 检查是否存在requirements.txt文件
    if exist requirements.txt (
        echo 正在根据requirements.txt安装Python依赖库...

        rem 使用清华pip镜像安装依赖库
        pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
    ) else (
        echo 没有找到requirements.txt文件，将不会安装任何依赖库。
    )

    echo 安装完成。
    pause
    exit
)
