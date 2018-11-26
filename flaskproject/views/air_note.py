from flask import Flask,render_template,request,Blueprint,redirect
import pymysql
import re,random,string
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
		sql = "create table air_note(id INT NOT NULL AUTO_INCREMENT primary key,pname char(20),context text,lock_path char(8) default '')"
		cursor.execute(sql)
		print('创建数据库air_note成功')

		#return 0        #不存在返回0

def is_tocreate_locknum():
	salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
	return salt
		
@air_note.route('/air/',methods=['GET'],endpoint='air')
def air():
	if request.method=='POST':
		return 'haha'
	return render_template('air_index.html')

@air_note.route('/air/<path:pname>',methods=['GET','POST'],)
def air_subpath(pname):
	print(pname)
	dic = {
		'lock':False,
		'pname':pname,
		'context':'',
		}
	if '/' not in pname:
		conn=pymysql.Connection(host='localhost',port=3306,user='root',passwd='chis1chang',db='t1',charset='utf8')
		cursor = conn.cursor()
		
		if request.method=="POST":
			context = request.form.get('a')
			if not context:
				print('delete everything')
				cursor.execute('delete  from air_note where pname=%s;',(pname))
				conn.commit()
				conn.close()
				return '已清理完毕'
				
			
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
			
				
			
			print(context)
			return '保存成功'
		
		
		cursor.execute('select * from air_note where pname=%s',(pname))
		data = cursor.fetchone()
		if not data:
			return render_template('air.html',**dic)
		#print(pname,data)
		
		dic['context']=data[2]
		if not request.args.get('get')=='lock':
			return render_template('air.html',**dic)
		
		#lock来到，请求只读页面
		if data[3]:
			return redirect('/air/s/%s'%data[3])
		else:
			#lock_path = is_tocreate_locknum()
			#cursor.execute('select * from air_note where lock_path=%s',(lock_path))
			#data = cursor.fetchone()
			while 1:
				
				lock_path=is_tocreate_locknum()
				data = cursor.execute('select * from air_note where lock_path=%s',(lock_path))
				if not data:
					break 
				
			cursor.execute('update air_note  set lock_path = %s where pname=%s;',(lock_path,pname))
			conn.commit()
			
			
			data = cursor.execute('select * from air_note where lock_path=%s',(lock_path))
			data =cursor.fetchone()
			dic['lock']=True
			dic['pname']=lock_path
			dic['context']=data[2]
			#print(dic)
			return render_template('air.html',**dic,)
	else:
		print('aaaa')
		a,lock_path= pname.rsplit('/')
		conn=pymysql.Connection(host='localhost',port=3306,user='root',passwd='chis1chang',db='t1',charset='utf8')
		cursor = conn.cursor()
		data = cursor.execute('select * from air_note where lock_path=%s',(lock_path))
		data =cursor.fetchone()
		if data:
			dic['lock']=True
			dic['pname']=lock_path
			dic['context']=data[2]
			print(dic)
			return render_template('air.html',**dic,)
		return redirect('/air')	
				
	

