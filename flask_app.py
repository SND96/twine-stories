from flask import Flask, request, session, redirect, url_for, \
                  send_from_directory, render_template

from parser import make_file
from transitions import make_option_files

app = Flask(__name__)

@app.route('/')
def Start():
	make_option_files("Start")
	make_file("Start")
	return render_template('page.html')

@app.route('/next', methods =['POST'])
def  next():
	if request.method == 'POST':
		form = request.form['option']
		print(form)
		make_option_files(form)
		make_file(form)

		return render_template('page.html')
        # return redirect(url_for('options',next_node=form))

@app.route('/options/<next_node>')
def options(next_node):
    return render_template(next_node+'.html')


if __name__ == '__main__':
   app.run(debug = True)
