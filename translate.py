# coding=utf-8
# author=zhouxin
# date=2017.7.10
# description
# 调用翻译接口，翻译数据库内词汇

import requests
import time

from models_exp import NewWord


class Translate:

    def __init__(self):
        # self.util = Utils()
        pass

    # translation api, tranlate a english word to chinese
    # return translation result
    # 百度翻译接口
    def _trans(self, word):
        # res = self.trans.translate('hello', dest='zh-CN')
        url = 'http://fanyi.baidu.com/sug'
        dct = {'kw': word}
        req = requests.post(url, dct)
        req.raise_for_status()
        res = req.json().get('data')
        if not res:
            return None
        return res[0].get('v', None)

    # iciba api / 金山词典 api
    # baidu api dont contain Phonogram , so change an api
    def _trans_ici(self, word):

        url = 'http://www.iciba.com/index.php?a=getWordMean&c=search&word=' + word
        try:
            req = requests.get(url)
            req.raise_for_status()
            info = req.json()
            data = info['baesInfo']['symbols'][0]
            assert info['baesInfo']['symbols'][0]
            # 去除没有音标的单词
            assert data['ph_am'] and data['ph_en']
            # 去除没有词性的单词
            assert data['parts'][0]['part']

        except:
            return ('none','none')

        ph_en = '英 [' + data['ph_en'] + ']'
        ph_am = '美 [' + data['ph_am'] + ']'
        ex = ''
        for part in data['parts']:
            ex += part['part'] + ';'.join(part['means']) + ';'

        return ph_en+ph_am, ex

    # 扇贝单词 api
    def _trans_shanbay(self, word):
        url = 'https://api.shanbay.com/bdc/search/?word=' + word
        req = requests.get(url)
        print(req.json())


    # 使用 金山单词 翻译接口
    # 百度接口没有音标
    # 扇贝接口包含的信息不如其他两家
    def trans(self):

        query = NewWord.select().where(NewWord.explanation != '')
        if not query:
            return
        for word in query:

            res = self._trans_ici(word.name)
            # print(res)
            if res:
                word.phonogram = res[0]
                # word.
                word.explanation = res[1]

            else:
                word.is_valid = False
            word.save()
            time.sleep(1)


if __name__ == '__main__':

    t = Translate()
    # res = t._trans_shanbay('hello')
    # print(res)
    # t.trans()
    res = t._trans_ici('hello')
    print(res[1])

    #写代码遍历修改数据库
    for i in NewWord.select():
        print(i.name,end=' ')
        exp = str(t._trans_ici(i.name)[1])
        i.explanation =  exp
        #print(i.explanation)
        i.save()
