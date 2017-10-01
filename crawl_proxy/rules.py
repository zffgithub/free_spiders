#coding: utf-8

para = {
    'xici': {
        'url': 'http://www.xicidaili.com/nn/%s',
        'page_num': "//div[@class='pagination']/a[last()-1]/text()",
        'type': 'xpath',
        'pattern': "//*[@id='ip_list']/tr[position()>1]",
        'position': {'ip': './td[2]/text()', 'port': './td[3]/text()', 'type': './td[5]/text()', 'protocol': './td[6]/text()'},
    },
}





vali_rule = {
    'http://www.taobao.com': 10,
    'http://www.jd.com': 10,
    'http://www.lianjia.com': 10,
    'http://www.koofang.com': 9,
    'http://www.5i5j.com': 5,
}