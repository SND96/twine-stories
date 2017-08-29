def make_file(node):
  with open('AROWF-recently.txt', 'r') as f:
      num_line = 0
      fname ="Start"
      #Variables used to signal the start of the parsing
      start = 0    
      begin = 0
      #Storing the options and the next node
      next_node = [""]*3
      ccline = [""]*3
      node = ":: "+node+"\n"
      question = 0

      #For storing the question statement
      statement = ""
      for line in f.readlines():
          alpha = 0
          if(question):
              statement += line
              # question = 0
  
          if(line[0] == ":" and start == 1):
            break

          if(line == node):
            start = 1
            question = 1

          elif(start!=1):
            continue

          if line[0]!='[':
              continue

          question = 0

          statement = statement[:statement.rfind('\n')]
          length = len(line)
          # print(line)
          alpha = 0
          nodes = 0
          initial = 0
          for i in range (length):
              if (line[i] == '.'):
                  nodes = i
                  break
              if line[i].isalpha():
                  alpha = 1
              if (alpha):
                  ccline[num_line] += line[i]


          for i in range (nodes,length):
              if(line[i] == ']'):
                  break
              if(initial == 2):
                  next_node[num_line] += line[i]

              if(initial==1 and line[i].isspace()==0):
                  next_node[num_line] += line[i]
                  initial = 2
              if(line[i] == '>'):
                  initial = 1
          num_line += 1            
      return(next_node, num_line, statement, ccline)





