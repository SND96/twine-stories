from flask import Flask, request, session, redirect, url_for, \
                  send_from_directory, render_template

app = Flask(__name__)

@app.route('/')
def Start():
    return render_template('Start.html')

@app.route('/next', methods =['POST'])
def  next():
    if request.method == 'POST':
        form = request.form['option']
       	# print(next_node)
        return redirect(url_for('options',next_node=form))

@app.route('/options/<next_node>')
def options(next_node):
    return render_template(next_node+'.html')


if __name__ == '__main__':
   app.run(debug = True)
