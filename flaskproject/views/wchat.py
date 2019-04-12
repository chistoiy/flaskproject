from flask import Flask,render_template,request,Blueprint,redirect
import pymysql
import re,random,string
wchat = Blueprint('wchat',__name__)

 
 
		
@air_note.route('/wchat/',methods=['GET'],endpoint='wchat')
def wchat():
	if request.method=='GET':
		return 'haha'


 