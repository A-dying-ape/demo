# coding=utf-8
"""
最近遇到一个json字符串解析失败的问题，原因是json里面的":,这个三个符合在搞鬼，报错如下：
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: ...
json.decoder.JSONDecodeError: Expecting ',' delimiter: ...
json.decoder.JSONDecodeError: Expecting ':' delimiter: ...
对json字符串解析失败处理方法，能解决95%以上的问题，还有5%可能自己还没遇到过奇葩字符串，如果大家有遇到欢迎给位留言，最后如果有帮助到你，点个赞支持一下博主谢谢啦~
"""
import json
import re
import sys


sys.setrecursionlimit(1000000)


def deal_json_invaild(text):
    if type(text) != str:
        raise Exception("参数接受的是字符串类型")
    # text = re.search(r"\{.*\}", text).group()
    text = re.sub(r"\n|\t|\r|\r\n|\n\r|\x08|\\", "", text)
    try:
        json.loads(text)
    except json.decoder.JSONDecodeError as err:
        temp_pos = int(re.search(r"\(char (\d+)\)", str(err)).group(1))
        temp_list = list(text)
        while True:
            if temp_list[temp_pos] == "\"" or "}":
                if temp_list[temp_pos - 1] == "{":
                    break
                elif temp_list[temp_pos - 1] == (":" or "{") and temp_list[temp_pos - 2] == ("\"" or ":" or "["):
                    break
                elif temp_list[temp_pos] == "|\n|\t|\r|\r\n|\n\r| ":
                    temp_list[temp_pos] = re.sub(temp_list[temp_pos], "", temp_list[temp_pos])
                    text = "".join(temp_list)
                elif temp_list[temp_pos] == "\"":
                    temp_list[temp_pos] = re.sub(temp_list[temp_pos], "“", temp_list[temp_pos])
                    text = "".join(temp_list)
                elif temp_list[temp_pos] == "}":
                    temp_list[temp_pos - 1] = re.sub(temp_list[temp_pos], "\"", temp_list[temp_pos])
                    text = "".join(temp_list)
                    temp_pos -= 1
            temp_pos -= 1
        return deal_json_invaild(text)
    else:
        return text