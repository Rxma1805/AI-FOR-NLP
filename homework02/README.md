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
    
���ϳ�������
    
������������Դ�� is more possible
---- ������������Դ�� with probility 6.320698068780764e-20
---- ������������Դ�� with probility 6.952767875658838e-19
['����', 'һ��', '��', '����']
['����', 'һ��', '��', 'ƻ��']
����һ���ƻ�� is more possible
---- ����һ������� with probility 2.0831116180984166e-15
---- ����һ���ƻ�� with probility 8.561588750384492e-12
['����', '����', '��', '��', '��', '���', ',', '����', 'һ��', '��', '����']
['����', '����', '��', '��', '��', '���', ',', '����', 'һ��', '��', 'ƻ��']
������������Դ��,����һ���ƻ�� is more possible
---- ������������Դ��,����һ������� with probility 2.655713232864335e-39
---- ������������Դ��,����һ���ƻ�� with probility 9.922710351884021e-37
['��', '��', 'һֻ', '�ÿ�', '��', 'Сè']
['����', 'һֻ', '�ÿ�', '��', 'Сè']
����һֻ�ÿ���Сè is more possible
---- ����һֻ�ÿ���Сè with probility 1.1498665310450489e-18
---- ����һֻ�ÿ���Сè with probility 1.272944327746083e-16
['����', '��', 'ȥ', '�Ի��']
['����', '���', 'ȥ', '��', '��']
������ȥ�Ի�� is more possible
---- ������ȥ�Ի�� with probility 9.40749580188389e-15
---- ������ȥ���� with probility 1.3313203136546739e-15
['���', '����', '��', 'һ��']
['���ֶ�', '����', 'һ��']
���������һ�� is more possible
---- ���������һ�� with probility 2.2701687556796086e-15
---- ���ֶ�����һ�� with probility 4.3548616064353e-16