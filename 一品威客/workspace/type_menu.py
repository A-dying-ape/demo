from lxml import etree
from setting import HEADERS, SORT_FILTER, MODEL_FILTER, BOUNTY_FILTER, STATE_FILTER


class Type_Menu():
    def __init__(self, session, addr):
        self.session = session
        self.addr = addr
        self.addr_url = "https://www.epwk.com/index-city-%s.html"
        self.task_url = "https://task.epwk.com/soft/"
        self.sort_list = []

    def get_prov(self):
        # 选择省份
        url = self.addr_url % self.addr
        self.session.get(url, headers=HEADERS)
        self.get_sort()

    def get_sort(self):
        # 获取分类条件
        temp_list = list()
        response = self.session.get(self.task_url, headers=HEADERS)
        html = etree.HTML(response.text)
        a_list = html.xpath("//div[@class='task_class_list']/div[1]/span/a")
        for a in a_list:
            try:
                text = a.xpath("./text()")[0].strip()
            except:
                text = None
                href = None
            else:
                href = a.xpath("./@href")[0].strip()
            if text in SORT_FILTER:
                temp_list.append(href)
        self.get_model(temp_list)

    def get_model(self, sort):
        # 获取模型条件
        temp_list = list()
        if "全部" in MODEL_FILTER:
            self.get_bounty(sort)
        else:
            for s in sort:
                response = self.session.get(s, headers=HEADERS)
                html = etree.HTML(response.text)
                a_list = html.xpath("//div[@class='task_class_list']/div[2]/span/a")
                for a in a_list:
                    try:
                        text = a.xpath("./text()")[0].strip()
                    except:
                        text = None
                        href = None
                    else:
                        href = a.xpath("./@href")[0].strip()
                    if text in MODEL_FILTER:
                        temp_list.append(href)
            self.get_bounty(temp_list)

    def get_bounty(self, model):
        # 获取赏金条件
        temp_list = list()
        if "全部" in BOUNTY_FILTER:
            self.get_state(model)
        else:
            for s in model:
                response = self.session.get(s, headers=HEADERS)
                html = etree.HTML(response.text)
                a_list = html.xpath("//div[@class='task_class_list']/div[3]/span/a")
                for a in a_list:
                    try:
                        text = a.xpath("./text()")[0].strip()
                    except:
                        text = None
                        href = None
                    else:
                        href = a.xpath("./@href")[0].strip()
                    if text in BOUNTY_FILTER:
                        temp_list.append(href)
            self.get_state(temp_list)

    def get_state(self, bounty):
        if "全部" in STATE_FILTER:
            self.sort_list = bounty
        else:
            for s in bounty:
                response = self.session.get(s, headers=HEADERS)
                html = etree.HTML(response.text)
                a_list = html.xpath("//div[@class='task_class_list']/div[4]/span/a")
                for a in a_list:
                    try:
                        text = a.xpath("./text()")[0].strip()
                    except:
                        text = None
                        href = None
                    else:
                        href = a.xpath("./@href")[0].strip()
                    if text in STATE_FILTER:
                        self.sort_list.append(href)


    def run (self):
        self.get_prov()
        return self.sort_list