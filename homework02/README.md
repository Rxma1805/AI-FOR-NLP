wiki中文数据经过处理生成的字典放在服务器端
本地与服务器tcp通信获取word_counts

修改的地方：2_gram
def get_combination_prob(w1, w2):
    esp = 1 / two_gram_all_words_counts
    word_counts = tcpClient.send('2_' + w1+w2)
    if word_counts != 'None':
        return int(word_counts) / two_gram_all_words_counts
    else:
        return get_prob(w1)*get_prob(w2)
        
之前老师方法：当p(w1,w2)不存在的时候，返回esp
我的方法      当p(w1,w2)不存在的时候，认为在这个语料库上是独立的等于p(w1)*pw(2)

这样的话  sentence = p(w1) * p(w2|w1)*p(w3|w2)*p(w4|w3)
									 = p(w1) *  p(w2,w1)/p(w1)  *p(w3|w2)*p(w4|w3)
									 如果p(w2,w1)不存在，则
									 =p(w1) *  [(p(w1)*pw(2)) /p(w1) ] *p(w3|w2)*p(w4|w3)
									 =p(w1) * p(w2) * p(w3|w2)*p(w4|w3)
									 
3_gram也是同样的道理，如下：
def get_three_combination_prob(w1, w2,w3):
    esp = 1 / three_gram_all_words_counts
    word_counts = tcpClient.send('3_' + w1+w2+w3)
    if word_counts != 'None':
        return int(word_counts) / three_gram_all_words_counts
    else:
        return get_combination_prob(w1,w2) * get_prob(w3)
    
附上程序结果：
    
今天晚上请你吃大餐 is more possible
---- 明天晚上请你吃大餐 with probility 6.320698068780764e-20
---- 今天晚上请你吃大餐 with probility 6.952767875658838e-19
['我们', '一起', '吃', '日料']
['我们', '一起', '吃', '苹果']
我们一起吃苹果 is more possible
---- 我们一起吃日料 with probility 2.0831116180984166e-15
---- 我们一起吃苹果 with probility 8.561588750384492e-12
['今天', '晚上', '请', '你', '吃', '大餐', ',', '我们', '一起', '吃', '日料']
['明天', '晚上', '请', '你', '吃', '大餐', ',', '我们', '一起', '吃', '苹果']
明天晚上请你吃大餐,我们一起吃苹果 is more possible
---- 今天晚上请你吃大餐,我们一起吃日料 with probility 2.655713232864335e-39
---- 明天晚上请你吃大餐,我们一起吃苹果 with probility 9.922710351884021e-37
['真', '事', '一只', '好看', '的', '小猫']
['真是', '一只', '好看', '的', '小猫']
真是一只好看的小猫 is more possible
---- 真事一只好看的小猫 with probility 1.1498665310450489e-18
---- 真是一只好看的小猫 with probility 1.272944327746083e-16
['今晚', '我', '去', '吃火锅']
['今晚', '火锅', '去', '吃', '我']
今晚我去吃火锅 is more possible
---- 今晚我去吃火锅 with probility 9.40749580188389e-15
---- 今晚火锅去吃我 with probility 1.3313203136546739e-15
['洋葱', '奶昔', '来', '一杯']
['养乐多', '绿来', '一杯']
洋葱奶昔来一杯 is more possible
---- 洋葱奶昔来一杯 with probility 2.2701687556796086e-15
---- 养乐多绿来一杯 with probility 4.3548616064353e-16