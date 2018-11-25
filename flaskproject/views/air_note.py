from flask import Flask,render_template,request,Blueprint
import pymysql
import re
air_note = Blueprint('air_note',__name__)

def is_to_create_table():        #这个函数用来判断表是否存在
	conn=pymysql.Connection(host='localhost',port=3306,user='root',passwd='chis1chang',db='t1',charset='utf8')
	cursor = conn.cursor()
	sql = 'show tables;'
	cursor.execute(sql)
	tables = [cursor.fetchall()]
	table_list = re.findall('(\'.*?\')',str(tables))
	table_list = [re.sub("'",'',each) for each in table_list]
	if 'air_note' in table_list:
		pass
		#return 1        #存在返回1
	else:
		sql = "create table air_note(id INT NOT NULL AUTO_INCREMENT primary key,pname char(20),context text)"
		cursor.execute(sql)
		print('创建数据库air_note成功')
		#return 0        #不存在返回0

@air_note.route('/air/<pname>',methods=['GET','POST'])
def air(pname):
	conn=pymysql.Connection(host='localhost',port=3306,user='root',passwd='chis1chang',db='t1',charset='utf8')
	
	cursor = conn.cursor()
	if request.method=="POST":
		context = request.form.get('a')
		cursor.execute('select * from air_note where pname=%s',(pname))
		c = cursor.fetchone()
		if c:
			print('存在')
			cursor.execute('update air_note  set context = %s where pname=%s;',(context,pname))
			conn.commit()
			conn.close()
		else:
			cursor.execute('insert into air_note(pname,context) value(%s,%s);',(pname,context.encode('utf-8')))
			conn.commit()
			conn.close()
		if not context:
			print('delete everything')
			
		
		print(context)
		return '保存成功'
	
	
	cursor.execute('select * from air_note where pname=%s',(pname))
	data = cursor.fetchone()
	if not data:
		return render_template('air.html')
	print(pname,data)
	return render_template('air.html',d=data[1])
	
