#encoding: utf-8
proxy_url = 'http://localhost:18885/crawl/proxy/all'

host = 'localhost'
port = 3306
user = 'root'
password = 'root'
db_name = 'pkulaw'

library = {'中央法规':'1469238638146621440'}  ##暂时先收入中央法规，地方法规两部分 '地方法规':'1469238638155010048'
#中央法规 效力阶位
zyfg_EffectivenessDic = ["XA0101","XA0102","XJ15","XA0103","XA0104","XA0105","XA0106","XR12","XA0107","XI05","XA0108","XK06","XC0201","XC0202","XC0203","XG0401","XG0402","XG0403","XE0301","XE0302","XE0303","XE0304","XQ0901","XQ0902","XQ0903"]
#地方法规 效力阶位
dffg_EffectivenessDic = ["XM0701","XM07","XO08","XM0702","XP08","XM0703","XP09","XM0704","XP10","XP11"]
#发布年份
year = {'begin':1949,'end':2023}
#法规分类
Category = {'begin':1,'end':109}
#时效性01现行有效，02失效，03已被修改，04尚未实行，05部分时效
TimelinessDic = ['01','02','03','04','05']


