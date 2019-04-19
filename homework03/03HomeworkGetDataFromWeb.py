import re
import requests
import pandas as pd

def hand_station_name(flag):
    def _w(station_with_noise,is_last=False):
        if flag == 1:
            if is_last:
                n_1,n = ((station_with_noise[1:-1].split('>')[1]).split('<')[0]).split('——')
                return [n_1,n]
            else:
                return [((station_with_noise[1:-1].split('>')[1]).split('<')[0]).split('——')[0]]
        elif flag == 2:
            return [((station_with_noise.split('<td')[0])[1:-1].split('>')[1]).split('<')[0]]
        elif flag == 3:
            # <td width="100" align="center" valign="middle" colspan="1" rowspan="1"><a target="_blank" href="/item/%E8%8B%B9%E6%9E%9C%E5%9B%AD%E7%AB%99"><i>苹果园站
            # <div class="para" label-module="para"><a target="_blank" href="/item/%E5%B7%B4%E6%B2%9F%E7%AB%99">巴沟站


            return [station_with_noise.split('>')[-1]]
        else:
            return []
    return _w

def re_match_station(pattern,station_text,handle_msg):
    station_list = pattern.findall(station_text)
    #print(station_list)
    _station_list=[]
    for i,station_name in enumerate(station_list):
        if i == len(station_list)-1:
            _station_list += handle_msg(station_name,True)
        else:
            _station_list += handle_msg(station_name)

    return _station_list if len(_station_list) > 2 else []







pat = 'https://baike.baidu.com'
url='https://baike.baidu.com/item/北京地铁/408485?fr=aladdin'
pattern = re.compile('/item/[%|a-z|A-Z|0-9]+">北京地铁\d*\w*线')
kv = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
r = requests.get(url, headers = kv, allow_redirects=False)
#print(r.encoding)
text= r.text.encode("iso-8859-1").decode('utf8')
#<a target="_blank" href="/item/%E5%AE%8B%E5%AE%B6%E5%BA%84%E7%AB%99/75170" data-lemmaid="75170">宋家庄站</a>
station_pattern = re.compile('<th[\s|=|"|\d|\w]*>[\w|\d|a-zA-Z]+——[\w|\d|a-zA-Z]+</th>')

#<td width="94" align="center" valign="middle" rowspan="1">23:22</td>
#<th>温阳路</th><td width="94" align="center" valign="middle" colspan="1" rowspan="1"><div class="para" label-module="para">6:27</div>
station_pattern2 = re.compile('<th[\s|=|"|\d|\w]*>[\w|\d|a-zA-Z]+</th><td[\s|=|"|\d|\w]*[\s|=|"|\d|\w|<|>|/|\-]*>[\d|:|—]+[\s|=|"|\d|\w|<|>|/|\-]*</td>')

#<td width="100" align="center" valign="middle" colspan="1" rowspan="1"><a target="_blank" href="/item/%E8%8B%B9%E6%9E%9C%E5%9B%AD%E7%AB%99"><i>苹果园站</i></a></td>
#<div class="para" label-module="para"><a target="_blank" href="/item/%E5%B7%B4%E6%B2%9F%E7%AB%99">巴沟站</a></div>
station_pattern3 = re.compile('[<div|<td][\s|"|=|a-zA-Z|\-|\d]+><a target=[\s|=|"|\d|\w|%|/|\-|]+>[<|i|>]*[\w|\d|a-zA-Z]+站')


result = pattern.findall(text)
sub_line = {}
for content in result:
    link,line_name = content.split('">')
    # if line_name != '北京地铁14号线':
    #     continue
    if line_name not in sub_line:
        if line_name != '北京地铁14号线':
            sub_line[line_name]= []

        new_url = pat+link
        r = requests.get(new_url, headers=kv, allow_redirects=True)
        station_text = r.text.encode("iso-8859-1").decode('utf8')
        print(station_text)
        station = re_match_station(station_pattern,station_text,handle_msg=hand_station_name(1))
        if line_name == '北京地铁14号线':
            sub_line[line_name + 'west'] = station[0:6]+['西局']
            sub_line[line_name + 'east'] = station[6:]
            continue

        if station not in sub_line[line_name]:
            sub_line[line_name] += station
        if sub_line[line_name]:
            continue
        station = re_match_station(station_pattern2, station_text, handle_msg=hand_station_name(2))
        if station not in sub_line[line_name]:
            sub_line[line_name] += station
        if sub_line[line_name]:
            continue
        station = re_match_station(station_pattern3, station_text, handle_msg=hand_station_name(3))
        if station not in sub_line[line_name]:
            sub_line[line_name] += station
        if not sub_line[line_name]:
            print(line_name, "Empty")

print(sub_line)
df = pd.DataFrame(columns=['line','station'])
count = 0
for line_name in sub_line:
    for station in  sub_line[line_name]:
        df.loc[count,['line','station']] = line_name,station
        count+=1
    print("line {} contains {} station stops!".format(line_name,len(sub_line[line_name])))
df.to_csv('./BeiJingStation.csv')
#s = '<th width="184">马各庄</th><td width="109" valign="top">05:37</td>'
#s = '<th align="center" valign="middle">天通苑北——天通苑</th>'
# station_pattern3 = re.compile('<a target=[\s|=|"|\d|\w|%|/|\-|]+>[\w|\d|a-zA-Z]+站')
# s = '<a target="_blank" href="/item/%E5%AE%8B%E5%AE%B6%E5%BA%84%E7%AB%99/75170" data-lemmaid="75170">宋家庄站</a>'
# s='<a target="_blank" href="/item/%E5%B7%B4%E6%B2%9F%E7%AB%99">巴沟站</a>'
# print(station_pattern3.findall(s))
