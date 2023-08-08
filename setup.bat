@echo off
setlocal

rem ����Ƿ�װ��Python 3.9
python --version 2>NUL
if %errorlevel% neq 0 (
    echo û�м�⵽��װ��Python 3.9��
    echo �밴���²��谲װPython 3.9��

    echo 1. ���� https://www.python.org/downloads/release/python-390/
    echo 2. ���ز�����Python 3.9�İ�װ����
    echo 3. �ڰ�װ�����У���ȷ����ѡ��Add Python 3.9 to PATH��ѡ�
    echo 4. ��ɰ�װ���������д��������ļ��Լ�����

    pause
    exit
) else (
    rem ����Ƿ�װ��pip
    pip --version 2>NUL
    if %errorlevel% neq 0 (
        echo û�м�⵽��װ��pip��
        echo ����Ϊ����װpip�����Ե�...

        rem ���ز�����get-pip.py�԰�װpip
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python get-pip.py

        rem ��װ��ɺ�ɾ��get-pip.py
        del get-pip.py
    ) else (
        echo �Ѽ�⵽��װ��Python 3.9��pip��
    )

    rem ����Ƿ����requirements.txt�ļ�
    if exist requirements.txt (
        echo ���ڸ���requirements.txt��װPython������...

        rem ʹ���廪pip����װ������
        pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
    ) else (
        echo û���ҵ�requirements.txt�ļ��������ᰲװ�κ������⡣
    )

    echo ��װ��ɡ�
    pause
    exit
)
