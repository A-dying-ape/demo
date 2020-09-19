# coding=utf-8
import json
import re
import sys


sys.setrecursionlimit(1000000)


def deal_json_invaild(text):
    """
    json字符串异常处理
    :param text: 文本
    :return: 可以被json的文本
    """
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