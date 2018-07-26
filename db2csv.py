# coding=utf-8
# description
# extract all valid words to a csv file
# 提取所有有效单词到 csv 文件


from models_exp import NewWord
import csv
import chardet

def extract():
    query = NewWord.select()
    #query = NewWord.select().where((NewWord.is_valid == True) & (NewWord.re1 == 'added')).order_by(-NewWord.frequency)
    print(len(query))

    for word in NewWord.select():
        #print(word.name)
        res = []
        
        for i in [word.name, word.explanation, word.frequency]:
            res.append(i)
        

        yield res

def save(res):

    with open('words.csv', 'a+', errors='ignore', newline='')as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(res)


def main():

    row = extract()
    count = 1
    #打印头部
    save(('单词','翻译','出现次数'))
    
    while True:
        try:
            row_data = next(row)
        except:
            break
        save(row_data)
        count += 1

if __name__ == '__main__':
    main()
    # res = extract()
    # print(next(res))
    # print(next(res))
    # print(next(res))
