#coding=utf-8
# 导入某文件夹下的所有 txt 文件，逐一分析，提取出词汇，存入数据库

from collections import Counter #计数器
import re #正则匹配

#引入排除词汇
from setting import exclude_list,NUMBERS
#数据库操作 新书、新单词 class
from models_exp import NewBook,NewWord

class AnlysisBook():
    
    def new_book(self,path,words):#获取新书 加入数据库
        bookname = path.split('/')[-1]
        query_book = NewBook.select().where((NewBook.name == bookname) & (NewBook.is_analyzed == True))#比对数据库是否已分析过
        if query_book:
            return 

        newbook = NewBook.create(
            name = bookname,
            total = len(words)
        )
        return newbook #数据库对象
    
    def _open_file(self,filename):#打开文件，返回所有单词list
        with open(filename,'r',encoding='utf-8')as f:
            raw_words = f.read()
        
        words = re.findall('[a-z]+',raw_words.lower()) #大写字符为小写 #正则匹配所有连续字母
        return　words

    def _filter_words(self,raw_words,count=NUMBERS):#载入未处理的所有单词列表 和 默认count值
        new_words = []
        for word in raw_words:#找出非exclude 和 长度大于1 的单词 -> new_words
            if word not in exclude_list and len(word) > 1:
                new_words.append(word)
                
                
        # 根据书籍字数确定从该书取多少单词
        ct = 10
        for i,j in count:
            if len(new_words) < i:
                ct = j
                break
        
        c = Counter(new_words) #list 里计数的一个class
        return c.most_common(ct) #返回从大到小的排序list[(a,1),....]
 
    def _insert_book_data(self,book,words_times):#建立书籍之后，载入数据
        if not book:
            return 
        
        # 向数据库内插入数据
        for word,fre in words_times:
            query = NewWord.select().where(NewWord.name == word) #数据库是否已有这个单词
            if query:#已有
                word_ins = query[0]
                word_ins.frequency += fre
                word_ins.save()
            else:
                word_ins = NewWord.create(name = word , frequency = fre)
                book.is_analyzed = True
                book.save()
        
    #对外接口
    def analysis(self, lst_files):
        # filename = 'Data+Structures+and+Algorithms+Using+Python.txt'
        for i in lst_files:
            raw_words = self._open_file(i)#拿到总单词
            bookins = self.new_book(i, raw_words)#创建[数据库]书籍对象
            filter_words = self._filter_words(raw_words)#总单词频率化处理 
            self._insert_book(bookins, filter_words)#书籍对象添加数据

                            




