from util.request import request_url
from setting import HEADERS, TOP_MENU
from lxml import etree
from urllib import parse
from workspace.showcase import Show_Case
from workspace.showtemplet import  Show_Templet


state_url = "http://www.jizhida.cn/"


def index_top():
    # 获取top分类
    temp_dict = {}
    response = request_url(url=state_url, headers=HEADERS, method='get', proxy=True)
    html = etree.HTML(response.text)
    top_text = html.xpath("//ul[@class='top_nav']/li/a/text()")
    for text in top_text:
        if text in TOP_MENU:
            href = html.xpath("//ul[@class='top_nav']/li/a[text()='%s']/@href" %text)[0]
            href = parse.urljoin(state_url, href)
            temp_dict[text.strip()] = href
    return temp_dict


if __name__ == '__main__':
    # 主逻辑
    it = index_top()
    for tm in TOP_MENU:
        if tm == "案例展示":
            sc = Show_Case(state_url, it[tm])
            sc.run()
        elif tm == "模板展示":
            st = Show_Templet(state_url, it[tm])
            st.run()