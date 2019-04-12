from flask import Flask,render_template,request,Blueprint,redirect
import pymysql
import re,random,string
import hashlib
import xmltodict,time
wc = Blueprint('wchat',__name__)

 
 
		
@wc.route('/wchat/',methods=['GET'],endpoint='wchat')
def wchat():
	
    if request.method == 'GET':
        #这里改写你在微信公众平台里输入的token
        token = '123456'
        #获取输入参数
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        #字典排序
        list = [token, timestamp, nonce]
        list.sort()

        s = list[0] + list[1] + list[2]
        #sha1加密算法        
        hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()
        #如果是来自微信的请求，则回复echostr
        if hascode == signature:
            return echostr
        else:
            return ""
    if request.method == 'POST':
        #这里改写你在微信公众平台里输入的token
        token = '123456'
        dict_data = xmltodict.parse(request.get_data())
        print(dict_data)		
        dict_data = xmltodict['xml']['MsgType'] 
        if msg_type =='text':
            content = dict_data['xml']['Content']
            resp_data={'xml':{"ToUserName":dict_data['xml']['FromUserName'],
                       'FromUserName': dict_data['xml']['ToUserName'],
                       'CreateTime': int(time.time()),
                       'MsgType':'text',
                       'Content':content,}}
            return xmltpdict.unparse(resp_data)
		


 