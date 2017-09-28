#定义好需要找到同义词的词语组合，放在words_set中
#遍历words.nearby.txt文件，为words_set关键词集合中的每个词语找到对应的同义词
#以 “标准词语 ：同义词1、同义词2 …… 同义词n”的形式写入文件dict_similar.txt中
#以 “Key<标准词语> : value<同义词集合>”的方式存储在standard_words_dict中
#因为dict中的Key有可能重复，所以dict_similar.txt文件中的行数比standard_words_dict要多

standard_words_dict = {}
current_words_set_list = []
count = 0
f_in = 'words.nearby.txt'
f_out = open('dict_similar.txt','w')
flag = False
with open(f_in) as f_open:
    for line in f_open:
        if(line.startswith('query')):
            if flag:
                standard_words_dict[standard_word] = current_words_set_list[count-1]
                f_out.write(standard_word+":")
                for i in current_words_set_list[count-1]:
                    if len(i) > 1:
                        f_out.write(i.strip()+" ")
                f_out.write('\n')
            flag = False
            current_words_set = set()
            current_words_set_list.append(current_words_set)
            count += 1
            standard_word = ''
            current_words_set.add(line.split(': ')[1].strip())
            if(line.split(': ')[1].strip() in words_set):
                flag = True
                standard_word = line.split(': ')[1].strip()
        else:
            current_word = line.strip().split('\t')[0].strip()
            current_words_set.add(current_word)
            if(current_word in words_set):
                flag = True
                standard_word = current_word
f_out.close()
f_open.close()
