#function to make the html file
def make_option_file(ccline, fname,next_node,num_line,statement):
    f1 = open('templates/page.html','w')
    f2 = open('templates/page.txt','r')
    f3 = open('templates/page-options.txt','r')
    # string1 = """\\v"""
    message =   """ 
            <html> 
                <body> 
                <p>"""+statement+"""</p>
                <form action="http://localhost:5000/next"  method = "POST">
                """
    for i in range(num_line):
        message = message+"""   <p>"""+ccline[i]+""" 
                    <button name="option" id="option"""+str(i+1)+"""" type = "submit"  value=\""""+next_node[i]+"""\">Submit</button> 
                    """
    message = message + """       
            </form>
        """

    message= message + """<body>
<div class="container">
<link type="text/css" rel="stylesheet" href="{{url_for('static', filename='css/materialize.min.css')}}"  media="screen,projection"/>

<div class="row">
<div class="pad-top"></div>
</div>
<div class="row"  style="text-align: center;">
        <div class="col s12 m12">
          <div class="card orange lighten-5">
            <div class="card-content">
<div class="row">
<div class="col s3 offset-s9">
</div>


    <!-- <h2></h2> -->
    <ul>

      <li><p>Click again to stop the recording. Press the play button to replay the recording </p></li>
    </ul>
    <select id="grammars">Select</select>
    <audio controls="controls"></audio>
    <span id="recording-indicator" ></span>
    <a style="display: inline;">Press to: Record/Stop </a>
    <button id="startBtn" style= ><i class="fa fa-microphone" aria-hidden="true" id="icon"></i>
</button>

          <span id="playing-indicator" ></span>
         <h10> <a style="display: inline;">Play </a></h10>
      <button id="play" title="Play" ><i class="fa fa-play" aria-hidden="true"></i></button>
      <a style="display: inline;">Evaluate </a>    
      <button id="eval" ><i class="fa fa-question" aria-hidden="true"></i></button>
      

          <a style="display: inline;">Say in phrase </a>
      
<!-- The Modal -->

  <!-- Modal content -->
 
    
<div class="row"  style="text-align: center;">
        <div class="col s10 m10 offset-s1 offset-m1">
          <div class="card brown lighten-4">
            <div class="card-content">
           <span class="card-title">Recognition Output</span>
            <div id="output" style="height:150px;overflow:auto;" >
            </div>
            </div>
          </div>
        </div>
    </div>
    <span class="card-title">Status</span>
    <div id="current-status">Loading page</div>

</div>
</div>
</div>
</div>
</div>
</div>


         
    <script>
      // These will be initialized later
      var recognizer, recorder, callbackManager, audioContext, outputContainer,rec;
      // Only when both recorder and recognizer do we have a ready application
      var isRecorderReady = isRecognizerReady = false;
      var choice="ONE"; //To hold the choice of the user
      // A convenience function to post a message to the recognizer and associate
      // a callback to its response
      function postRecognizerJob(message, callback) {
        var msg = message || {}; 
        if (callbackManager) msg.callbackId = callbackManager.add(callback);
        if (recognizer) recognizer.postMessage(msg);
      };
    //This function initializes an instance of the recorder
    //it posts a message right away and calls onReady when it
    //is ready so that onmessage can be properly set
      function spawnWorker(workerURL, onReady) {
          recognizer = new Worker(workerURL);
          recognizer.onmessage = function(event) {
            onReady(recognizer);
          };
          recognizer.postMessage('');
      };
      // To display the hypothesis sent by the recognizer
      function updateHyp(hyp) {
        if (outputContainer) 
          {outputContainer.innerHTML = hyp;
          }
          choice = hyp;
      };
      // This updates the UI when the app might get ready
      // Only when both recorder and recognizer are ready do we enable the buttons
      function updateUI() {
        if (isRecorderReady && isRecognizerReady) startBtn.disabled = false;
      };
      // This is just a logging window where we display the  
      function updateStatus(newStatus) {
        document.getElementById('current-status').innerHTML += "<br/>" + newStatus;
      };
      // A not-so-great recording indicator
     // A not-so-great recording indicator

      var audioContext = new AudioContext(); 
      function startUserMedia(stream) {
        var input = audioContext.createMediaStreamSource(stream);
        // Firefox hack https://support.mozilla.org/en-US/questions/984179
        window.firefox_audio_hack = input;
        var audioRecorderConfig = {errorCallback: function(x) {updateStatus("Error from recorder: " + x);}};
        recorder = new AudioRecorder(input, audioRecorderConfig);
        rec = new Recorder(input);
        // If a recognizer is ready, we pass it to the recorder
        if (recognizer) recorder.consumers = [recognizer];
        isRecorderReady = true;
        updateUI();
        updateStatus("Audio recorder ready");
      };
            // This starts recording. We first need to get the id of the grammar to use
       function startRecording() {
        var id = document.getElementById('grammars').value;
        if (recorder && recorder.start(id)) displayRecording(true)
        rec && rec.record();
      };

      // Stops recording
         function stopRecording() {
         rec && rec.stop();
         recorder && recorder.stop();
          
    };
      

          
  var playbackRecorderAudio = function (recorder, context) {
    recorder.getBuffer(function (buffers) {
      var source = context.createBufferSource();
      source.buffer = context.createBuffer(1, buffers[0].length, 44100);
      source.buffer.getChannelData(0).set(buffers[0]);
      source.connect(context.destination);

      source.start(0);
    });
  }
      var check = function(){
        var id = document.getElementById('icon')
        var img = id.getAttribute('class')
        
        if( img == "fa fa-microphone")
        {
          id.setAttribute("class","fa fa-stop");
          startRecording();
        }
        else
        { 

          id.setAttribute("class","fa fa-microphone");
                           """
    options = f3.read()
    message += options
    message += """

          stopRecording();
          document.getElementById('startBtn').checked = false;
        }
      };
      var playback = function(e){
          playbackRecorderAudio(rec, audioContext);
      }
      // Called once the recognizer is ready
      // We then add the grammars to the input select tag and update the UI
      var recognizerReady = function() {
           updateGrammars();
           isRecognizerReady = true;
           updateUI();
           updateStatus("Recognizer ready");
      };
      // We get the grammars defined below and fill in the input select tag
      var updateGrammars = function() {
        var selectTag = document.getElementById('grammars');
        for (var i = 0 ; i < grammarIds.length ; i++) {
            var newElt = document.createElement('option');
            newElt.value=grammarIds[i].id;
            newElt.innerHTML = grammarIds[i].title;
            selectTag.appendChild(newElt);
        }
      };
      // This adds a grammar from the grammars array
      // We add them one by one and call it again as
      // a callback.
      // Once we are done adding all grammars, we can call
      // recognizerReady()
      var feedGrammar = function(g, index, id) {
        if (id && (grammarIds.length > 0)) grammarIds[0].id = id.id;
        if (index < g.length) {
          grammarIds.unshift({title: g[index].title})
    postRecognizerJob({command: 'addGrammar', data: g[index].g},
                             function(id) {feedGrammar(grammars, index + 1, {id:id});});
        } else {
          recognizerReady();
        }
      };
      // This adds words to the recognizer. When it calls back, we add grammars
      var feedWords = function(words) {
           postRecognizerJob({command: 'addWords', data: words},
                        function() {feedGrammar(grammars, 0);});
      };
      // This initializes the recognizer. When it calls back, we add words
      var initRecognizer = function() {
          // You can pass parameters to the recognizer, such as : {command: 'initialize', data: [["-hmm", "my_model"], ["-fwdflat", "no"]]}
         
          postRecognizerJob({command: 'initialize',// data: [["-hmm", "my_model"], ["-fwdflat", "no"]]}
                             //callbackId: id,
                                data: [  //["-jsgf", "Start.jsgf"],
                              // ["-dict", "phonemes.dict"],
                               //  //["-hmm","my_model"],
                                ["-backtrace", "yes"],
                               ["-fsgusefiller","yes"],
                                ["-bestpath","yes"]
                                                              ]
                             },
                             
                            function(id) {
                                        if (recorder) recorder.consumers = [recognizer];
                                        feedWords(wordList);}
                                        );
      };
      // When the page is loaded, we spawn a new recognizer worker and call getUserMedia to
      // request access to the microphone
      window.onload = function() {
        outputContainer = document.getElementById("output");
        updateStatus("Initializing web audio and speech recognizer, waiting for approval to access the microphone");
        callbackManager = new CallbackManager();
        spawnWorker("static/js/recognizer.js", function(worker) {
            // This is the onmessage function, once the worker is fully loaded
            worker.onmessage = function(e) {
                // This is the case when we have a callback id to be called
                if (e.data.hasOwnProperty('id')) {
                  var clb = callbackManager.get(e.data['id']);
                  var data = {};
                  if ( e.data.hasOwnProperty('data')) data = e.data.data;
                  if(clb) clb(data);
                }
                // This is a case when the recognizer has a new hypothesis
                if (e.data.hasOwnProperty('hyp')) {
                  var newHyp = e.data.hyp;
                  if (e.data.hasOwnProperty('final') &&  e.data.final) newHyp = String(newHyp);
                  updateHyp(newHyp);
                }
                if (e.data.hasOwnProperty('stringer')) {
                  var newStringer = e.data.stringer;
                  newStringer =  String(newStringer);
                  if(e.data.hasOwnProperty('final')) 
                    { var finalString = [];
                      var i =0;
                      var word =[];
                      while(word!=["word"] && i<600)
                      {
                        if(String(newStringer[i])==" " || String(newStringer[i])==",")
                         { word =[];
                         }
                        else
                         { //console.log(word);
                          word += newStringer[i];
                        }
                        i++;
                      }
                      finalString = "word";
                      for(;String(newStringer[i])!="\\v";i++)
                      { if(String(newStringer[i]) == ",")
                        { finalString += "<br/>";
                          continue;
                        }
                        if(String(newStringer[i])== " ")
                        {
                          finalString += "&nbsp;"
                        }
                        finalString += newStringer[i];
                        
                      }
                      // document.getElementById('resultymf').innerHTML += "<br/>" + String(finalString) + '\\n';
                }
                }
                // This is the case when we have an error
                if (e.data.hasOwnProperty('status') && (e.data.status == "error")) {
                  updateStatus("Error in " + e.data.command + " with code " + e.data.code);
                }
            };
            // Once the worker is fully loaded, we can call the initialize function
            initRecognizer();
        });
        // The following is to initialize Web Audio
        try {
          window.AudioContext = window.AudioContext || window.webkitAudioContext;
          navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
          window.URL = window.URL || window.webkitURL;
          audioContext = new AudioContext();
        } catch (e) {
          updateStatus("Error initializing Web Audio browser");
        }
        if (navigator.getUserMedia) navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
                                        updateStatus("No live audio input in this browser");
                                    });
        else updateStatus("No web audio support in this browser");
      // Wiring JavaScript to the UI
      var startBtn = document.getElementById('startBtn');
      //var stopBtn = document.getElementById('stopBtn');
      startBtn.disabled = true;
      startBtn.onclick = check;
 
      play.onclick = playback;

      };

       // This is the list of words that need to be added to the recognizer
       // This follows the CMU dictionary format


    """

    grammars = f2.read()
    message += grammars
    message += """
          var grammars = [ {title: "Choices", g: grammarChoices}];
      var grammarIds = [];
    </script>
    <script >
            // Get the modal
  var modal = document.getElementById('myModal');
// Get the button that opens the modal
  var btn = document.getElementById("eval");
// Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];
// When the user clicks the button, open the modal 
  btn.onclick = function() {
    modal.style.display = "block";
}
// When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
}
// When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
    }
}
    </script>
    <!-- These are the two JavaScript files you must load in the HTML,
    The recognizer is loaded through a Web Worker -->

    <!-- These are the two JavaScript files you must load in the HTML,
    // The recognizer is loaded through a Web Worker -->
     <script src="{{url_for('static', filename='js/audioRecorder.js')}}"></script>
     <script src="{{url_for('static', filename='js/callbackManager.js')}}"></script>
     <script src="{{url_for('static', filename='js/audioRecorderWorker.js')}}"></script>
     <script src="{{url_for('static', filename='js/recorder.js')}}"></script>
     <script src="{{url_for('static', filename='js/recognizer.js')}}"></script>
     <script src="{{url_for('static', filename='js/materialize.min.js')}}"></script>


     <script src="https://code.jquery.com/jquery-2.1.1.min.js"></script>

     <script src="https://use.fontawesome.com/03f8396175.js"></script>
  </body>
</html>


    """


    f1.write(message)


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
      
      # print(next_node)
      # print(num_line)
      make_option_file(ccline,fname,next_node,num_line,statement)

# make_file("Step 1")





