wiki�������ݾ����������ɵ��ֵ���ڷ�������
�����������tcpͨ�Ż�ȡword_counts

�޸ĵĵط���2_gram
def get_combination_prob(w1, w2):
    esp = 1 / two_gram_all_words_counts
    word_counts = tcpClient.send('2_' + w1+w2)
    if word_counts != 'None':
        return int(word_counts) / two_gram_all_words_counts
    else:
        return get_prob(w1)*get_prob(w2)
        
֮ǰ��ʦ��������p(w1,w2)�����ڵ�ʱ�򣬷���esp
�ҵķ���      ��p(w1,w2)�����ڵ�ʱ����Ϊ��������Ͽ����Ƕ����ĵ���p(w1)*pw(2)

�����Ļ�  sentence = p(w1) * p(w2|w1)*p(w3|w2)*p(w4|w3)
									 = p(w1) *  p(w2,w1)/p(w1)  *p(w3|w2)*p(w4|w3)
									 ���p(w2,w1)�����ڣ���
									 =p(w1) *  [(p(w1)*pw(2)) /p(w1) ] *p(w3|w2)*p(w4|w3)
									 =p(w1) * p(w2) * p(w3|w2)*p(w4|w3)
									 
3_gramҲ��ͬ���ĵ������£�
def get_three_combination_prob(w1, w2,w3):
    esp = 1 / three_gram_all_words_counts
    word_counts = tcpClient.send('3_' + w1+w2+w3)
    if word_counts != 'None':
        return int(word_counts) / three_gram_all_words_counts
    else:
        return get_combination_prob(w1,w2) * get_prob(w3)