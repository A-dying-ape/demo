# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import xlwt
import json


class TbspiderPipeline(object):
    gr = 0
    dr = 0
    gc = 0
    dc = 0
    gfile = xlwt.Workbook(encoding='utf-8')
    gtable = gfile.add_sheet('data_goods')
    dtable = gfile.add_sheet('data_detail')
    goods_title = ['商品名称','商店名称','发货地址','图片链接','价格','付款人数','详情链接']
    detail_title = ['商品名称','基本信息']
    for i in goods_title:
        gtable.write(gr,gc,i)
        gc += 1
    for i in detail_title:
        dtable.write(dr,dc,i)
        dc += 1


    def process_item(self, item, spider):
        print(item)
        self.goods_table(item)
        self.gfile.save('good_data.xlsx')
        self.detail_table(item)
        self.gfile.save('good_data.xlsx')
        return item


    def goods_table(self,item):
        table = self.gtable
        good_list = list()
        good_list.append(item['title'][0])
        good_list.append(item['shop'][0])
        good_list.append(item['location'][0])
        good_list.append(item['img'][0])
        good_list.append(item['price'][0])
        good_list.append(item['pay_num'][0])
        good_list.append(item['href'])
        # print(good_list)
        self.gr += 1
        c = 0
        for i in good_list:
            table.write(self.gr,c,i)
            c += 1


    def detail_table(self,item):
        table = self.dtable
        detail_list = list()
        detail_list.append(item['title'][0])
        detail_list.append(json.loads(item['detail_dict'])[0]['基本信息'])
        self.dr += 1
        c = 0
        for i in detail_list:
            table.write(self.dr,c,str(i))
            c += 1