import requests
import random
import json
import time


PROXY = [{"gH4n2CuU": "http://58.218.201.74:7009"}, {"0K6NThrw": "http://58.218.200.220:5288"}, {"YXOIGwNn": "http://58.218.201.74:4888"}, {"uejNqOhT": "http://58.218.201.74:5884"}, {"mTltbhvd": "http://58.218.201.114:6886"}, {"zwVXKPb5": "http://58.218.200.253:5795"}, {"RCB4tw7q": "http://58.218.201.74:8799"}, {"Q5tbVs8g": "http://58.218.201.122:7598"}, {"ZC1944wl": "http://58.218.200.253:5982"}, {"pbhs8CRi": "http://58.218.201.122:9129"}, {"2tlGURbk": "http://58.218.200.220:4387"}, {"g4MKUYev": "http://58.218.201.122:3082"}, {"yqdcVSgP": "http://58.218.201.74:4700"}, {"LbQ4hAFf": "http://58.218.201.114:5786"}, {"xUyk4vuc": "http://58.218.201.122:7472"}, {"A4J1sl4C": "http://58.218.201.74:7921"}, {"n4JOEAsp": "http://58.218.201.114:2756"}, {"12XVtWKR": "http://58.218.201.122:2740"}, {"5XV0j4eU": "http://58.218.201.114:2945"}, {"I3u9dUBD": "http://58.218.200.253:6254"}, {"8O6nhoc5": "http://58.218.201.114:5813"}, {"plcMSxo6": "http://58.218.201.122:2305"}, {"fInYDe8H": "http://58.218.200.253:5616"}, {"m9y14fUz": "http://58.218.201.114:2225"}, {"l0UYTZ13": "http://58.218.201.114:8551"}, {"ZWkJduMt": "http://58.218.201.114:8685"}, {"aDYCrI74": "http://58.218.201.122:7129"}, {"M12vkspN": "http://58.218.200.253:7788"}, {"KbUdxaLt": "http://58.218.201.74:7233"}, {"GM3NExi4": "http://58.218.200.253:9022"}, {"NAGEFz4J": "http://58.218.200.220:6487"}, {"3zUwqehv": "http://58.218.201.114:6288"}, {"8SkVL94b": "http://58.218.201.122:9154"}, {"xCj4d0o9": "http://58.218.201.74:4911"}, {"8vtj7dGY": "http://58.218.201.74:4381"}, {"3IlSzxa5": "http://58.218.201.74:8005"}, {"DtBY7COT": "http://58.218.201.74:4453"}, {"TORmLdVC": "http://58.218.200.220:2432"}, {"PYGwZaEh": "http://58.218.201.114:8921"}, {"TpOte7cs": "http://58.218.200.253:9103"}, {"4Uj6Fcu2": "http://58.218.201.74:4707"}, {"kez4SPbj": "http://58.218.201.74:4452"}, {"P2JmM3Q9": "http://58.218.200.220:3306"}, {"qfz7WGTn": "http://58.218.201.74:3308"}, {"XP4y8r3U": "http://58.218.201.74:6893"}, {"q6Y491aB": "http://58.218.200.220:3090"}, {"r9yVEkLB": "http://58.218.201.114:4287"}, {"HVfvEqk2": "http://58.218.200.253:6493"}, {"VQJ4YEm7": "http://58.218.201.74:2878"}, {"xED7RQqk": "http://58.218.200.253:8010"}, {"pwyjG8tR": "http://58.218.201.74:7417"}, {"COMkW7xf": "http://58.218.200.253:7449"}, {"jsPUuXlM": "http://58.218.201.74:6603"}, {"2QNkuprK": "http://58.218.201.122:7052"}, {"E9bN6Dfj": "http://58.218.201.114:3524"}, {"RYLGIT9E": "http://58.218.201.122:7722"}, {"R7tlfE0W": "http://58.218.201.74:6564"}, {"UpRmvGEY": "http://58.218.201.74:8080"}, {"0Y4i2WkF": "http://58.218.201.122:2212"}, {"zmBu8Ujb": "http://58.218.201.74:3938"}, {"dHR9y4Fs": "http://58.218.201.74:6237"}, {"C3zNn6dO": "http://58.218.201.74:9191"}, {"pnxN1qMB": "http://58.218.201.114:2589"}, {"o6DpSax2": "http://58.218.201.114:3123"}, {"q4R5zIGU": "http://58.218.201.122:9130"}, {"KYDiCNSk": "http://58.218.200.253:2561"}, {"kjvhCIea": "http://58.218.200.253:3420"}, {"75fuBh86": "http://58.218.201.114:7206"}, {"CWnYsQc4": "http://58.218.200.253:5034"}, {"CHXyxn4W": "http://58.218.201.122:3348"}, {"tl8en7JD": "http://58.218.201.74:5277"}, {"D4SERnZ9": "http://58.218.201.122:4089"}, {"sLz2gv3M": "http://58.218.201.122:8923"}, {"LiwHkNRK": "http://58.218.201.74:6452"}, {"WrIgmbu4": "http://58.218.201.74:2896"}, {"oMWl6hI8": "http://58.218.201.114:6183"}, {"1Me54XtG": "http://58.218.201.74:6541"}, {"0ycVIt3K": "http://58.218.200.253:4406"}, {"njbe9PCW": "http://58.218.201.122:2780"}, {"o4Qk9tcM": "http://58.218.201.122:5434"}, {"VQpAP2JE": "http://58.218.201.114:6329"}, {"g6h1xLEC": "http://58.218.200.220:5280"}, {"QlnO4VmF": "http://58.218.201.74:6342"}, {"nV7JhWIx": "http://58.218.200.253:6520"}, {"w5uA9czg": "http://58.218.201.74:7641"}, {"uxFesgqG": "http://58.218.201.74:7161"}, {"k4lVtI41": "http://58.218.200.253:2988"}, {"Oi4o2Pn4": "http://58.218.201.74:5744"}, {"X5Bl604h": "http://58.218.200.253:9129"}, {"3MPN9knS": "http://58.218.200.220:5795"}, {"zfu6CTRp": "http://58.218.201.74:2446"}, {"YeRgWJPZ": "http://58.218.201.122:9081"}, {"esWBPQrq": "http://58.218.200.220:4562"}, {"9wZPWzSh": "http://58.218.201.114:3942"}, {"6clBgFpG": "http://58.218.201.114:2209"}, {"I56dMcmp": "http://58.218.201.74:6146"}, {"Nu493Ir1": "http://58.218.200.253:8792"}, {"24oPJyNb": "http://58.218.201.122:9135"}, {"XLuv7s20": "http://58.218.200.253:4666"}, {"m7ek9JOF": "http://58.218.201.122:4995"}, {"lgEsvKIM": "http://58.218.201.122:2025"}, {"J0Dqgtin": "http://58.218.201.114:5252"}, {"KnX2Cf8A": "http://58.218.201.122:6642"}, {"4EyoaYdV": "http://58.218.201.74:8641"}, {"7h4Czl8u": "http://58.218.201.74:4009"}, {"wupfz3Uc": "http://58.218.201.122:6925"}, {"vmKIV4yj": "http://58.218.200.220:4423"}, {"d1a6w7bl": "http://58.218.200.220:6544"}, {"iAykZ1xI": "http://58.218.201.114:2918"}, {"ZRi2F89W": "http://58.218.200.220:3103"}, {"QoH1JALf": "http://58.218.201.114:9069"}, {"4Un6DN4w": "http://58.218.200.253:8529"}, {"ftyOwjuX": "http://58.218.200.220:5445"}, {"B4vAhe5s": "http://58.218.200.220:3454"}, {"UpIw8sDa": "http://58.218.200.220:2274"}, {"5Oy1N2PX": "http://58.218.201.74:2488"}, {"bx5HJErR": "http://58.218.201.122:5418"}, {"VpcKgwfs": "http://58.218.201.122:4061"}, {"78xmM1JI": "http://58.218.201.114:5669"}, {"N5OGVmg8": "http://58.218.200.220:3052"}, {"5RPDy92d": "http://58.218.200.253:8305"}, {"PGzYZx6C": "http://58.218.200.253:7975"}, {"HEhIuT4o": "http://58.218.201.122:8552"}, {"Os4TQplL": "http://58.218.201.122:3531"}, {"dgnWCb5L": "http://58.218.200.253:8373"}, {"2Ph7Hqja": "http://58.218.200.220:6384"}, {"DUPVo4b7": "http://58.218.201.114:3492"}, {"mrL9R14Q": "http://58.218.201.122:6423"}, {"zP1Rnk58": "http://58.218.201.122:3359"}, {"3nVOz8gu": "http://58.218.201.74:5434"}, {"wLGBqbDp": "http://58.218.200.220:2559"}, {"P0k4V8on": "http://58.218.201.122:3722"}, {"oXgxku9v": "http://58.218.201.114:5870"}, {"mpfDgSbc": "http://58.218.201.114:7602"}, {"LOj3k9Dp": "http://58.218.201.74:7576"}, {"0wBJj5Sa": "http://58.218.201.114:4021"}, {"ZQ4Vm5S7": "http://58.218.201.122:9128"}, {"TSZkB9Hw": "http://58.218.201.122:6505"}, {"HKfGNyjJ": "http://58.218.201.74:2167"}, {"4Yg0z5cP": "http://58.218.201.114:4713"}, {"AjyEGZaM": "http://58.218.200.253:9201"}, {"Oo9UEXyn": "http://58.218.200.220:5043"}, {"57OaqDGT": "http://58.218.200.253:8912"}, {"Y180epsM": "http://58.218.201.122:3667"}, {"t92F1xmn": "http://58.218.201.74:7440"}, {"VoIB4jhK": "http://58.218.201.122:4650"}, {"vjCM4FUu": "http://58.218.201.122:4202"}, {"8IM4Qf5s": "http://58.218.201.122:7443"}, {"lzyDxKCA": "http://58.218.200.220:6091"}, {"yl4SsLwt": "http://58.218.201.74:5910"}, {"nz9YCfiF": "http://58.218.201.74:8635"}, {"2VTAKtdZ": "http://58.218.201.74:5773"}, {"Zixp8QYC": "http://58.218.201.114:2668"}, {"V1M9OsIp": "http://58.218.201.122:8441"}, {"TZgECAvK": "http://58.218.201.114:5265"}, {"AFsUXSgw": "http://58.218.201.114:6547"}, {"BYgudJps": "http://58.218.201.74:7934"}, {"KvjIrNBU": "http://58.218.201.122:2460"}, {"Mvc1k3Qd": "http://58.218.201.122:2544"}, {"QSrCvNpZ": "http://58.218.201.74:2359"}, {"zRHryTWP": "http://58.218.201.74:4812"}, {"kASTrOBx": "http://58.218.200.220:5178"}, {"3de8tlk1": "http://58.218.200.253:2053"}, {"gnrPYxXG": "http://58.218.200.220:5587"}, {"7P6YzrOy": "http://58.218.201.114:2297"}, {"OzLFJE7Z": "http://58.218.201.74:7748"}, {"HN9EkXpT": "http://58.218.201.122:5473"}, {"dtsUaWy5": "http://58.218.200.253:7953"}, {"TqotQvpe": "http://58.218.201.114:6316"}, {"tD9O4ZnS": "http://58.218.200.220:2877"}, {"enVIchNQ": "http://58.218.200.253:3048"}, {"dwl4iqDo": "http://58.218.201.74:3723"}, {"XklHD0OU": "http://58.218.201.74:3483"}, {"JzTHc0N1": "http://58.218.201.74:3797"}, {"Rg54Qjk2": "http://58.218.201.122:8881"}, {"pmq1kWu3": "http://58.218.200.253:4679"}, {"2nYFl7EK": "http://58.218.200.253:7751"}, {"onhiqM87": "http://58.218.201.114:7575"}, {"JAwL5Yvj": "http://58.218.201.74:6167"}, {"FzEHaquO": "http://58.218.200.253:7173"}, {"z74oRlKX": "http://58.218.200.220:6005"}, {"hJvsuSCg": "http://58.218.201.74:3288"}, {"JyxUmP2M": "http://58.218.201.114:3476"}, {"bzjat7Vs": "http://58.218.201.74:4420"}, {"CyS6xWLq": "http://58.218.200.253:7961"}, {"JihQO250": "http://58.218.201.74:7524"}, {"2GYZvujy": "http://58.218.201.74:5441"}, {"qpQkrgP1": "http://58.218.201.114:6230"}, {"C8DsKX24": "http://58.218.201.122:6229"}, {"9CdF4KQh": "http://58.218.201.114:5695"}, {"Zu6BLUjp": "http://58.218.201.74:4591"}, {"8osSYX5N": "http://58.218.201.114:7635"}, {"GAw9gKN4": "http://58.218.200.220:3163"}, {"omHjPSA8": "http://58.218.201.74:4425"}, {"UBifS57m": "http://58.218.201.122:6435"}, {"wbE4P95q": "http://58.218.201.74:8107"}, {"GC4ZHxWi": "http://58.218.201.122:6728"}, {"0kac1wSi": "http://58.218.200.220:2070"}, {"IXQx4RS3": "http://58.218.201.114:3961"}, {"Pgj1aLyf": "http://58.218.200.220:2239"}, {"Ky349ilv": "http://58.218.201.74:4680"}, {"W7If8Dcq": "http://27.152.195.143:4246"}, {"PJCcApos": "http://121.207.94.185:4246"}, {"9wAJ845H": "http://120.42.133.173:4246"}, {"xGbQtql0": "http://117.26.40.81:4246"}, {"68CYIgVn": "http://120.42.132.104:4246"}, {"BUDwyucr": "http://121.207.92.16:4246"}, {"xJLBGahQ": "http://27.152.193.3:4246"}, {"CVl4ix7L": "http://120.42.133.113:4246"}, {"Db9s5hQK": "http://121.207.92.238:4246"}, {"CWoA8d4x": "http://27.152.192.2:4246"}, {"ql8S4X1s": "http://117.26.41.195:4246"}, {"l0e28rRv": "http://121.207.93.107:4246"}, {"jTAHMmgU": "http://27.152.195.192:4246"}, {"1FMGrjmu": "http://27.152.193.61:4246"}, {"04yLYAK6": "http://117.26.40.51:4246"}, {"lxN7MtOL": "http://27.152.192.188:4246"}, {"7Jpml5RF": "http://120.42.133.128:4246"}, {"JlALoRn2": "http://121.207.93.28:4246"}, {"0Y85wFTl": "http://120.42.132.84:4246"}, {"ByTuMpqg": "http://117.26.40.60:4246"}, {"x4KSDFph": "http://120.42.132.168:4246"}, {"NEdDqzrW": "http://121.207.94.69:4246"}, {"vMpqWhYB": "http://117.26.40.152:4246"}, {"VaKJQ6hy": "http://121.207.92.30:4246"}, {"jVoimG9R": "http://120.42.134.158:4246"}, {"YqtLH32T": "http://120.42.132.232:4246"}, {"BACwrUG0": "http://121.207.93.208:4246"}, {"whyDFoz9": "http://117.24.80.213:4246"}, {"pb0J7EG9": "http://120.42.133.195:4246"}, {"nrhEA4Fc": "http://121.207.92.115:4246"}, {"1MopbLQR": "http://27.152.195.229:4246"}, {"iVfAXTmG": "http://117.26.41.115:4246"}, {"MOS9P441": "http://121.207.93.238:4246"}, {"RJYheopt": "http://120.42.132.185:4246"}, {"jFV8k7QX": "http://121.207.93.119:4246"}, {"CzgpPAWM": "http://117.24.80.228:4246"}, {"hw1j05cu": "http://117.26.40.192:4246"}, {"kBFlSjtr": "http://117.26.41.28:4246"}, {"S1TEvCdB": "http://117.24.81.24:4246"}, {"tsf5n2lD": "http://121.207.92.118:4246"}, {"3iIvxWzZ": "http://117.24.81.217:4246"}, {"OaNh9kdm": "http://117.24.80.116:4246"}, {"WVen1m2q": "http://27.152.195.215:4246"}, {"HUFlkYxa": "http://117.26.40.202:4246"}, {"6GDjEYeA": "http://121.207.92.10:4246"}, {"kwVmW4Cd": "http://120.42.134.47:4246"}, {"hGpBtKxb": "http://27.152.194.73:4246"}, {"bxfrCJYF": "http://117.26.40.193:4246"}, {"OWGaxz4T": "http://117.24.80.186:4246"}, {"y1EIemar": "http://117.24.80.77:4246"}, {"IyUapLk9": "http://27.152.192.254:4246"}, {"X2U4PTRE": "http://120.42.132.12:4246"}, {"FygNmWdX": "http://27.152.192.136:4246"}, {"szFjICQ6": "http://27.152.193.118:4246"}, {"xDaRnZQf": "http://120.42.133.207:4246"}, {"WtlTPiER": "http://117.24.80.162:4246"}, {"rN4gFBRc": "http://120.42.133.248:4246"}, {"tGw9fLRi": "http://121.207.93.181:4246"}, {"0oNZ3LGc": "http://117.26.41.140:4246"}, {"RPonmFLM": "http://117.24.81.40:4246"}, {"Wv3cFNIy": "http://117.24.80.237:4246"}, {"UPSbfkY0": "http://121.207.92.192:4246"}, {"1mwZIG4h": "http://117.26.41.143:4246"}, {"Elo89OuU": "http://117.26.41.136:4246"}, {"94t7UpJa": "http://117.24.81.176:4246"}, {"vefWHjkY": "http://117.26.40.99:4246"}, {"9NQlG4Jy": "http://120.42.134.109:4246"}, {"csfJunU1": "http://121.207.92.93:4246"}, {"WKB4XCtg": "http://121.207.92.69:4246"}, {"sj5BvXKP": "http://117.26.42.40:4246"}, {"wy8bUki2": "http://27.152.194.94:4246"}, {"1HzKZkWF": "http://27.152.192.87:4246"}, {"TEDGh5ei": "http://120.42.132.203:4246"}, {"fBjQh7lH": "http://121.207.92.119:4246"}, {"SwVhJ2a4": "http://117.24.82.10:4246"}, {"V5pvrSZg": "http://117.24.80.91:4246"}, {"L5j3zrUQ": "http://27.152.194.162:4246"}, {"rTmN2sBu": "http://121.207.93.211:4246"}, {"sKunHzLW": "http://117.24.81.191:4246"}, {"f96OpojZ": "http://117.24.80.27:4246"}, {"4dxwp2LQ": "http://117.26.40.195:4246"}, {"UkX90M3I": "http://120.42.132.172:4246"}, {"e8g4yBJ1": "http://117.26.41.236:4246"}, {"3T0ntxlO": "http://27.152.193.10:4246"}, {"47XLKGgB": "http://27.152.192.211:4246"}, {"qXniS3NK": "http://27.152.195.236:4246"}, {"SNcFCR2o": "http://120.42.132.204:4246"}, {"U4PrdDvM": "http://117.24.81.107:4246"}]
start_url = "http://api.daoshidianping.com/Get_Uni_List"
session_url = "http://api.daoshidianping.com/Get_Session"
school_url = "http://api.daoshidianping.com/Get_School_List?uni_id={}"
teacher_url = "http://api.daoshidianping.com/Get_Teacher_Info?id={}"
comment_url = "http://api.daoshidianping.com/Get_Comment_List?id={}"
msg_list = []


def get_comment(id, headers, temp_dict):
    time.sleep(0.5)
    response = requests.get(comment_url.format(id), headers=headers, proxies=random.choice(PROXY))
    j_str = json.loads(response.text)
    temp_dict['评价条数'] = str(len(j_str))
    comment = ""
    if len(j_str) > 0:
        for i in j_str:
            if i.get('tutor_ability_comment') is None:
                pass
            else:
                comment += ("科研能力：" + i.get('tutor_ability_comment') + "||")
            if i.get('tutor_fund_comment') is None:
                pass
            else:
                comment += ("科研经费" + i.get('tutor_fund_comment') + "||")
            if i.get('tutor_relation_comment') is None:
                pass
            else:
                comment += ("师生关系" + i.get('tutor_relation_comment') + "||")
            if i.get('tutor_time_comment') is None:
                pass
            else:
                comment += ("工作时间" + i.get('tutor_time_comment') + "||")
            if i.get('tutor_prospect_comment') is None:
                pass
            else:
                comment += ("学生前途" + i.get('tutor_prospect_comment') + "||")
            if i.get('tutor_info_comment') is None:
                pass
            else:
                comment += (i.get('tutor_info_comment') + "|<>|")
            comment = comment.replace('<br><br>', '||')
    else:
        pass
    temp_dict['评论内容'] = comment
    with open('daoshidianpin.txt', 'a', encoding='gbk') as f:
        f.write(str(temp_dict) + '\n')
    print(temp_dict)


def get_teacher(teacher, headers):
    temp_dict = {}
    id = teacher.get('id')
    time.sleep(0.5)
    response = requests.get(teacher_url.format(id), headers=headers, proxies=random.choice(PROXY))
    j_str = json.loads(response.text)
    for i in j_str:
        temp_dict['学校'] = i.get('uni_name')
        temp_dict['学院'] = i.get('school_name')
        temp_dict['姓名'] = i.get('teacher_name')
        temp_dict['职称'] = i.get('title')
        temp_dict['所在系所'] = i.get('college_name')
        temp_dict['办公室'] = i.get('location')
        temp_dict['研究方向'] = i.get('research_field')
    get_comment(id, headers, temp_dict)


def get_school(school, headers):
    id = school.get('id')
    response = requests.get(school_url.format(id), headers=headers, proxies=random.choice(PROXY))
    j_str = json.loads(response.text)
    for i in j_str:
        for j in i.get('school'):
            get_teacher(j, headers)


def spider(headers):
    response = requests.get(start_url, headers=headers, proxies=random.choice(PROXY))
    j_str = json.loads(response.text)
    for i in j_str:
        for j in i.get('university'):
            get_school(j, headers)


def get_session():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    }
    response = requests.get(session_url, headers=headers, proxies=random.choice(PROXY))
    headers['Authorization'] = response.text
    return headers


def main():
    headers = get_session()
    spider(headers)


if __name__ == '__main__':
    main()