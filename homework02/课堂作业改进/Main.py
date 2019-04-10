from TCPClient import Client
import jieba

tcpClient = Client()
one_gram_all_words_counts = int(tcpClient.send('1_LEN'))
two_gram_all_words_counts = int(tcpClient.send('2_LEN'))
three_gram_all_words_counts = int(tcpClient.send('3_LEN'))

def get_combination_prob(w1, w2):
    esp = 1 / two_gram_all_words_counts
    word_counts = tcpClient.send('2_' + w1+w2)
    if word_counts != 'None':
        return int(word_counts) / two_gram_all_words_counts
    else:
        return get_prob(w1)*get_prob(w2)

def get_three_combination_prob(w1, w2,w3):
    esp = 1 / three_gram_all_words_counts
    word_counts = tcpClient.send('3_' + w1+w2+w3)
    if word_counts != 'None':
        return int(word_counts) / three_gram_all_words_counts
    else:
        return get_combination_prob(w1,w2) * get_prob(w3)

def get_prob(word):#P(w1)
    esp = 1 / one_gram_all_words_counts
    word_counts = tcpClient.send('1_'+word)
    if word_counts != 'None':
        return int(word_counts) / one_gram_all_words_counts
    else:
        return esp

def get_prob_2_gram(w1, w2):#P(w2|w1)
    return get_combination_prob(w1, w2) / get_prob(w1)

def get_prob_3_gram(w1,w2,w3):#P(w3|w1w2)
    return get_three_combination_prob(w1, w2, w3)/get_combination_prob(w1, w2)


def language_model_of_3(sentence):
    probability = 1
    word_list =  list(jieba.cut(sentence))
    for i,word in enumerate(word_list):
        if i == 0:
            probability*=get_prob(word)
            # print(word,probability)
        elif i == 1:
            pre_word = word_list[i-1]
            probability *=get_prob_2_gram(pre_word,word)
            # print(pre_word,word, probability)
        else:
            pr_n_2_word = word_list[i - 2]
            pr_n_1_word = word_list[i - 1]
            probability *= get_prob_3_gram(pr_n_2_word, pr_n_1_word,word)
            # print(pr_n_2_word, pr_n_1_word,word, probability)
    return probability


need_compared = [
    "明天晚上请你吃大餐 今天晚上请你吃大餐",
    "我们一起吃日料 我们一起吃苹果",
    "今天晚上请你吃大餐,我们一起吃日料 明天晚上请你吃大餐,我们一起吃苹果",
    "真事一只好看的小猫 真是一只好看的小猫",
    "今晚我去吃火锅 今晚火锅去吃我",
    "洋葱奶昔来一杯 养乐多绿来一杯"
]

for s in need_compared:
    s1, s2 = s.split()

    print(list(jieba.cut(s1)))
    print(list(jieba.cut(s2)))

    p1, p2 = language_model_of_3(s1), language_model_of_3(s2)

    better = s1 if p1 > p2 else s2

    print('{} is more possible'.format(better))
    print('-' * 4 + ' {} with probility {}'.format(s1, p1))
    print('-' * 4 + ' {} with probility {}'.format(s2, p2))


