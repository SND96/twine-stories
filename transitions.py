from re import compile
from collections import Counter

regexp = compile(r'\(.*\)')
CMUDICT = {}

def read_dict():
    with open('../sphinx4-5prealpha-src/sphinx4-data/src/main/resources/edu/cmu/sphinx/models/en-us/cmudict-en-us.dict',
              'r') as f:
        for line in f.readlines():
            dictline = line.strip().split()
            pronunciation = ' '.join(dictline[1:]).lower()
            if '(' in dictline[0]:
                headword = regexp.sub('', dictline[0], 1).lower()
            else:
                headword = dictline[0].lower()
            if headword in CMUDICT:
                CMUDICT[headword].append(pronunciation)
            else:
                CMUDICT[headword] = [pronunciation]

read_dict()

punct = compile(r'[,.?!]')


#function to make the jsgf file
def make_jsgf_file(ccline, fname,num_line):
    # print(fname)
    f = open('templates/page.txt','w')
    f1 = open('templates/page-options.txt','w')
    message=''
    message1 = 'var wordList = ['
    message2 = 'var grammarChoices = {numStates: 15, start: 0, end: 14, transitions: ['
    message3 = ''
    message4 = ''
    wordList = []
    choice_num = 0
    for i in range(num_line):
        state = 0
        sentence = punct.sub('',ccline[i].strip().lower())
        words = sentence.split()
        if(i == 0):
            message3 += '''if(choice=="'''+sentence+'''")
              {
                //document.getElementById("option1").click();
                decode_word = "'''+sentence+'''"
              }\n\t\t\t'''

        elif(i == 1):
            message3 += '''else if(choice=="'''+sentence+'''")
              {
               // document.getElementById("option2").click();
                decode_word = "'''+sentence+'''"
              }\n\t\t\t'''
        else:
            message3 += '''else if(choice=="'''+sentence+'''")
              {
                //document.getElementById("option3").click();
                decode_word = "'''+sentence+'''"
              }'''
        # if(i == 0):
        #     message3 += '''if(choice=="ONE")
        #       {
        #         document.getElementById("option1").click();
        #       }\n'''
        # elif(i == 1):
        #     message3 += '''else if(choice=="TWO")
        #       {
        #         document.getElementById("option2").click();
        #       }\n'''
        # else:
        #     message3 += '''else if(choice=="THREE")
        #       {
        #         document.getElementById("option3").click();
        #       }'''
             
             
        for word in words:
            try:
                # print(word)
                prons = CMUDICT[word]

                for pron in prons:
                    # print (wordList)
                    if(word not in wordList):
                        # print(word)
                        message1 += "[\""+word+"\", \""+str.upper(pron) + "\"], "
                        wordList = wordList+ [word]
                        # print((wordList))
                    message2 += "{from: "+str(state)+", to:" +str(state+1) +", word:\"" +word+"\"},"
                    break 
                    # f.write(message)
            
            except:
                print ( word )
            state+=1
        

    message1 = message1[:-1]
    message1 += '];\n\n'
    message2 = message2[:-1]
    message2 += ']};\n\n'
    #message1 = """var wordList = [["ONE", "W AH N"], ["TWO", "T UW"], ["THREE", "TH R IY"], ["FOUR", "F AO R"], ["FIVE", "F AY V"], ["SIX", "S IH K S"], ["SEVEN", "S EH V AH N"], ["EIGHT", "EY T"], ["NINE", "N AY N"], ["ZERO", "Z IH R OW"], ["NEW-YORK", "N UW Y AO R K"], ["NEW-YORK-CITY", "N UW Y AO R K S IH T IY"], ["PARIS", "P AE R IH S"] , ["PARIS(2)", "P EH R IH S"], ["SHANGHAI", "SH AE NG HH AY"], ["SAN-FRANCISCO", "S AE N F R AE N S IH S K OW"], ["LONDON", "L AH N D AH N"], ["BERLIN", "B ER L IH N"], ["SUCKS", "S AH K S"], ["ROCKS", "R AA K S"], ["IS", "IH Z"], ["NOT", "N AA T"], ["GOOD", "G IH D"], ["GOOD(2)", "G UH D"], ["GREAT", "G R EY T"], ["WINDOWS", "W IH N D OW Z"], ["LINUX", "L IH N AH K S"], ["UNIX", "Y UW N IH K S"], ["MAC", "M AE K"], ["AND", "AE N D"], ["AND(2)", "AH N D"], ["O", "OW"], ["S", "EH S"], ["X", "EH K S"],["name", "N EY M"],["sil",  "SIL"],["whats",  "W AH T S"],["your","Y UH R"]];"""
    #message2 = """var grammarDigits = {numStates: 1, start: 0, end: 0, transitions: [{from: 0, to: 0, word: "ONE"},{from: 0, to: 0, word: "TWO"},{from: 0, to: 0, word: "THREE"},{from: 0, to: 0, word: "FOUR"},{from: 0, to: 0, word: "FIVE"},{from: 0, to: 0, word: "SIX"},{from: 0, to: 0, word: "SEVEN"},{from: 0, to: 0, word: "EIGHT"},{from: 0, to: 0, word: "NINE"},{from: 0, to: 0, word: "ZERO"}]};"""
    f.write(message1)
    f.write(message2)
    f1.write(message3)

def make_option_files(node):
    with open('AROWF-recently.txt', 'r') as f:
        num_line = 0
        fname ="Start"
        #Variables used to signal the start of the parsing
        start = 0    
        begin = 0
        #Storing the options and the next node
        next_node = [""]*3
        ccline = [""]*3

        #For storing the question statement
        question = ":: "+node+"\n"
        statement = ""
        for line in f.readlines():
            alpha = 0


            if(line[0] == ":" and start == 1):
                break
            # print(line)
            # print(question)
            if(line == question):
                # print(line)
                start = 1

            elif(start != 1):
                continue

            if line[0]!='[':
              continue

            # print("Starting")
            length = len(line)

            for i in range (length):
                #check = isalpha(line[i])
                if (line[i] == '.'):
                    break
                if ((line[i].isalpha()) or (line[i].isspace())):
                    ccline[num_line]+=line[i]


        # print(next_node)
            num_line += 1            
                
        make_jsgf_file(ccline,fname,num_line)

# make_option_files("Step 1")


    