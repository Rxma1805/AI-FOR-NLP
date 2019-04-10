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