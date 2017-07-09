
def make_option_file(ccline, fname,next_node,num_line):
    f = open('templates/'+fname+'.html','w')
    message =   """ 
            <html> 
                <body> 
                <p>Hi! This is a node in a Twee story. Do you want to....</p>
                <form action="http://localhost:5000/next"  method = "POST">
                """
    for i in range(num_line):
        message = message+"""   <p>"""+ccline[i]+""" 
                    <button type = "submit"  value=\""""+next_node[i]+"""\">Submit</button> 
                    """
    message = message + """       
            </form>
                 </body>
            </html>
        """
    f.write(message)


with open('AROWF-recently.txt', 'r') as f:
    done = {}
    num_line = 0
    fname ="Start"
    start = 0
    first = 0
    next_node = [""]*3
    ccline = [""]*3
    begin = 0
    for line in f.readlines():
        alpha = 0
        
        if line[:8] == ":: Start":
            start = 1
            begin = 1

        elif (line[0] == ':' and start == 1) :
                       
            begin = 0
            make_option_file(ccline,fname,next_node,num_line)
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
        print(fname)
        if(start!=1 and begin!=1):
            continue
 
        if line[0]!='[':
            continue

        length = len(line)
        alpha = 0
        node = 0
        initial = 0
        for i in range (length):
            if (line[i] == '.'):
                node = i
                break
            if line[i].isalpha():
                alpha = 1
            if (alpha):
                ccline[num_line] += line[i]


        for i in range (node,length):
            if(line[i] == ']'):
                break            
            if(initial==1 and line[i].isspace()==0):
                next_node[num_line] += line[i]
            if(line[i] == '>'):
                initial = 1
        # print(next_node)
        num_line += 1            
            

    num_line -= 1
    make_option_file(ccline,fname,next_node,num_line)







