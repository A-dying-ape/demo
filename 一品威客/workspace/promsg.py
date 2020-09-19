import re
import time
from setting import HEADERS
from lxml import etree
from util.deal_html import deal_nbsp


class Pro_Msg():
    def __init__(self, session, sort_list):
        self.session = session
        self.sort_list = sort_list

    def get_pro_info(self, s):
        response = self.session.get(s, headers=HEADERS)
        response = deal_nbsp(response)
        html = etree.HTML(response)
        div_list = html.xpath("//div[@class='task_class_list_li']/div[@class='task_class_list_li_box']")
        for div in div_list:
            temp_dict = {}
            temp_dict['赏金额度'] = div.xpath("./div[@class='wrid1']/h3/b/text()")[0].strip()
            temp_dict['项目名'] = div.xpath("./div[@class='wrid1']/h3/a/text()")[0].strip()
            temp_dict['详情链接'] = div.xpath("./div[@class='wrid1']/h3/a/@href")[0].strip()
            temp_dict['投标热度'] = div.xpath("./div[@class='wrid1']/samp//text()")[0].strip() + div.xpath("./div[@class='wrid1']/samp/font/text()")[0].strip() + "人已经投标"
            try:
                temp_dict['截止时间'] = div.xpath("./div[@class='wrid2']/span/span[1]/text()")[0].strip() + "天" + div.xpath("./div[@class='wrid2']/span/span[2]/text()")[0].strip() + "小时后投稿截止"
            except:
                try:
                    temp_dict['截止时间'] = div.xpath("./div[@class='wrid2']/span/span[1]/text()")[0].strip() + "小时后投稿截止"
                except:
                    return
            detail_response = self.session.get(temp_dict['详情链接'], headers=HEADERS)
            dhtml = etree.HTML(detail_response.text)
            temp_dict["用户名"] = dhtml.xpath("//div[@class='task-user-header']/span/text()")[0].strip()
            temp_dict["赏金分配"] = re.split("：", dhtml.xpath("//div[@class='task_user_info']//span[@class='span_state']/a/text()")[0].strip())[1]
            temp_dict["任务需求"] = ""
            texts = dhtml.xpath("//div[@class='task-info-content']//text()")
            for t in texts:
                temp_dict["任务需求"] += t.strip()
            span_list = dhtml.xpath("//div[@class='task-chengxin']/span")
            temp_dict["欠缺条件"] = ""
            for span in span_list:
                try:
                    temp_dict["欠缺条件"] += (span.xpath("./a/text()")[0].strip() + "|")
                except:
                    pass
            temp_dict["发布时间"] = dhtml.xpath("//div[@class='task-user-info-action']/span[1]/span/text()")[0].strip()
            temp_dict["任务编号"] = re.split("：", dhtml.xpath("//div[@class='task-user-info-action']/span[3]/span/text()")[0].strip())[1]
            with open("./msg.csv", "a", encoding="GBK") as f:
                f.write(str(temp_dict) + "\n")
            print(temp_dict)
            time.sleep(1)
        try:
            next_page = html.xpath("//div[@class='page pt_15 pb_15']/a[text()='下一页>>']/@href")[0]
        except:
            return
        else:
            self.get_pro_info(next_page)

    def run(self):
        for s in self.sort_list:
            self.get_pro_info(s)