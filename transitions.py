from re import compile

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
    f = open('templates/'+fname+'.txt','w')
    message=''
    message1 = 'var wordList = ['
    message2 = 'var grammarDigits = {numStates: 15, start: 0, end: 14, transitions: ['
    for i in range(num_line):
        state = 0
        words = punct.sub('', ccline[i].strip().lower()).split()
        for word in words:
            try:
                # print(word)
                prons = CMUDICT[word]
                for pron in prons:
                    message1 += "[\""+word+"\", \""+pron + "\"],"
                    message2 += "{from: "+str(state)+", to:" +str(state+1) +", word:\"" +word+"\"}," 
                    # f.write(message)
            
            except:
                print ( word )
            state+=1
        # message2

    message1 = message1[:-1]
    message1 += '];\n\n'
    message2 = message2[:-1]
    message2 += ']};'

    f.write(message1)
    f.write(message2)


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
    question = 0 
    statement = ""
    for line in f.readlines():
        alpha = 0
        if(question):
            statement = line
            question = 0

        if line[:8] == ":: Start":
            start = 1
            begin = 1
            question = 1

        elif (line[0] == ':' and start == 1) :
            question = 1                           
            begin = 0
            make_jsgf_file(ccline,fname,num_line)
            num_line = 0
            next_node = [""]*3
            ccline = [""]*3
            fname=""
            for i in range (len(line)):
                if(line[i].isalpha()):
                    alpha = 1
                    
                if(alpha == 1 and line[i].isspace() == 0 ):
                    fname += line[i]
            begin = 1
        if(start!=1 and begin!=1):
            continue
        
        if line[0]!='[':
            continue

        length = len(line)
        alpha = 0
        node = 0
        initial = 0
        for i in range (length):
            #check = isalpha(line[i])
            if (line[i] == '.'):
                break
            if ((line[i].isalpha()) or (line[i].isspace())):
                ccline[num_line]+=line[i]


        # print(next_node)
        num_line += 1            
            

    num_line -= 1
    make_jsgf_file(ccline,fname,num_line)


    