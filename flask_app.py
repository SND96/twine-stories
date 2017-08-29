from flask import Flask, request, session, redirect, url_for, \
                  send_from_directory, render_template

from parser import make_file
from transitions import make_option_files

import json




app = Flask(__name__)


@app.route('/')
def Start():
	next_node, lines, question, option =  make_file("Start")
	strings, wordList = make_option_files("Start")
	return render_template('Start.html' , next1 = next_node[0], next2 = next_node[1], next3 = next_node[2], question = question, option1 = option[0], option2 = option[1] , option3 = option[2], choice1 = strings[0], choice2 = strings[1], choice3 = strings[2], wordList = wordList[0], grammarChoices = wordList[1])

@app.route('/next', methods =['POST'])
def  next():
	if request.method == 'POST':
		form = request.form['option']
		# Page for the pronunciation evaluation.
		if(form == "PronEval"):
			return render_template('PronEval.html')
		# Page for inteligibility remediation information.
		elif(form == "Info"):
			return render_template('Info.html')
		elif(form == "Start"):
			next_node, lines, question, option =  make_file("Start")
			strings, wordList = make_option_files("Start")
			return render_template('Start.html' , next1 = next_node[0], next2 = next_node[1], next3 = next_node[2], question = question, option1 = option[0], option2 = option[1] , option3 = option[2], choice1 = strings[0], choice2 = strings[1], choice3 = strings[2], wordList = wordList[0], grammarChoices = wordList[1])
		else:
			next_node, lines, question, option =  make_file(form)
			strings, wordList = make_option_files(form)
			print(lines)
			if(lines == 3):
				return render_template('page.html' , next1 = next_node[0], next2 = next_node[1], next3 = next_node[2], question = question, option1 = option[0], option2 = option[1] , option3 = option[2], choice1 = strings[0], choice2 = strings[1], choice3 = strings[2],wordList = wordList[0], grammarChoices = wordList[1])
			else:
				return render_template('end_page.html' , next1 = next_node[0], question = question, option1 = option[0], choice1 = strings[0], wordList = wordList[0], grammarChoices = wordList[1])


if __name__ == '__main__':
   app.run(debug = True)
