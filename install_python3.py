# -*- coding:utf-8 -*-
"""
1.wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
2.mkdir -p /usr/local/python3
3.tar -zxvf Python-3.6.1.tgz
4.cd Python-3.6.1
5../configure --prefix=/usr/local/python3
6.make
7.make install
8.ln -s /usr/local/python3/bin/python3 /usr/bin/python3
9.vim ~/.bash_profile
10.export PATH=$PATH:$HOME/bin:/usr/local/python3/bin
"""
import os
import re


def main():
    os.system("wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0a1.tgz")
    os.system("sudo mkdir -p /usr/local/python3")
    os.system("sudo tar -zxvf Python-3.9.0a1.tgz")
    os.system("cd Python-3.9.0a1.tgz")
    os.system("sudo ./configure --prefix=/usr/local/python3")
    os.system("sudo make")
    os.system("sudo make install")
    os.system("sudo ln -s /usr/local/python3/bin/python3 /usr/bin/python3")
    export_path = "export PATH=$PATH:$HOME/bin:/usr/local/python3/bin"
    with open("~/.bash_profile", "r") as f:
        content = f.read()
    if not re.search(r"export PATH=$PATH:$HOME/bin:/usr/local/python3/bin", content, re.IGNORECASE):
        with open("~/.bash_profile", "a+") as f:
            f.write(export_path)
    os.system("source ~/.bash_profile")


if __name__ == "__main__":
	main()