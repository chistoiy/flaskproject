from flaskproject import create_app
from flask import render_template
app = create_app()


if __name__ == '__main__':
	
	app.run(host='172.17.255.83',port=5000)
