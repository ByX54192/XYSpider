import requests
import json
import pymongo
import time
import random

class SaveData(object):
	"""docstring for SaveData"""
	def __init__(self, arg):
		super(SaveData, self).__init__()
		self.ip = arg
		myclient=pymongo.MongoClient('mongodb://{}:27017/'.format(self.ip))
		mydb=myclient['XianYu']
		self.__mycol=mydb['Watches2']
	def dbObj(self):
		mycol=self.__mycol
		return mycol

def connectAPI(parame):
	headers={
	    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	    'accept-encoding': 'gzip, deflate, br',
	    'accept-language':'zh-CN,zh;q=0.9',
	    'cache-control': 'max-age=0',
	    'cookie': 'mt=ci%3D-1_0; t=411d101aadb963ed3c2828f019d332ab; thw=cn; cna=ZJf5E0ObVFsCAcp/HMdB28Xp; mt=ci%3D-1_0; UM_distinctid=165d78f074725f-0f86bece647812-5701732-1aeaa0-165d78f074856e; cookie2=1f6df40f8035a2619200f523cd5bc1c0; v=0; _tb_token_=3ee5e8383b65a; CNZZDATA1252911424=1894482996-1536919166-https%253A%252F%252F2.taobao.com%252F%7C1537077096; CNZZDATA30058275=cnzz_eid%3D1793920906-1536914610-https%253A%252F%252F2.taobao.com%252F%26ntime%3D1537076740; isg=BBkZNYPpphWZK3qHI5y3_555KAUzDmM-CxG2EjvOlcC_QjnUg_YdKIdwQEaReqWQ',
	    #'referer': 'https://2.taobao.com/',
	    'upgrade-insecure-requests':'1',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
	}
	api='https://s.2.taobao.com/list/waterfall/waterfall.htm?stype=1&&{}'.format(parame)
	response = requests.get(api,headers=headers).text.replace('(','').replace(')','')
	webdata=json.loads(response)
	totalPage=webdata['totalPage']
	return totalPage
def getData(parame,page):
	headers={
	    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	    'accept-encoding': 'gzip, deflate, br',
	    'accept-language':'zh-CN,zh;q=0.9',
	    'cache-control': 'max-age=0',
	    'cookie': 'mt=ci%3D-1_0; swfstore=276201; t=411d101aadb963ed3c2828f019d332ab; thw=cn; cna=ZJf5E0ObVFsCAcp/HMdB28Xp; UM_distinctid=165d78f074725f-0f86bece647812-5701732-1aeaa0-165d78f074856e; cookie2=1f6df40f8035a2619200f523cd5bc1c0; v=0; _tb_token_=3ee5e8383b65a; skt=628d2beff5cecd36; csg=e5a943ab; uc3=vt3=F8dBzrVI27uJiuOo6xI%3D&id2=UUpkvvAJmOaDlw%3D%3D&nk2=FP0fUcLS&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; existShop=MTUzNzA4OTgyNA%3D%3D; tracknick=wdff24; lgc=wdff24; _cc_=V32FPkk%2Fhw%3D%3D; dnk=wdff24; tg=0; CNZZDATA1252911424=1894482996-1536919166-https%253A%252F%252F2.taobao.com%252F%7C1537088065; CNZZDATA30058275=cnzz_eid%3D1793920906-1536914610-https%253A%252F%252F2.taobao.com%252F%26ntime%3D1537087661; mt=ci=43_1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; uc1=cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&cookie21=URm48syIZJwTkNGk7euL6g%3D%3D&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&existShop=false&pas=0&cookie14=UoTfLJVHGYx%2BSg%3D%3D&tag=8&lng=zh_CN; whl=-1%260%260%261537092562295; isg=BDU14rKCgmoIxObTr-jT09q1RLEvGoeiT-1K5rdaZazZjlWAfgC6lEZP3BIdzgF8',
	    #'referer': 'https://2.taobao.com/',
	    'upgrade-insecure-requests':'1',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
	}
	api='https://s.2.taobao.com/list/waterfall/waterfall.htm?stype=1&page={}&{}'.format(page,parame)
	response = requests.get(api,headers=headers).text.replace('(','').replace(')','')
	jsonStr = response.encode('utf-8')
	webdata = json.loads(jsonStr)
	idles=webdata['idle']
	currPage=webdata['currPage']
	return idles,currPage

if __name__ == '__main__':
	mycol=SaveData('192.168.110.146').dbObj()
	parame="catid=50100500&st_trust=1&q=%BB%FA%D0%B5&ist=1"

	totalPage=connectAPI(parame)
	PriviousPage=0
	for i in range(1,int(totalPage)//3+1):
		try:
			idles,page=getData(parame,i)
		except:
			print("get Data Error"+str(i))
			continue
		if PriviousPage!=page:
			print("已经获取第{}页".format(i))
			print('CurrentPage'+str(page))
			'''记录上一页'''
			PriviousPage=page
			for num,pr in enumerate(idles):
				mycol.insert_one(pr)
			time.sleep(random.randint(1,10))
		else:
			print("Done!!!")
	print('Stay Young!')
		

    