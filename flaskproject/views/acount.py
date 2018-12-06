from flask import Blueprint,render_template,abort 
ac = Blueprint('ac',__name__)

@ac.route('/')
def a():
	return render_template('index.html')

@ac.route('/acount')
def acount():
	
	return render_template('acount.html')
@ac.route('/ind' ,endpoint='ind')
def ind():
	return render_template('base.html')
	#return 'ahhaha'
	
@ac.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404	