# coding=utf-8
# import re
# m_list = {'text_link': 'http://www.flightclub.cn/news/a/sneaker/2020/0711/58340.html', 'title': '明星穿鞋也跟风！17 位明星晒了同一双！最狠的居然是他...', 'push_time': ['2020-07-11 发布时间'], 'read_count': '4064', 'img_list': "['http://www2.flightclub.cn/news/uploads/allimg/200711/14-200G1131J0.jpg', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0130156.jpg', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0132613.jpg', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0101200.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0102046.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0102048.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0132526.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0102048-50.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0102314.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0133017.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0133018.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0131234.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0131530.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0131F6.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0131F8.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0131F8-50.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0131F9.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0133447.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0154153.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0154151.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G0154150.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G01R032.png', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G01R031.png', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G01R211.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G01R215.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G01R525.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200711/17-200G1011220.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G01R535.gif', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G01R538.gif', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G01R538.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png', 'http://www2.flightclub.cn/news/uploads/allimg/200710/17-200G01S455.jpg', 'http://www2.flightclub.cn/static/img/news_blank_bg_pic.png']", 'text_content': '上个月的球鞋圈，似乎只充斥着两个类别的球鞋：DiorxJordan联名，其他球鞋。而且在明星圈，更是掀起了不小的人传人现象，晒DiorxJordan联名，似乎比晒超跑、名表还来的实在。究竟现在有多少位明星晒了DiorxAirJordan1联名？上月还有哪些明星上脚了狠货？看过这篇让你一饱眼福！01真正的「顶级明星同款」最后一位谁也比不过！要说上脚DiorxAirJordan1联名的第一人，Dior总监KimJones是毫无疑问的第一人。作为引领时尚风向的意见领袖，在传统奢侈品设计中，融入了高级街头与潮流时尚元素。即便放在当下多元文化包容性极强的环境中，依然是具有特殊意义的合作联名。紧随他之后，TravisScott应该算是第二个上脚的明星。备受Dior设计总监KimJones欣赏，TravisScott担纲了DiorxAirJordan1联名的型录模特，早于迈阿密DiorMenFall2020秀场就已经上脚。TravisScott（左1）不久之后，鞋王DJKhaled也旋即在Instagram手舞足蹈的秀了一波。这种拿到挚爱的感觉，估计每个玩鞋的朋友都能深刻的感受到。DJKhaled然后，就陆续迎来了海外晒DiorxAirJordan1的首波高峰。姆巴佩贾老板保罗金小妹而后便迎来了全球的疫情，原定于4月发售的DiorxAirJordan1与AirJordan1Low不得不推迟。但在3月，Dior品牌大使王俊凯在为《时尚先生Esquirefine》拍杂志封面时，提前为大家带来了上脚及服饰的预告。王俊凯同样也因为这样的紧俏形势，Dior联名的市价因此也一路飙涨，高帮款最高市价曾经涨至10万元以上。能在这个时期入手这双鞋，更是实力的体现。想要的鞋迷很多，比如像王校长。但是，即便强如王校长，买鞋也会被鸽。所以直到一个多月以后，王校长才如愿上脚。紧随王校长之后，晒DiorxAirJordan1的人传人风潮正式刮起。周董作为活跃在Instagram的知名鞋头，也安耐不住对这双鞋的喜爱。哥想問問各位鞋頭哥這樣算是全亞洲最速上腳嗎（哭笑表情）。次日，陈冠希在Instagram上也晒了收货照，云淡风轻的说了句BUBBLEWRAP（气泡膜）。陈冠希随意晒照紧接着，雨神萧敬腾互动了周董，表示小弟跟@jaychou哥撞鞋撞的開開心心。网友说：雨神你的鞋总容易泡水，不如卖我！音乐制作人兼歌手ZICO同样收到了品牌送来的礼物，并第一时间上脚。整身搭配HumanMade卫衣，活力感十足的阳光大男孩气质。ZICO以整身HumanMade搭配还有Dr.Woo也在第一时间上脚，鞋盒内的花体字手写信估计正是Dr.Woo喜欢的感觉。Dr.Woo上脚清一色的晒高帮，林俊杰错峰晒鞋，晒了双少见的低帮DiorxAirJordan1Low，牛仔裤搭配简单高级。林俊杰比低帮更少见的，是新晋鞋头刘嘉玲！冠希为大姐大点赞，不知道她是更喜欢Dior这个牌子，还是喜欢球鞋。以上几位大佬，无论从自身人气还是上脚搭配，都已经不是我们普（未）通（中）人（签）能比的。但放在最后这位狠人面前，可能都不太够看。因为上边几位可能只有鞋，但下面这位，他有完整一套DiorxJordan联名，外套、衬衫乃至领带、袜子可谓一应俱全。要问这位不露脸低调炫富的狠人是谁，看右下角水印就知道了。秦奋低调晒照02藤原浩晒新联名，吴亦凡晒LV各路明星都有狠货！藤原浩前两天，野村訓市在Instagram上晒了一张藤原浩和HIMI的合照。照片本身平平无奇，但细心的小编发现，藤原浩脚上这双sacaixNikeLDVWaffle可有点东西！本周网络上便浮现了这双鞋的渲染图及细节，这质感细节，小编真是一目倾心。不仅如此，教父还被拍到上脚了一双特别的AirJordan3联名，后跟的闪电Logo说明了身份，但目前不知道具体是什么情况。再有就是已经提上议程的FragmentDesignxJordanAirCadence联名，这个设计你给几分？吴亦凡近期除了Dior联名外，时尚圈、潮流圈晒得最多的，怕就是LouisVuittonxNigo的LV系列联名了。发售当日秒售罄，吴亦凡多次上身的夹克、帽子都是分分钟卖完的狠货。像这样的一身，要是换做常人估计很难驾驭。小编非常喜欢这件灰色卫衣，上身质感非常高级。Nigo与LV的这次合作，不仅让他本人在时尚圈名声大作，更让他的品牌HumanMade热度大增。像吴亦凡身上的小鸭子挂饰，就是此次合作的标志性象征之一，LVMADELogo可以说就是品牌带货品牌的最好象征。不少买不到LV联名的小伙伴，都选择了HumanMade带有小鸭子的单品，Nigo这波操作可以说是名利双收啊！来自Kris的凝视欧阳娜娜与大家一样，因为疫情宅在家的娜比，日常生活照也多了起来。近期娜娜最中意的球鞋，莫过于上月发售的TravisScottxNikeAirMax270React联名。多次特写晒照，还搭配同色系的服饰，可见喜爱之情。而在配饰选择上，娜娜也上身了LV联名的小鸭子，朋克风格褡裢修饰，搞怪又可爱。上月18号刚刚过完生日的她，迎来了20岁。作为千禧年生人，娜娜再度让无数网友羡慕不已，在微博留言中最多的回复也是，谁不想活成欧阳娜娜呢？周杰伦上月还有一个大事件，那便是发了新单《Mojito》的周董，小编现在还记得发歌那天晚上朋友圈的盛景...细心的小伙伴估计发现了，在专辑中的说唱部分，穿的正是他去年总晒的CLOTxNikeAirForce1黑丝绸，搭配自家品牌PHANTACi，整身搭配可谓酷劲十足。黑丝绸CLOTxNikeAirForce1除了黑丝绸，以及上边说过的Dior联名外，周董最近也穿了不少新鞋。比如他最爱的BenJerrysxNikeDunkSBLow，醒目的颜值，让小编根本没看身后的迈凯伦...BenJerrysxNikeDunkSBLow以及TravisScottxAirMax270React，简单的照片朴实无华。TravisScottxAirMax270React再或者低调朴实的AirJordan12，在屋顶的J形状吊灯及两辆小轿车的衬托下，显得非常潇洒...当然，以周董歌词为创意设计的NikeLeBron17Courage是不得不提的狠货！没有超跑的型照，依旧很酷！最后的最后，小编还想cue一下上月的热播剧《隐秘的角落》，实在是太火了。甭管看没看过，应该都听说了秦昊带你去爬山、时间管理大师朱朝阳的梗。而在热播之后，各位主演变成了时尚杂志的封面新宠。史彭元/王圣迪/秦昊/荣梓杉《时尚芭莎》封面人物而要说这部剧对球鞋圈的影响力，最直接的体现，便是本月销量大增的纯白AirForce1，竟然一度登顶销量榜榜首，足以见得这部剧的影响力。剧中朱朝阳上脚纯白AirForce1而现实生活中，朱朝阳的扮演者荣梓杉，同样也是个不折不扣的鞋头。前两天在为剧宣传的时候，还不忘秀一波收藏，这架势大有赶超白敬亭的势头，估计未来也是个不可估量的球鞋大佬。好了！由于篇幅原因，本期的明星上脚就到这了谁是你心目中最狠的鞋头，大家应该一目了然了吧！如果大家发掘了新的明星鞋头，可以在评论区留言，我们将在下一期为大家带来更多养眼帅照！'}
# print(re.sub("'", "", str(tuple(m_list))))
# print(str(tuple(m_list.values())))
# temp_str = ""
# for i in tuple('%s = "%s",' % (k, v) for k, v in m_list.items()):
#     temp_str += i
# temp_str = temp_str[0:-2] + "\""
# print(temp_str)


import re
import json
from retryl_request import request_url
from lxml import etree
from urllib import parse


url = "http://www.flightclub.cn/news/a/sneaker/2019/1029/53700.html"
start_url = "http://www.flightclub.cn/"
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }
with open("./ip_pool", "r") as f:
    content = f.read()
ip_pool = json.loads(content)
msg_dict = {"text_link": url}
response = request_url(url, headers=headers, proxies_list=ip_pool)
html = etree.HTML(response.text)
# 获取文字主题
temp_title = re.sub("\\|\n", "", html.xpath("//div[@class='news_title']/h1/text()")[0])
temp_title = re.sub("\"|'", "“", temp_title)
msg_dict["title"] = temp_title
# 获取文字发表时间
msg_dict["push_time"] = html.xpath("//div[@class='body']/div[1]/text()")[0]
# 请求阅读数api，获取阅读数量
count_url_list = re.findall("fetch\(\"(/ajax/news_count/\d+)\"\)\.then\(function\(r\)", response.text)
count_url = parse.urljoin(start_url, count_url_list[0])
count = request_url(count_url, headers=headers, proxies_list=ip_pool)
try:
    msg_dict["read_count"] = count.text
except:
    print(url)
    print(count_url)
# 获取全部图片链接
img = html.xpath("//div[@class='content']/img")
if len(img) <= 0:
    img = html.xpath("//div[@class='content']/p/a/img")
img_list = list()
for i in img:
    temp_img = str(i.xpath("./@src")[0])
    if temp_img.endswith(".png"):
        try:
            img_list.append(str(i.xpath("./@data-original")[0]))
        except:
            pass
        else:
            img_list.append(temp_img)
    else:
        img_list.append(temp_img)
msg_dict["img_list"] = str(img_list)
# 获取正文内容
temp_re_obj = re.compile(r"<div class=\"content\">(.*?)<!-- GA -->", re.S)
text_list = temp_re_obj.findall(response.text)
text_content = ""
for i in text_list:
    text_temp = re.sub(
        r"<(.*?)>| |&sup2;|\u200b|&yen;|&nbsp;|&ldquo;|&rdquo;|&middot;|&amp;|&mdash;|▼|\r|\n|\t|\\", "", i)
    text_temp = re.sub("\"|'", "“", text_temp)
    text_content += text_temp
msg_dict["text_content"] = text_content
print(msg_dict)