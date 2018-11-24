from flask import Flask,render_template
from .views.acount import ac
def create_app():


	app = Flask(__name__)
	
	app.register_blueprint(ac)
	#app.register_blueprint(uc,url_profix='/xxx'),相当于访问这个url时，这一组url均为/xxx/list和/xxx/detail
	#@app.before_request
	#def xxx():
	#	return 'look out!'
	@app.errorhandler(404)
	def page_not_found(e):
		return render_template('404.html'),404	
	
	return app