#Alex Holcombe alex.holcombe@sydney.edu.au
#See the github repository for more information: https://github.com/alexholcombe/twoWords
from __future__ import print_function #use python3 style print
from psychopy import monitors, visual, event, data, logging, core, sound, gui
import psychopy.info
import numpy as np
from math import atan, log, ceil, sin,radians, cos
import copy
import time, sys, os, pylab, random
from EyelinkEyetrackerForPsychopySUPA3 import EyeLinkCoreGraphicsPsychopy, Tracker_EyeLink #Chris Fajou integration
try:
    from noiseStaircaseHelpers import printStaircase, toStaircase, outOfStaircase, createNoise, plotDataAndPsychometricCurve
except ImportError:
    print('Could not import from noiseStaircaseHelpers.py (you need that file to be in the same directory)')
try:
    import stringResponseKRedit
except ImportError:
    print('Could not import stringResponseKRedit.py (you need that file to be in the same directory)')

eyetracking = False; eyetrackFileGetFromEyelinkMachine = False #very timeconsuming to get the file from the Windows machine over the ethernet cable, 

limitedTest = False;


# Opening wordlists

def getWords(sample):
    name = open(sample)
    output = [x.rstrip() for x in name.readlines()]
    print(output)
    return output

Sample1 = getWords("Sample1.txt")
Sample2 = getWords("Sample2.txt")
Sample3 = getWords("Sample3.txt")
Sample4 = getWords("Sample4.txt")
Sample5 = getWords("Sample5.txt")
Sample6 = getWords("Sample6.txt")
PracSample1 = getWords("Prac1.txt")

lettersUnparsed="a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z" 
SampleLetters = lettersUnparsed.split(",") #split into list
for i in range(len(SampleLetters)):
    SampleLetters[i] = SampleLetters[i].replace(" ", "") #delete spaces

print("SampleLetters",SampleLetters)

#for j in range(len(i)):
#        i[j] = i[j].replace(" ", "") #delete spaces
#        print(i)
#    return(i)

#wordEccentricity=3 #degrees of visual angle away from the fixation point
tasks=['T1']; task = tasks[0]
#THINGS THAT COULD PREVENT SUCCESS ON A NEW MACHINE
#same screen or external screen? Set scrn=0 if one screen. scrn=1 means display stimulus on second screen.
#widthPix, heightPix
quitFinder = False #if checkRefreshEtc, quitFinder becomes True.
autopilot=False
demo=False #False
exportImages= False #quits after one trial
subject='Hubert' #user is prompted to enter true subject name
if autopilot: subject='auto'
if os.path.isdir('.'+os.sep+'data'):
    dataDir='data'
else:
    print('"data" directory does not exist, so saving data in present working directory')
    dataDir='.'
timeAndDateStr = time.strftime("%d%b%Y_%H-%M", time.localtime())
trialClock = core.Clock()

showRefreshMisses=True #flicker fixation at refresh rate, to visualize if frames missed
feedback=True
autoLogging=False
refreshRate = 60.;  #100
if demo:
    refreshRate = 60.;  #100

staircaseTrials = 25
prefaceStaircaseTrialsN = 20 #22
prefaceStaircaseNoise = np.array([5,20,20,20,50,50,50,5,80,80,80,5,95,95,95]) #will be recycled / not all used, as needed
descendingPsycho = True #psychometric function- more noise means worse performance
threshCriterion = 0.58
pracTrials = 10
numWordsInStream = 18
instrLtrHeight = 0.8
instrcolor = 'white'
#moving this bit under trial handler
#wordsUnparsed="time, good, work, file, game, home, card, data, mail, best, show, hard, post, year, case, book, read, name, back, life, send, down, read, high" #24 most common words

instructionTextL1 = """On each trial, a rapid stream of letters will appear at two different locations on the screen.\n
The two streams will be simultaneous, but the order of letters will be different in each stream.\n 
The locations of the two streams will be cued before each trial.\n\n
Press any key for more instructions."""

instructionTextL2 = """At some time during the trial, white circles will appear around both streams.\n
Your task is to report the letter that was displayed in each stream at the time that the circles appeared.\n
The letters may be any in the alphabet\n\n
Press any key for more instructions."""

instructionTextL3 = """Please keep your eyes fixated on the white dot at the centre of the screen at all times during the trial.\n
After each trial, please clearly say the letter that you saw in each stream when the circles appeared.\n
If you are unsure, please make your best guess.\n\n
Press any key for more instructions."""

instructionTextW1 = """On each trial, a rapid stream of words will appear at two different locations on the screen.\n
The two streams will be simultaneous, but the words will be different in each stream.\n 
The locations of the two streams will be cued before each trial.\n\n
Press any key for more instructions."""

instructionTextW2 = """At some time during the trial, white circles will appear around both streams.\n
Your task is to report the word that was displayed in each stream at the time that the circles appeared.\n
The words are all four letter words\n\n
Press any key for more instructions."""

instructionTextW3 = """Please keep your eyes fixated on the white dot at the centre of the screen at all times during the trial.\n
After each trial, please clearly say the word that you saw in each stream when the circles appeared.\n
If you are unsure, please make your best guess.\n\n
Press any key for more instructions."""

instructionText4 = 'If you have any questions, please ask the experimenter now.\n\nPress any key to begin some practice trials.'

nextBlock1 = """You have now completed the first block.  There are two blocks altogether.\n\n
Take a short break and press a key to continue"""

nextBlockL2 = """The next block is just the same as the first one, except the streams contain letters instead of words.\n
Your task is to report the letter that was displayed in each stream at the time that the circles appeared.\n
The letters may be any in the alphabet\n\n
Press any key for more instructions."""

nextBlockW2 = """The next block is just the same as the first one, except the streams contain words instead of letters.\n
Your task is to report the word that was displayed in each stream at the time that the circles appeared.\n
The words are all four letter words\n\n
Press any key for more instructions."""

finishedPractice  = """You have completed the practice trials.  If you have any questions, please ask the experimenter now.\n\n
Press any key to begin the experiment."""

instructionTextSkipped = 'Plese press any key to begin some practice trials.'

skippedText = 'Please press any key to begin the experiment.'

def instructions(condition):
            
            if condition==0:
                text1 = instructionTextL1
                text2 = instructionTextL2
                text3 = instructionTextL3
            else:
                text1 = instructionTextW1
                text2 = instructionTextW2
                text3 = instructionTextW3


            Instructions1 = visual.TextStim(myWin, text = text1,pos=(0, 0),height=instrLtrHeight,colorSpace='rgb',color=instrcolor,alignHoriz='center',alignVert='center',units='deg',autoLog=autoLogging )
            Instructions2 = visual.TextStim(myWin, text = text2,pos=(0, 0),height=instrLtrHeight,colorSpace='rgb',color=instrcolor,alignHoriz='center',alignVert='center',units='deg',autoLog=autoLogging )
            Instructions3 = visual.TextStim(myWin, text = text3,pos=(0, 0),height=instrLtrHeight,colorSpace='rgb',color=instrcolor,alignHoriz='center',alignVert='center',units='deg',autoLog=autoLogging )
            Instructions4 = visual.TextStim(myWin, text = instructionText4,pos=(0, 0),height=instrLtrHeight,colorSpace='rgb',color=instrcolor,alignHoriz='center',alignVert='center',units='deg',autoLog=autoLogging )

            Instructions1.draw()
            myWin.flip()
            event.waitKeys()
            Instructions2.draw()
            myWin.flip()
            event.waitKeys()
            Instructions3.draw()
            myWin.flip()
            event.waitKeys()
            Instructions4.draw()
            myWin.flip()
            event.waitKeys()

def block2instructions(condition):
            
            if condition==0:
                b2text2 = nextBlockL2
            else:
                b2text2 = nextBlockW2


            NextBlockInstructions1 = visual.TextStim(myWin, text = nextBlock1,pos=(0, 0),height=instrLtrHeight,colorSpace='rgb',color=instrcolor,alignHoriz='center',alignVert='center',units='deg',autoLog=autoLogging )
            NextBlockInstructions2 = visual.TextStim(myWin, text = b2text2,pos=(0, 0),height=instrLtrHeight,colorSpace='rgb',color=instrcolor,alignHoriz='center',alignVert='center',units='deg',autoLog=autoLogging )
            NextBlockInstructions3 = visual.TextStim(myWin, text = instructionText4,pos=(0, 0),height=instrLtrHeight,colorSpace='rgb',color=instrcolor,alignHoriz='center',alignVert='center',units='deg',autoLog=autoLogging )

            NextBlockInstructions1.draw()
            myWin.flip()
            event.waitKeys()
            NextBlockInstructions2.draw()
            myWin.flip()
            event.waitKeys()
            NextBlockInstructions3.draw()
            myWin.flip()
            event.waitKeys()

bgColor = [-.7,-.7,-.7] # [-1,-1,-1]
cueColor = [1.,1.,1.]
letterColor = [1.,1.,1.]
cueRadius = 2.9 #6 deg in Goodbourn & Holcombe
widthPix= 1440 #monitor width in pixels of Agosta
heightPix= 900 #800 #monitor height in pixels
monitorwidth = 36 #monitor width in cm
scrn=1 #0 to use main screen, 1 to use external screen connected to computer
fullscr=True #True to use fullscreen, False to not. Timing probably won't be quite right if fullscreen = False
allowGUI = False
if demo: monitorwidth = 23#18.0
if exportImages:
    widthPix = 600; heightPix = 600
    monitorwidth = 13.0
    fullscr=False; scrn=0
    framesSaved=0
if demo:    
    scrn=0; fullscr=False
    widthPix = 800; heightPix = 600
    monitorname='testMonitor'
    allowGUI = True
viewdist = 57. #cm
pixelperdegree = widthPix/ (atan(monitorwidth/viewdist) /np.pi*180)
print('pixelperdegree=',pixelperdegree)
    
# create a dialog from dictionary 
infoFirst = { 'Do staircase (only)': False, 'Check refresh etc':True, 'Fullscreen (timing errors if not)': False, 'Screen refresh rate':refreshRate, 'Show instructions': False, 'Practice Trials': False }
OK = gui.DlgFromDict(dictionary=infoFirst, 
    title='Dual-RSVP experiment OR staircase to find thresh noise level for performance criterion', 
    order=['Do staircase (only)', 'Check refresh etc', 'Fullscreen (timing errors if not)','Show instructions', 'Practice Trials'], 
    tip={'Check refresh etc': 'To confirm refresh rate and that can keep up, at least when drawing a grating'},
    #fixed=['Check refresh etc'])#this attribute can't be changed by the user
    )
if not OK.OK:
    print('User cancelled from dialog box'); core.quit()
doStaircase = infoFirst['Do staircase (only)']
checkRefreshEtc = infoFirst['Check refresh etc']
fullscr = infoFirst['Fullscreen (timing errors if not)']
refreshRate = infoFirst['Screen refresh rate']
showInstr = infoFirst['Show instructions']
practiceTrials = infoFirst['Practice Trials']
if checkRefreshEtc:
    quitFinder = True 
if quitFinder:
    import os
    applescript="\'tell application \"Finder\" to quit\'"
    shellCmd = 'osascript -e '+applescript
    os.system(shellCmd)




AngleToStim = 30
#letter size 2.5 deg
SOAms = 2200 #170 #133 #Battelli, Agosta, Goodbourn, Holcombe mostly using 133
#Minimum SOAms should be 84  because any shorter, I can't always notice the second ring when lag1.   71 in Martini E2 and E1b (actually he used 66.6 but that's because he had a crazy refresh rate of 90 Hz)
letterDurMs =  1800 #130 #80 #23.6  in Martini E2 and E1b (actually he used 22.2 but that's because he had a crazy refresh rate of 90 Hz)

ISIms = SOAms - letterDurMs
letterDurFrames = int( np.floor(letterDurMs / (1000./refreshRate)) )
cueDurFrames = letterDurFrames
ISIframes = int( np.floor(ISIms / (1000./refreshRate)) )
#have set ISIframes and letterDurFrames to integer that corresponds as close as possible to originally intended ms
rateInfo = 'total SOA=' + str(round(  (ISIframes + letterDurFrames)*1000./refreshRate, 2)) + ' or ' + str(ISIframes + letterDurFrames) + ' frames, comprising\n'
rateInfo+=  'ISIframes ='+str(ISIframes)+' or '+str(ISIframes*(1000./refreshRate))+' ms and letterDurFrames ='+str(letterDurFrames)+' or '+str(round( letterDurFrames*(1000./refreshRate), 2))+'ms'
logging.info(rateInfo); print(rateInfo)

trialDurFrames = int( numWordsInStream*(ISIframes+letterDurFrames) ) #trial duration in frames

monitorname = 'testmonitor'
waitBlank = False
mon = monitors.Monitor(monitorname,width=monitorwidth, distance=viewdist)#relying on  monitorwidth cm (39 for Mitsubishi to do deg calculations) and gamma info in calibratn
mon.setSizePix( (widthPix,heightPix) )
units='deg' #'cm'
def openMyStimWindow(): #make it a function because have to do it several times, want to be sure is identical each time
    myWin = visual.Window(monitor=mon,size=(widthPix,heightPix),allowGUI=allowGUI,units=units,color=bgColor,colorSpace='rgb',fullscr=fullscr,screen=scrn,waitBlanking=waitBlank) #Holcombe lab monitor
    return myWin
myWin = openMyStimWindow()
refreshMsg2 = ''
if not checkRefreshEtc:
    refreshMsg1 = 'REFRESH RATE WAS NOT CHECKED'
    refreshRateWrong = False
else: #checkRefreshEtc
    runInfo = psychopy.info.RunTimeInfo(
            # if you specify author and version here, it overrides the automatic detection of __author__ and __version__ in your script
            #author='<your name goes here, plus whatever you like, e.g., your lab or contact info>',
            #version="<your experiment version info>",
            win=myWin,    ## a psychopy.visual.Window() instance; None = default temp window used; False = no win, no win.flips()
            refreshTest='grating', ## None, True, or 'grating' (eye-candy to avoid a blank screen)
            verbose=True, ## True means report on everything 
            userProcsDetailed=True  ## if verbose and userProcsDetailed, return (command, process-ID) of the user's processes
            )
    #print(runInfo)
    logging.info(runInfo)
    print('Finished runInfo- which assesses the refresh and processes of this computer') 
    #check screen refresh is what assuming it is ##############################################
    Hzs=list()
    myWin.flip(); myWin.flip();myWin.flip();myWin.flip();
    myWin.setRecordFrameIntervals(True) #otherwise myWin.fps won't work
    print('About to measure frame flips') 
    for i in range(50):
        myWin.flip()
        Hzs.append( myWin.fps() )  #varies wildly on successive runs!
    myWin.setRecordFrameIntervals(False)
    # end testing of screen refresh########################################################
    Hzs = np.array( Hzs );     Hz= np.median(Hzs)
    msPerFrame= 1000./Hz
    refreshMsg1= 'Frames per second ~='+ str( np.round(Hz,1) )
    refreshRateTolerancePct = 3
    pctOff = abs( (np.median(Hzs)-refreshRate) / refreshRate)
    refreshRateWrong =  pctOff > (refreshRateTolerancePct/100.)
    if refreshRateWrong:
        refreshMsg1 += ' BUT'
        refreshMsg1 += ' program assumes ' + str(refreshRate)
        refreshMsg2 =  'which is off by more than' + str(round(refreshRateTolerancePct,0)) + '%!!'
    else:
        refreshMsg1 += ', which is close enough to desired val of ' + str( round(refreshRate,1) )
    myWinRes = myWin.size
    myWin.allowGUI =True
myWin.close() #have to close window to show dialog box

defaultNoiseLevel = 0.0 #to use if no staircase, can be set by user
trialsPerCondition = 1 #default value
firstCondition = 1
dlgLabelsOrdered = list()
if doStaircase:
    myDlg = gui.Dlg(title="Staircase to find appropriate noisePercent", pos=(200,400))
else: 
    myDlg = gui.Dlg(title="RSVP experiment", pos=(200,400))
if not autopilot:
    myDlg.addField('Subject name (default="Hubert"):', 'Hubert', tip='or subject code')
    dlgLabelsOrdered.append('subject')
if doStaircase:
    easyTrialsCondText = 'Num preassigned noise trials to preface staircase with (default=' + str(prefaceStaircaseTrialsN) + '):'
    myDlg.addField(easyTrialsCondText, tip=str(prefaceStaircaseTrialsN))
    dlgLabelsOrdered.append('easyTrials')
    myDlg.addField('Staircase trials (default=' + str(staircaseTrials) + '):', tip="Staircase will run until this number is reached or it thinks it has precise estimate of threshold")
    dlgLabelsOrdered.append('staircaseTrials')
    pctCompletedBreak = 101
else:
    
    myDlg.addField('\tPercent noise dots=',  defaultNoiseLevel, tip=str(defaultNoiseLevel))
    dlgLabelsOrdered.append('defaultNoiseLevel')
    myDlg.addField('firstCondition (0 = Letters, 1 = Words):', firstCondition, tip=str(firstCondition))
    dlgLabelsOrdered.append('firstCondition')
    myDlg.addField('Trials per condition (default=' + str(trialsPerCondition) + '):', trialsPerCondition, tip=str(trialsPerCondition))
    dlgLabelsOrdered.append('trialsPerCondition')
    pctCompletedBreak = 50
    
myDlg.addText(refreshMsg1, color='Black')
if refreshRateWrong:
    myDlg.addText(refreshMsg2, color='Red')
if refreshRateWrong:
    logging.error(refreshMsg1+refreshMsg2)
else: logging.info(refreshMsg1+refreshMsg2)

if checkRefreshEtc and (not demo) and (myWinRes != [widthPix,heightPix]).any():
    msgWrongResolution = 'Screen apparently NOT the desired resolution of '+ str(widthPix)+'x'+str(heightPix)+ ' pixels!!'
    myDlg.addText(msgWrongResolution, color='Red')
    logging.error(msgWrongResolution)
    print(msgWrongResolution)
myDlg.addText('Note: to abort press ESC at a trials response screen', color='DimGrey') # [-1.,1.,-1.]) # color='DimGrey') color names stopped working along the way, for unknown reason
myDlg.show()

if myDlg.OK: #unpack information entered in dialogue box
   thisInfo = myDlg.data #this will be a list of data returned from each field added in order
   if not autopilot:
       name=thisInfo[dlgLabelsOrdered.index('subject')]
       if len(name) > 0: #if entered something
         subject = name #change subject default name to what user entered
   if doStaircase:
       if len(thisInfo[dlgLabelsOrdered.index('staircaseTrials')]) >0:
           staircaseTrials = int( thisInfo[ dlgLabelsOrdered.index('staircaseTrials') ] ) #convert string to integer
           print('staircaseTrials entered by user=',staircaseTrials)
           logging.info('staircaseTrials entered by user=',staircaseTrials)
       if len(thisInfo[dlgLabelsOrdered.index('easyTrials')]) >0:
           prefaceStaircaseTrialsN = int( thisInfo[ dlgLabelsOrdered.index('easyTrials') ] ) #convert string to integer
           print('prefaceStaircaseTrialsN entered by user=',thisInfo[dlgLabelsOrdered.index('easyTrials')])
           logging.info('prefaceStaircaseTrialsN entered by user=',prefaceStaircaseTrialsN)
   else: #not doing staircase
       trialsPerCondition = int( thisInfo[ dlgLabelsOrdered.index('trialsPerCondition') ] ) #convert string to integer
       print('trialsPerCondition=',trialsPerCondition)
       logging.info('trialsPerCondition =',trialsPerCondition)
       defaultNoiseLevel = int (thisInfo[ dlgLabelsOrdered.index('defaultNoiseLevel') ])
       firstCondition = int(thisInfo[ dlgLabelsOrdered.index('firstCondition') ])
else: 
   print('User cancelled from dialog box.')
   logging.flush()
   core.quit()
if not demo: 
    allowGUI = False

myWin = openMyStimWindow() #reopen stim window. Had to close test window to allow for dialogue boxes
#set up output data file, log file, copy of program code, and logging
infix = '' #part of the filenames
if doStaircase:
    infix = 'staircase_'
fileName = os.path.join(dataDir, subject + '_' + infix+ timeAndDateStr)
if not demo and not exportImages:
    dataFile = open(fileName+'.txt', 'w')
    saveCodeCmd = 'cp \'' + sys.argv[0] + '\' '+ fileName + '.py'
    os.system(saveCodeCmd)  #save a copy of the code as it was when that subject was run
    logFname = fileName+'.log'
    ppLogF = logging.LogFile(logFname, 
        filemode='w',#if you set this to 'a' it will append instead of overwriting
        level=logging.INFO)#errors, data and warnings will be sent to this logfile
if demo or exportImages: 
  dataFile = sys.stdout; logF = sys.stdout
  logging.console.setLevel(logging.ERROR)  #only show this level  messages and higher
logging.console.setLevel(logging.ERROR) #DEBUG means set  console to receive nearly all messges, INFO next level, EXP, DATA, WARNING and ERROR 

if fullscr and not demo and not exportImages:
    runInfo = psychopy.info.RunTimeInfo(
        # if you specify author and version here, it overrides the automatic detection of __author__ and __version__ in your script
        #author='<your name goes here, plus whatever you like, e.g., your lab or contact info>',
        #version="<your experiment version info>",
        win=myWin,    ## a psychopy.visual.Window() instance; None = default temp window used; False = no win, no win.flips()
        refreshTest='grating', ## None, True, or 'grating' (eye-candy to avoid a blank screen)
        verbose=False, ## True means report on everything 
        userProcsDetailed=True,  ## if verbose and userProcsDetailed, return (command, process-ID) of the user's processes
        #randomSeed='set:42', ## a way to record, and optionally set, a random seed of type str for making reproducible random sequences
            ## None -> default 
            ## 'time' will use experimentRuntime.epoch as the value for the seed, different value each time the script is run
            ##'set:time' --> seed value is set to experimentRuntime.epoch, and initialized: random.seed(info['randomSeed'])
            ##'set:42' --> set & initialize to str('42'), and will give the same sequence of random.random() for all runs of the script
        )
    logging.info(runInfo)
logging.flush()


if eyetracking:
    eyeMoveFile=('EyeTrack_'+subject+'_'+timeAndDateStr+'.EDF')
    tracker=Tracker_EyeLink(myWin,trialClock,subject,1, 'HV5',(255,255,255),(0,0,0),False,(widthPix,heightPix))

if firstCondition==1:
    secondCondition=0
else: secondCondition=1

textStimuliStream1 = list()
textStimuliStream2 = list() #used for second, simultaneous RSVP stream
def calcAndPredrawStimuli(wordList1,wordList2,cues,thisTrial): #Called before each trial 
    #textStimuliStream1 and 2 assumed to be global variables
    
    if len(wordList1) < numWordsInStream:
        print('Error! Your word list must have at least ',numWordsInStream,'strings')
    idxsIntoWordList = np.arange( len(wordList1) ) #create a list of indexes of the entire word list: 0,1,2,3,4,5,...23
    print('wordList1=',wordList1)
    print('wordList2=',wordList2)
    textStimuliStream1[:] = [] #Delete all items in the list
    textStimuliStream2[:] = [] #Delete all items in the list
    for i in xrange( len(cues) ):
        eccentricity = thisTrial['wordEccentricity']
        if eccentricity < 2:  #kludge to deal with very low separation case where want just one cue - draw them both in the same place
            eccentricity = 0
        if i==0: cues[i].setPos( [cos(radians(AngleToStim))*eccentricity*thisTrial['hemifield'], sin(radians(AngleToStim))*eccentricity] )
        else:  cues[i].setPos( [cos(radians(AngleToStim))*eccentricity*thisTrial['hemifield'], sin(radians(AngleToStim))*-eccentricity])
    for i in range(0,len(wordList1)): #draw all the words. Later, the seq will indicate which one to present on each frame. The seq might be shorter than the wordList
       word1 = wordList1[ i ]
       word2 = wordList2[ i ]
       #flipHoriz, flipVert  textStim http://www.psychopy.org/api/visual/textstim.html
       #Create one bucket of words for the left stream
       textStimulusStream1 = visual.TextStim(myWin,text=word1,font='Arial',height=ltrHeight,colorSpace='rgb',color=letterColor,alignHoriz='center',alignVert='center',units='deg',autoLog=autoLogging) 
       print('font',textStimulusStream1.font)
       #Create a bucket of words for the right stream
       textStimulusStream2 = visual.TextStim(myWin,text=word2,height=ltrHeight,colorSpace='rgb',color=letterColor,alignHoriz='center',alignVert='center',units='deg',autoLog=autoLogging)
       textStimulusStream1.setPos([cos(radians(AngleToStim))*thisTrial['wordEccentricity']*thisTrial['hemifield'],sin(radians(AngleToStim))*-thisTrial['wordEccentricity']])#down
       textStimuliStream1.append(textStimulusStream1) #add to list of text stimuli that comprise  stream 1
       textStimulusStream2.setPos([cos(radians(AngleToStim))*thisTrial['wordEccentricity']*thisTrial['hemifield'],sin(radians(AngleToStim))*thisTrial['wordEccentricity']]) #up
       textStimuliStream2.append(textStimulusStream2)  #add to list of text stimuli that comprise stream 2
       #If you are Joel or someone else who needs to mess with the stream conditional on the cue position, this is probably where we are going to do it
       #pseudoHomophonePos = thisTrial['cuePos'] -1
       
    #Use these buckets by pulling out the drawn words in the order you want them. For now, just create the order you want.
    np.random.shuffle(idxsIntoWordList) #0,1,2,3,4,5,... -> randomly permuted 3,2,5,...
    idxsStream1 = copy.deepcopy(idxsIntoWordList) #first RSVP stream
    idxsStream1= idxsStream1[:numWordsInStream] #take the first numWordsInStream of the shuffled list
    idxsStream2 = copy.deepcopy(idxsIntoWordList)  #make a copy for the right stream, and permute them on the next list
    np.random.shuffle(idxsStream2)
    idxsStream2= idxsStream2[:numWordsInStream]  #take the first numWordsInStream of the shuffled list
    return idxsStream1, idxsStream2, cues
    
#create click sound for keyboard
try:
    click=sound.Sound('406__tictacshutup__click-1-d.wav')
except: #in case file missing, create inferiro click manually
    logging.warn('Could not load the desired click sound file, instead using manually created inferior click')
    click=sound.Sound('D',octave=4, sampleRate=22050, secs=0.015, bits=8)

if showRefreshMisses:
    fixSizePix = 32 #2.6  #make fixation bigger so flicker more conspicuous
else: fixSizePix = 32
fixColor = [1,1,1]
if exportImages: fixColor= [0,0,0]
fixatnNoiseTexture = np.round( np.random.rand(fixSizePix/4,fixSizePix/4) ,0 )   *2.0-1 #Can counterphase flicker  noise texture to create salient flicker if you break fixation

#Construct the fixation point.
fixation= visual.PatchStim(myWin, tex=fixatnNoiseTexture, size=(fixSizePix,fixSizePix), units='pix', mask='circle', interpolate=False, autoLog=False)
fixationBlank= visual.PatchStim(myWin, tex= -1*fixatnNoiseTexture, size=(fixSizePix,fixSizePix), units='pix', mask='circle', interpolate=False, autoLog=False) #reverse contrast
fixationPoint= visual.PatchStim(myWin,tex='none',colorSpace='rgb',color=(1,1,1),size=4,units='pix',autoLog=autoLogging)
#Construct the holders for the experiment text that will appear on screen
respPromptStim = visual.TextStim(myWin,pos=(0, -.9),colorSpace='rgb',color=(1,1,1),alignHoriz='center', alignVert='center',height=.1,units='norm',autoLog=autoLogging)
acceptTextStim = visual.TextStim(myWin,pos=(0, -.8),colorSpace='rgb',color=(1,1,1),alignHoriz='center', alignVert='center',height=.1,units='norm',autoLog=autoLogging)
acceptTextStim.setText('Say your response. Press Enter to continue')
respStim = visual.TextStim(myWin,pos=(0,0),colorSpace='rgb',color=(1,1,0),alignHoriz='center', alignVert='center',height=3,units='deg',autoLog=autoLogging)
requireAcceptance = True #previously this was FALSE.  NOT SURE WHY.
nextText = visual.TextStim(myWin,pos=(0, .1),colorSpace='rgb',color = (1,1,1),alignHoriz='center', alignVert='center',height=.1,units='norm',autoLog=autoLogging)
NextRemindCountText = visual.TextStim(myWin,pos=(0,.2),colorSpace='rgb',color= (1,1,1),alignHoriz='center', alignVert='center',height=.1,units='norm',autoLog=autoLogging)

clickSound, badKeySound = stringResponseKRedit.setupSoundsForResponse()

screenshot= False; screenshotDone = False


if limitedTest:
    stimList = []
    #SETTING THE CONDITIONS, This implements the full factorial design!
    for upResponseFirst in [False,True]:
      for wordEcc in [5]:
        for bin in [Sample6]: #Different samples of words taken from database to vary word frequency range
            for hemifield in [-1,1]:#-1 = Left
                    stimList.append( {'upResponseFirst':upResponseFirst,
                                            'leftStreamFlip':False, 'rightStreamFlip':False,
                                         'wordEccentricity':wordEcc, 'bin':bin ,'hemifield':hemifield} )

    trials = data.TrialHandler(stimList,trialsPerCondition) #constant stimuli method
    trialsForPossibleStaircase = data.TrialHandler(stimList,trialsPerCondition) #independent randomization, just to create random trials for staircase phase
    block2trials = data.TrialHandler(stimList,trialsPerCondition)

else:
    stimList = []
    #SETTING THE CONDITIONS, This implements the full factorial design!
    for upResponseFirst in [False,True]:
      for wordEcc in [5]:
        for bin in [Sample1,Sample2,Sample3,Sample4,Sample5,Sample6]: #Different samples of words taken from database to vary word frequency range
            for hemifield in [-1,1]:
                stimList.append( {'upResponseFirst':upResponseFirst,
                                        'leftStreamFlip':False, 'rightStreamFlip':False,
                                         'wordEccentricity':wordEcc, 'bin':bin, 'hemifield':hemifield } )

    trials = data.TrialHandler(stimList,trialsPerCondition) #constant stimuli method
    trialsForPossibleStaircase = data.TrialHandler(stimList,trialsPerCondition) #independent randomization, just to create random trials for staircase phase
    block2trials = data.TrialHandler(stimList,trialsPerCondition)

stimListPrac = []
#SETTING THE CONDITIONS FOR PRAC TRIALS,
for upResponseFirst in [False,True]:
  for wordEcc in [5]:
    for bin in [PracSample1]: #Different samples of words taken from database to vary word frequency range
        for hemifield in [-1,1]:
            stimListPrac.append( {'upResponseFirst':upResponseFirst,
                                    'leftStreamFlip':False, 'rightStreamFlip':False,
                                     'wordEccentricity':wordEcc, 'bin':bin ,'hemifield':hemifield} )


pracTrials = data.TrialHandler(stimListPrac,1) #constant stimuli method
block2pracTrials = data.TrialHandler(stimListPrac,1)

cueSerialPositions = np.array([5,6,7,8,9,10,11,12])
numRightWrongEachCuepos = np.zeros([ len(cueSerialPositions), 1 ]); #summary results to print out at end

logging.info( 'numtrials=' + str(trials.nTotal) + ' and each trialDurFrames='+str(trialDurFrames)+' or '+str(trialDurFrames*(1000./refreshRate))+ \
               ' ms' + '  task=' + task)

 #  np.array([10,11,12,13,14])  ## Previously in trialHandler
#cueSerialPos in cueSerialPositions:

def numberToLetter(number): #0 = A, 25 = Z
    #if it's not really a letter, return @
    if number < 0 or number > 25:
        return ('@')
    else: #it's probably a letter
        try:
            return chr( ord('A')+number )
        except:
            return('@')

def letterToNumber(letter): #A = 0, Z = 25
    #if it's not really a letter, return -999
    #HOW CAN I GENERICALLY TEST FOR LENGTH. EVEN IN CASE OF A NUMBER THAT'S NOT PART OF AN ARRAY?
    try:
        #if len(letter) > 1:
        #    return (-999)
        if letter < 'A' or letter > 'Z':
            return (-999)
        else: #it's a letter
            return ord(letter)-ord('A')
    except:
        return (-999)

def wordToIdx(word,wordList):
    #if it's not in the list of stimuli, return -999
    try:
        #http://stackoverflow.com/questions/7102050/how-can-i-get-a-python-generator-to-return-none-rather-than-stopiteration
        firstMatchIdx = next((i for i, val in enumerate(wordList) if val.upper()==word), None) #return i (index) unless no matches, in which case return None
        #print('Looked for ',word,' in ',wordList,'\nfirstMatchIdx =',firstMatchIdx)
        return firstMatchIdx
                #http://stackoverflow.com/questions/7102050/how-can-i-get-a-python-generator-to-return-none-rather-than-stopiteration
       # secondMatchIdx = next((i for i, val in enumerate(wordList) if val.upper()==word), None) #return i (index) unless no matches, in which case return None
        #print('Looked for ',word,' in ',wordList,'\nfirstMatchIdx =',firstMatchIdx)
       # return secondMatchIdx
    except:
        print('Unexpected error in wordToIdx with word=',word)
        return (None)
        
#print header for data file
print('experimentPhase\tblock\tcondition\ttrialnum\tsubject\ttask\t',file=dataFile,end='')
print('noisePercent\themifield\tleftStreamFlip\trightStreamFlip\t',end='',file=dataFile)
if task=='T1':
    numRespsWanted = 2
dataFile.write('upResponseFirst\t')
for i in range(numRespsWanted):
   dataFile.write('cueSerialPos'+str(i)+'\t')   #have to use write to avoid ' ' between successive text, at least until Python 3
   dataFile.write('answer'+str(i)+'\t')
   #dataFile.write('response'+str(i)+'\t')
   #dataFile.write('correct'+str(i)+'\t')
   #dataFile.write('responsePosRelative'+str(i)+'\t')
for i in range(numWordsInStream):
    dataFile.write('word1_'+str(i)+'\t')
for i in range(numWordsInStream):
    dataFile.write('Seq1_'+str(i)+'\t')
for i in range(numWordsInStream):
    dataFile.write('word2_'+str(i)+'\t')
for i in range(numWordsInStream):
    dataFile.write('Seq2_'+str(i)+'\t')
print('timingBlips',file=dataFile)
#end of header

def  oneFrameOfStim( n,cues,cuesSerialPos,seq1,seq2,cueDurFrames,letterDurFrames,ISIframes,thisTrial,textStimuliStream1,textStimuliStream2,
                                       noise,proportnNoise,allFieldCoords,numNoiseDots ): 
#defining a function to draw each frame of stim.
#seq1 is an array of indices corresponding to the appropriate pre-drawn stimulus, contained in textStimuli
  SOAframes = letterDurFrames+ISIframes
  cueFrames = cuesSerialPos*SOAframes
  stimN = int( np.floor(n/SOAframes) )
  frameOfThisLetter = n % SOAframes #every SOAframes, new letter
  showLetter = frameOfThisLetter < letterDurFrames #if true, it's not time for the blank ISI.  it's still time to draw the letter
  #print 'n=',n,' SOAframes=',SOAframes, ' letterDurFrames=', letterDurFrames, ' (n % SOAframes) =', (n % SOAframes)  #DEBUGOFF
  thisStimIdx = seq1[stimN] #which letter, from A to Z (1 to 26), should be shown?
  #print ('stimN=',stimN, 'thisStimIdx=', thisStimIdx, ' SOAframes=',SOAframes, ' letterDurFrames=', letterDurFrames, ' (n % SOAframes) =', (n % SOAframes) ) #DEBUGOFF
  if seq2 is not None:
    thisStim2Idx = seq2[stimN]
  #so that any timing problems occur just as often for every frame, always draw the letter and the cue, but simply draw it in the bgColor when it's not meant to be on
  for cue in cues:
    cue.setLineColor( bgColor )
  if type(cueFrames) not in [tuple,list,np.ndarray]: #scalar. But need collection to do loop based on it
    cueFrames = list([cueFrames])
  for i in xrange( len(cueFrames) ): #check whether it's time for any cue. Assume first cueFrame is for first cue, etc.
    thisCueFrame = cueFrames[i]
    if n>=thisCueFrame and n<thisCueFrame+cueDurFrames:
         cues[i].setLineColor( cueColor )

  if showLetter:
    textStimuliStream1[thisStimIdx].setColor( letterColor )
    textStimuliStream2[thisStim2Idx].setColor( letterColor )
  else: 
    textStimuliStream1[thisStimIdx].setColor( bgColor )
    textStimuliStream2[thisStim2Idx].setColor( bgColor )
  textStimuliStream1[thisStimIdx].flipHoriz = thisTrial['leftStreamFlip']
  textStimuliStream2[thisStim2Idx].flipHoriz = thisTrial['rightStreamFlip']
  textStimuliStream1[thisStimIdx].draw()
  textStimuliStream2[thisStim2Idx].draw()
  for cue in cues:
    cue.draw() #will be drawn in backgruond color if it's not time for that
  refreshNoise = False #Not recommended because takes longer than a frame, even to shuffle apparently. Or may be setXYs step
  if proportnNoise>0 and refreshNoise: 
    if frameOfThisLetter ==0: 
        np.random.shuffle(allFieldCoords) 
        dotCoords = allFieldCoords[0:numNoiseDots]
        noise.setXYs(dotCoords)
  if proportnNoise>0:
    noise.draw()
  return True 
# #######End of function definition that displays the stimuli!!!! #####################################
#############################################################################################################################
cues = list()
for i in xrange(2):
    cue = visual.Circle(myWin, 
                     radius=cueRadius,#Martini used circles with diameter of 12 deg
                     lineColorSpace = 'rgb',
                     lineColor=bgColor,
                     lineWidth=4.0, #in pixels. Was thinner (2 pixels) in letter AB experiments
                     units = 'deg',
                     fillColorSpace = 'rgb',
                     fillColor=None, #beware, with convex shapes fill colors don't work
                     pos= [0,0], #the anchor (rotation and vertices are position with respect to this)
                     interpolate=True,
                     autoLog=False)#this stim changes too much for autologging to be useful
    cues.append(cue)
    
#Precue to potentially inform the participant where the letter streams will appear
preCue1 = visual.Circle(myWin,  
                 radius=cueRadius,#Martini used circles with diameter of 12 deg
                 lineColorSpace = 'rgb',
                 lineColor='white',
                 lineWidth=4.0, #in pixels. Was thinner (2 pixels) in letter AB experiments
                 units = 'deg',
                 fillColorSpace = 'rgb',
                 fillColor= None, #beware, with convex shapes fill colors don't work
                 #pos= [wordEcc*thisTrial['hemifield',-wordEcc]], #the anchor (rotation and vertices are position with respect to this)
                 interpolate=True,
                 autoLog=False)#this stim changes too much for autologging to be useful

preCue2 = visual.Circle(myWin,  
                 radius=cueRadius,#Martini used circles with diameter of 12 deg
                 lineColorSpace = 'rgb',
                 lineColor='white',
                 lineWidth=4.0, #in pixels. Was thinner (2 pixels) in letter AB experiments
                 units = 'deg',
                 fillColorSpace = 'rgb',
                 fillColor= None, #beware, with convex shapes fill colors don't work
                 #pos= [wordEcc*thisTrial['hemifield',wordEcc]], #the anchor (rotation and vertices are position with respect to this)
                 interpolate=True,
                 autoLog=False)#this stim changes too much for autologging to be useful

ltrHeight = 2  #changed to accomodate 4 letter words #2.5 #Martini letters were 2.5deg high
#All noise dot coordinates ultimately in pixels, so can specify each dot is one pixel 
noiseFieldWidthDeg=ltrHeight *1.0
noiseFieldWidthPix = int( round( noiseFieldWidthDeg*pixelperdegree ) )

def timingCheckAndLog(ts,trialN):
    #check for timing problems and log them
    #ts is a list of the times of the clock after each frame
    interframeIntervs = np.diff(ts)*1000
    #print '   interframe intervs were ',around(interframeIntervs,1) #DEBUGOFF
    frameTimeTolerance=.3 #proportion longer than refreshRate that will not count as a miss
    longFrameLimit = np.round(1000/refreshRate*(1.0+frameTimeTolerance),2)
    idxsInterframeLong = np.where( interframeIntervs > longFrameLimit ) [0] #frames that exceeded 150% of expected duration
    numCasesInterframeLong = len( idxsInterframeLong )
    if numCasesInterframeLong >0 and (not demo):
       longFramesStr =  'ERROR,'+str(numCasesInterframeLong)+' frames were longer than '+str(longFrameLimit)+' ms'
       if demo: 
         longFramesStr += 'not printing them all because in demo mode'
       else:
           longFramesStr += ' apparently screen refreshes skipped, interframe durs were:'+\
                    str( np.around(  interframeIntervs[idxsInterframeLong] ,1  ) )+ ' and was these frames: '+ str(idxsInterframeLong)
       if longFramesStr != None:
                logging.error( 'trialnum='+str(trialN)+' '+longFramesStr )
                if not demo:
                    flankingAlso=list()
                    for idx in idxsInterframeLong: #also print timing of one before and one after long frame
                        if idx-1>=0:
                            flankingAlso.append(idx-1)
                        else: flankingAlso.append(np.NaN)
                        flankingAlso.append(idx)
                        if idx+1<len(interframeIntervs):  flankingAlso.append(idx+1)
                        else: flankingAlso.append(np.NaN)
                    flankingAlso = np.array(flankingAlso)
                    flankingAlso = flankingAlso[np.negative(np.isnan(flankingAlso))]  #remove nan values
                    flankingAlso = flankingAlso.astype(np.integer) #cast as integers, so can use as subscripts
                    logging.info( 'flankers also='+str( np.around( interframeIntervs[flankingAlso], 1) )  ) #because this is not an essential error message, as previous one already indicates error
                      #As INFO, at least it won't fill up the console when console set to WARNING or higher
    return numCasesInterframeLong
    #end timing check
    
trialClock = core.Clock()
numTrialsCorrect = 0; 
numTrialsApproxCorrect = 0;
numTrialsEachCorrect= np.zeros( numRespsWanted )
numTrialsEachApproxCorrect= np.zeros( numRespsWanted )

def do_RSVP_stim(thisTrial, cues, seq1, seq2, proportnNoise,trialN,eyeTrackthisTrial):
    #relies on global variables:
    #   textStimuli, logging, bgColor
    #  thisTrial should have 'cueSerialPos'
    global framesSaved #because change this variable. Can only change a global variable if you declare it
    cuesSerialPos = [] #will contain the serial positions in the stream of all the cues (corresponding to the targets)
    cueSerialPositions = np.array([5,6,7,8,9,10,11,12])
    random.shuffle(cueSerialPositions)
    cuesSerialPos.append(cueSerialPositions[0]) #stream1
    cuesSerialPos.append(cueSerialPositions[0]) #stream2
    #cuesSerialPos.append(thisTrial['cueSerialPos']) #stream1
    #cuesSerialPos.append(thisTrial['cueSerialPos']) #stream2
    cuesSerialPos = np.array(cuesSerialPos)
    noise = None; allFieldCoords=None; numNoiseDots=0
    if proportnNoise > 0: #gtenerating noise is time-consuming, so only do it once per trial. Then shuffle noise coordinates for each letter
        (noise,allFieldCoords,numNoiseDots) = createNoise(proportnNoise,myWin,noiseFieldWidthPix, bgColor)

    preDrawStimToGreasePipeline = list() #I don't know why this works, but without drawing it I have consistent timing blip first time that draw ringInnerR for phantom contours
    for cue in cues:
        cue.setLineColor(bgColor)
        preDrawStimToGreasePipeline.extend([cue])
    for stim in preDrawStimToGreasePipeline:
        stim.draw()
    myWin.flip(); myWin.flip()
    #end preparation of stimuli
    if eyeTrackthisTrial: 
        tracker.startEyeTracking(trialN,calibTrial=True,widthPix=widthPix,heightPix=heightPix) # tell eyetracker to start recording. Does this also somehow allow it to draw on the screen for the calibration?

    core.wait(.1);
    trialClock.reset()
    fixatnPeriodMin = 0.3
    fixatnPeriodFrames = int(   (np.random.rand(1)/2.+fixatnPeriodMin)   *refreshRate)  #random interval between 800ms and 1.3s
    ts = list(); #to store time of each drawing, to check whether skipped frames
    preCue1.setPos([cos(radians(AngleToStim))*wordEcc*thisTrial['hemifield'],sin(radians(AngleToStim))*wordEcc])
    preCue2.setPos([cos(radians(AngleToStim))*wordEcc*thisTrial['hemifield'],sin(radians(AngleToStim))*-wordEcc])
    preCueMin = 0.5
    preCueFrames = int(preCueMin*refreshRate)
    play_high_tone_correct_low_incorrect(correct=True, passThisTrial=False)
    for i in range(preCueFrames):
        fixationPoint.draw()
        preCue1.draw()
        preCue2.draw()
        
        myWin.flip()
    
    for i in range(fixatnPeriodFrames+20):  #prestim fixation interval
        #if i%4>=2 or demo or exportImages: #flicker fixation on and off at framerate to see when skip frame
        #      fixation.draw()
        #else: fixationBlank.draw()
        fixationPoint.draw()
        myWin.flip()  #end fixation interval
    #myWin.setRecordFrameIntervals(True);  #can't get it to stop detecting superlong frames
    t0 = trialClock.getTime()
    

    for n in range(trialDurFrames): #this is the loop for this trial's stimulus!
        worked = oneFrameOfStim( n,cues,cuesSerialPos,seq1,seq2,cueDurFrames,letterDurFrames,ISIframes,thisTrial,textStimuliStream1,textStimuliStream2,
                                                     noise,proportnNoise,allFieldCoords,numNoiseDots ) #draw letter and possibly cue and noise on top
        if thisTrial['wordEccentricity'] > 2:  #kludge to avoid drawing fixation in super-near condition for Cheryl
            fixationPoint.draw()
        if exportImages:
            myWin.getMovieFrame(buffer='back') #for later saving
            framesSaved +=1
        myWin.flip()
        t=trialClock.getTime()-t0;  ts.append(t);
        if eyeTrackthisTrial:
            tracker.stopEyeTracking() #This seems to work immediately and cause the Eyelink machine to save the EDF file to its own drive
    #end of big stimulus loop
    myWin.setRecordFrameIntervals(False);

    if task=='T1':
        respPromptStim.setText('What was circled?',log=False)   
    else: respPromptStim.setText('Error: unexpected task',log=False)
    postCueNumBlobsAway=-999 #doesn't apply to non-tracking and click tracking task
    correctAnswerIdxsStream1 = np.array( seq1[cuesSerialPos] )
    correctAnswerIdxsStream2 = np.array( seq2[cuesSerialPos] )
    #print('correctAnswerIdxsStream1=',correctAnswerIdxsStream1, 'wordList[correctAnswerIdxsStream1[0]]=',wordList[correctAnswerIdxsStream1[0]])
    return cuesSerialPos,correctAnswerIdxsStream1,correctAnswerIdxsStream2,ts
    
def handleAndScoreResponse(passThisTrial,response,responseAutopilot,task,stimSequence,cueSerialPos,correctAnswerIdx,wordList):
    #Handle response, calculate whether correct, ########################################
    #responses are actual characters
    #correctAnswer is index into stimSequence
    #autopilot is global variable
    if autopilot or passThisTrial:
        response = responseAutopilot
    #print('handleAndScoreResponse correctAnswerIdxs=',correctAnswerIdxs,'\nstimSequence=',stimSequence, '\nwords=',wordList)
    correct = 0
    approxCorrect = 0
    posOfResponse = -999
    responsePosRelative = -999
    idx = correctAnswerIdx
    print('correctAnswerIdx = ',correctAnswerIdx) 
    print('wordlist = ', wordList)
    correctAnswer = wordList[idx].upper()
    #responseString= 'NULL'
    #responseString= responseString.upper()
    #print('correctAnswer=',correctAnswer ,' responseString=',responseString)
    #if correctAnswer == responseString:
    #    correct = 1
    #print('correct=',correct)
    #responseWordIdx = wordToIdx(responseString,wordList)
    #print('responseWordIdx = ', responseWordIdx, ' stimSequence=', stimSequence)
    #if responseWordIdx is None: #response is not in the wordList
    #    posOfResponse = -999
    #    logging.warn('Response was not present in the stimulus stream')
    #else:
    #    posOfResponse= np.where( responseWordIdx==stimSequence )
    #    posOfResponse= posOfResponse[0] #list with two entries, want first which will be array of places where the response was found in the sequence
    #    if len(posOfResponse) > 1:
    #        logging.error('Expected response to have occurred in only one position in stream')
    #    elif len(posOfResponse) == 0:
    #        logging.error('Expected response to have occurred somewhere in the stream')
    #        raise ValueError('Expected response to have occurred somewhere in the stream')
     #   else:
    #        posOfResponse = posOfResponse[0] #first element of list (should be only one element long 
    #    responsePosRelative = posOfResponse - cueSerialPos
    #    approxCorrect = abs(responsePosRelative)<= 3 #Vul efficacy measure of getting it right to within plus/minus
    #print('wordToIdx(',responseString,',',wordList,')=',responseWordIdx,' stimSequence=',stimSequence,'\nposOfResponse = ',posOfResponse) #debugON
    #print response stuff to dataFile
    #header was answerPos0, answer0, response0, correct0, responsePosRelative0
    print(cueSerialPos,'\t', end='', file=dataFile)
    print(correctAnswer, '\t', end='', file=dataFile) #answer0
    #print(responseString, '\t', end='', file=dataFile) #response0
    #print(correct, '\t', end='',file=dataFile)   #correct0
    #print(responsePosRelative, '\t', end='',file=dataFile) #responsePosRelative0

    return correct,approxCorrect,responsePosRelative
    #end handleAndScoreResponses

def play_high_tone_correct_low_incorrect(correct, passThisTrial=False):
    highA = sound.Sound('G',octave=5, sampleRate=6000, secs=.5, bits=8)
    low = sound.Sound('F',octave=3, sampleRate=6000, secs=.5, bits=8)
    highA.setVolume(0.8)
    low.setVolume(1.0)

    high= sound.Sound('G',octave=5, sampleRate=6000, secs=0.08, bits=8)
    high.setVolume(0.8)
    for i in range(20): 
        high.play(); 
        


expStop=False
nDoneMain = -1 #change to zero once start main part of experiment
if doStaircase:
    #create the staircase handler
    useQuest = True
    if  useQuest:
        staircase = data.QuestHandler(startVal = 95, 
                              startValSd = 80,
                              stopInterval= 1, #sd of posterior has to be this small or smaller for staircase to stop, unless nTrials reached
                              nTrials = staircaseTrials,
                              #extraInfo = thisInfo,
                              pThreshold = threshCriterion, #0.25,    
                              gamma = 1./26,
                              delta=0.02, #lapse rate, I suppose for Weibull function fit
                              method = 'quantile', #uses the median of the posterior as the final answer
                              stepType = 'log',  #will home in on the 80% threshold. But stepType = 'log' doesn't usually work
                              minVal=1, maxVal = 100
                              )
        print('created QUEST staircase')
    else:
        stepSizesLinear = [.2,.2,.1,.1,.05,.05]
        stepSizesLog = [log(1.4,10),log(1.4,10),log(1.3,10),log(1.3,10),log(1.2,10)]
        staircase = data.StairHandler(startVal = 0.1,
                                  stepType = 'log', #if log, what do I want to multiply it by
                                  stepSizes = stepSizesLog,    #step size to use after each reversal
                                  minVal=0, maxVal=1,
                                  nUp=1, nDown=3,  #will home in on the 80% threshold
                                  nReversals = 2, #The staircase terminates when nTrials have been exceeded, or when both nReversals and nTrials have been exceeded
                                  nTrials=1)
        print('created conventional staircase')
        
    if prefaceStaircaseTrialsN > len(prefaceStaircaseNoise): #repeat array to accommodate desired number of easyStarterTrials
        prefaceStaircaseNoise = np.tile( prefaceStaircaseNoise, ceil( prefaceStaircaseTrialsN/len(prefaceStaircaseNoise) ) )
    prefaceStaircaseNoise = prefaceStaircaseNoise[0:prefaceStaircaseTrialsN]
    
    phasesMsg = ('Doing '+str(prefaceStaircaseTrialsN)+'trials with noisePercent= '+str(prefaceStaircaseNoise)+' then doing a max '+str(staircaseTrials)+'-trial staircase')
    print(phasesMsg); logging.info(phasesMsg)

    #staircaseStarterNoise PHASE OF EXPERIMENT
    corrEachTrial = list() #only needed for easyStaircaseStarterNoise
    staircaseTrialN = -1; mainStaircaseGoing = False
    while (not staircase.finished) and expStop==False: #staircase.thisTrialN < staircase.nTrials
        if staircaseTrialN+1 < len(prefaceStaircaseNoise): #still doing easyStaircaseStarterNoise
            staircaseTrialN += 1
            noisePercent = prefaceStaircaseNoise[staircaseTrialN]
        else:
            if staircaseTrialN+1 == len(prefaceStaircaseNoise): #add these non-staircase trials so QUEST knows about them
                mainStaircaseGoing = True
                print('Importing ',corrEachTrial,' and intensities ',prefaceStaircaseNoise)
                staircase.importData(100-prefaceStaircaseNoise, np.array(corrEachTrial))
                printStaircase(staircase, descendingPsycho, briefTrialUpdate=False, printInternalVal=True, alsoLog=False)
            try: #advance the staircase
                printStaircase(staircase, descendingPsycho, briefTrialUpdate=True, printInternalVal=True, alsoLog=False)
                noisePercent = 100. - staircase.next()  #will step through the staircase, based on whether told it (addResponse) got it right or wrong
                staircaseTrialN += 1
            except StopIteration: #Need this here, even though test for finished above. I can't understand why finished test doesn't accomplish this.
                print('stopping because staircase.next() returned a StopIteration, which it does when it is finished')
                break #break out of the trials loop
        #print('staircaseTrialN=',staircaseTrialN)
        idxsStream1, idxsStream2, cues = calcAndPredrawStimuli(wordList,cues,staircaseTrials)
        cuesSerialPos,correctAnswerIdxsStream1,correctAnswerIdxsStream2, ts  = \
                                        do_RSVP_stim(thisTrial, cues, idxsStream1, idxsStream2, noisePercent/100.,staircaseTrialN)
        numCasesInterframeLong = timingCheckAndLog(ts,staircaseTrialN)
        expStop,passThisTrial,responses,responsesAutopilot = \
                stringResponseKRedit.collectStringResponse(numRespsWanted,respPromptStim,respStim,acceptTextStim,myWin,clickSound,badKeySound,
                                                                               requireAcceptance,autopilot,responseDebug=True)



        if not expStop:
            if mainStaircaseGoing:
                print('staircase\t', end='', file=dataFile)
            else: 
                print('staircase_preface\t', end='', file=dataFile)
             #header start      'trialnum\tsubject\ttask\t'
            print(staircaseTrialN,'\t', end='', file=dataFile) #first thing printed on each line of dataFile
            print(subject,'\t',task,'\t', round(noisePercent,2),'\t', end='', file=dataFile)
            correct,approxCorrect,responsePosRelative= handleAndScoreResponse(
                                                passThisTrial,responses,responseAutopilot,task,g,cuesSerialPos[0],correctAnswerIdx )

            print(numCasesInterframeLong, file=dataFile) #timingBlips, last thing recorded on each line of dataFile
            core.wait(.06)
            if feedback: 
                play_high_tone_correct_low_incorrect(correct, passThisTrial=False)
            print('staircaseTrialN=', staircaseTrialN,' noisePercent=',round(noisePercent,3),' T1approxCorrect=',T1approxCorrect) #debugON
            corrEachTrial.append(T1approxCorrect)
            if mainStaircaseGoing: 
                staircase.addResponse(T1approxCorrect, intensity = 100-noisePercent) #Add a 1 or 0 to signify a correct/detected or incorrect/missed trial
                #print('Have added an intensity of','{:.3f}'.format(100-noisePercent), 'T1approxCorrect =', T1approxCorrect, ' to staircase') #debugON
    #ENDING STAIRCASE PHASE

    if staircaseTrialN+1 < len(prefaceStaircaseNoise) and (staircaseTrialN>=0): #exp stopped before got through staircase preface trials, so haven't imported yet
        print('Importing ',corrEachTrial,' and intensities ',prefaceStaircaseNoise[0:staircaseTrialN+1])
        staircase.importData(100-prefaceStaircaseNoise[0:staircaseTrialN], np.array(corrEachTrial)) 
    print('framesSaved after staircase=',framesSaved) #debugON

    timeAndDateStr = time.strftime("%H:%M on %d %b %Y", time.localtime())
    msg = ('prefaceStaircase phase' if expStop else '')
    msg += ('ABORTED' if expStop else 'Finished') + ' staircase part of experiment at ' + timeAndDateStr
    logging.info(msg); print(msg)
    printStaircase(staircase, descendingPsycho, briefTrialUpdate=True, printInternalVal=True, alsoLog=False)
    #print('staircase.quantile=',round(staircase.quantile(),2),' sd=',round(staircase.sd(),2))
    threshNoise = round(staircase.quantile(),3)
    if descendingPsycho:
        threshNoise = 100- threshNoise
    threshNoise = max( 0, threshNoise ) #e.g. ff get all trials wrong, posterior peaks at a very negative number
    msg= 'Staircase estimate of threshold = ' + str(threshNoise) + ' with sd=' + str(round(staircase.sd(),2))
    logging.info(msg); print(msg)
    myWin.close()
    #Fit and plot data
    fit = None
    try:
        intensityForCurveFitting = staircase.intensities
        if descendingPsycho: 
            intensityForCurveFitting = 100-staircase.intensities #because fitWeibull assumes curve is ascending
        fit = data.FitWeibull(intensityForCurveFitting, staircase.data, expectedMin=1/26., sems = 1.0/len(staircase.intensities))
    except:
        print("Fit failed.")
    plotDataAndPsychometricCurve(staircase,fit,descendingPsycho,threshCriterion)
    #save figure to file
    pylab.savefig(fileName+'.pdf')
    print('The plot has been saved, as '+fileName+'.pdf')
    pylab.show() #must call this to actually show plot
else: #not staircase
    block = 1
    for condition in (firstCondition,secondCondition):
        print(condition)
        print(block)
        noisePercent = defaultNoiseLevel
        phasesMsg = 'Experiment will have '+str(trials.nTotal)+' trials. Letters will be drawn with superposed noise of ' + "{:.2%}".format(defaultNoiseLevel)
        print(phasesMsg); logging.info(phasesMsg)
        nDonePrac = 0
        while nDonePrac < pracTrials.nTotal and expStop==False: #PRACTICE EXPERIMENT LOOP
            if block==1:
                if nDonePrac==0:
                    print('startingPrac')
                    instructions(condition)
                    msg='Starting practice trials'
                    logging.info(msg); print(msg)
                thisPracTrial = pracTrials.next()
            else:
                if nDonePrac==0:
                    block2instructions(condition)
                    msg='Starting practice trials'
                    logging.info(msg); print(msg)
                thisPracTrial = block2pracTrials.next()
    
            if condition==1:
                wordBin = thisPracTrial['bin']
            else:
                wordBin = SampleLetters
            np.random.shuffle(wordBin)
            
            wordList1 = wordBin[0:numWordsInStream]
            if condition==1:
                wordList2 = wordBin[numWordsInStream:numWordsInStream*2]
            else:  wordList2 = wordList1
            print('Now')
            print(wordList1)
            print(wordList2)
            sequenceStream1, sequenceStream2, cues = calcAndPredrawStimuli(wordList1,wordList2,cues,thisPracTrial)
            print('sequenceStream1=',sequenceStream1)
            print('sequenceStream2=',sequenceStream2)
            cuesSerialPos,correctAnswerIdxsStream1,correctAnswerIdxsStream2, ts  = \
                                                                        do_RSVP_stim(thisPracTrial, cues, sequenceStream1, sequenceStream2, noisePercent/100.,nDonePrac,False)
            numCasesInterframeLong = timingCheckAndLog(ts,nDonePrac)
            #call for each response
            expStop = list(); passThisTrial = list(); responses=list(); responsesAutopilot=list()
            numCharsInResponse = len(wordList1[0])
            dL = [None]*numRespsWanted #dummy list for null values
            expStop = copy.deepcopy(dL); responses = copy.deepcopy(dL); responsesAutopilot = copy.deepcopy(dL); passThisTrial=copy.deepcopy(dL)
            responseOrder = range(numRespsWanted)
            print(thisPracTrial['upResponseFirst'])
            if thisPracTrial['upResponseFirst']: #change order of indices depending on upResponseFirst. response0, answer0 etc refer to which one had to be reported first
                    responseOrder.reverse()
            print('responseOrder',responseOrder)
            for i in responseOrder:
                x = 1.5 * sin(radians(AngleToStim))*thisPracTrial['wordEccentricity']*(i*2-1) #put it 3 times farther out than stimulus, so participant is sure which is left and which right
    #            blanksNeeded = numCharsInResponse
    #            respStim = visual.TextStim(myWin,pos=(0,x),colorSpace='rgb',color=(1,1,0),alignHoriz='center', alignVert='center',height=.16,units='norm',autoLog=autoLogging)
    #            respStr = '____'
    #            respStim.setText(respStr,log=False)
    #            respStim.draw(); 
    #            myWin.flip()
    #        
    #            waitingForSpace = True
    #            while waitingForSpace:
    #                for key in event.getKeys():
    #                    key = key.upper()
    #                    if key in ['SPACE']:
    #                        waitingForSpace=False
    
                #if (numResponses == numCharsWanted) and requireAcceptance:  #ask participant to HIT ENTER TO ACCEPT
    
                print('x',x)
                
                respStim = visual.TextStim(myWin,pos=(cos(radians(AngleToStim))*thisPracTrial['wordEccentricity']*thisPracTrial['hemifield'],x),colorSpace='rgb',color=(1,1,0),alignHoriz='center', alignVert='center',height=2.5,units='deg',autoLog=autoLogging)
    
                expStop[i],passThisTrial[i],responses[i],responsesAutopilot[i] = stringResponseKRedit.collectStringResponse(
                                          numCharsInResponse,respPromptStim,respStim,acceptTextStim,myWin,clickSound,badKeySound,
                                                                                       requireAcceptance,autopilot,responseDebug=True)                                                                               
            expStop = np.array(expStop).any(); passThisTrial = np.array(passThisTrial).any()
            nDonePrac+=1
            if nDonePrac==pracTrials.nTotal:
                    
                endPrac = visual.TextStim(myWin, text = finishedPractice,pos=(0, 0),height=instrLtrHeight,colorSpace='rgb',color=instrcolor,alignHoriz='center',alignVert='center',units='deg',autoLog=autoLogging )
    
                endPrac.draw()
                myWin.flip()
                event.waitKeys()
            
        noisePercent = defaultNoiseLevel
        phasesMsg = 'Experiment will have '+str(trials.nTotal)+' trials. Letters will be drawn with superposed noise of ' + "{:.2%}".format(defaultNoiseLevel)
        print(phasesMsg); logging.info(phasesMsg)
        
        nDoneMain =0
        while nDoneMain < trials.nTotal and expStop==False: #MAIN EXPERIMENT LOOP
            if nDoneMain==0:
                msg='Starting main (non-staircase) part of experiment'
                logging.info(msg); print(msg)
            if block==1:
                thisTrial = trials.next() #get a proper (non-staircase) trial
            else:
                thisTrial = block2trials.next()
            if condition==1:
                wordBin = thisTrial['bin']
            else:
                wordBin = SampleLetters
            np.random.shuffle(wordBin)
            
            wordList1 = wordBin[0:numWordsInStream]
            if condition==1:
                wordList2 = wordBin[numWordsInStream:numWordsInStream*2]
            else:  wordList2 = wordList1
            print('Now')
            print(wordList1)
            print(wordList2)
            sequenceStream1, sequenceStream2, cues = calcAndPredrawStimuli(wordList1,wordList2,cues,thisTrial)
            print('sequenceStream1=',sequenceStream1)
            print('sequenceStream2=',sequenceStream2)
            cuesSerialPos,correctAnswerIdxsStream1,correctAnswerIdxsStream2, ts  = \
                                                                        do_RSVP_stim(thisTrial, cues, sequenceStream1, sequenceStream2, noisePercent/100.,nDoneMain,eyetracking)
            numCasesInterframeLong = timingCheckAndLog(ts,nDoneMain)
            #call for each response
            expStop = list(); passThisTrial = list(); responses=list(); responsesAutopilot=list()
            numCharsInResponse = len(wordList1[0])
            dL = [None]*numRespsWanted #dummy list for null values
            expStop = copy.deepcopy(dL); responses = copy.deepcopy(dL); responsesAutopilot = copy.deepcopy(dL); passThisTrial=copy.deepcopy(dL)
            responseOrder = range(numRespsWanted)
            if thisTrial['upResponseFirst']: #change order of indices depending on upResponseFirst. response0, answer0 etc refer to which one had to be reported first
                    responseOrder.reverse()
            for i in responseOrder:
                x = 1.5 * sin(radians(AngleToStim))*thisTrial['wordEccentricity']*(i*2-1) #put it 3 times farther out than stimulus, so participant is sure which is left and which right
    #            blanksNeeded = numCharsInResponse
    #            respStim = visual.TextStim(myWin,pos=(0,x),colorSpace='rgb',color=(1,1,0),alignHoriz='center', alignVert='center',height=.16,units='norm',autoLog=autoLogging)
    #            respStr = '____'
    #            respStim.setText(respStr,log=False)
    #            respStim.draw(); 
    #            myWin.flip()
    #        
    #            waitingForSpace = True
    #            while waitingForSpace:
    #                for key in event.getKeys():
    #                    key = key.upper()
    #                    if key in ['SPACE']:
    #                        waitingForSpace=False
    
                #if (numResponses == numCharsWanted) and requireAcceptance:  #ask participant to HIT ENTER TO ACCEPT
    
                respStim = visual.TextStim(myWin,pos=(cos(radians(AngleToStim))*thisTrial['wordEccentricity']*thisTrial['hemifield'],x),colorSpace='rgb',color=(1,1,0),alignHoriz='center', alignVert='center',height=2.5,units='deg',autoLog=autoLogging)
                expStop[i],passThisTrial[i],responses[i],responsesAutopilot[i] = stringResponseKRedit.collectStringResponse(
                                          numCharsInResponse,respPromptStim,respStim,acceptTextStim,myWin,clickSound,badKeySound,
                                                                                       requireAcceptance,autopilot,responseDebug=True)                                                                               
            expStop = np.array(expStop).any(); passThisTrial = np.array(passThisTrial).any()
            if not expStop:
                print('main\t', end='', file=dataFile) #first thing printed on each line of dataFile to indicate main part of experiment, not staircase
                print(block,'\t', end='', file=dataFile)
                print(condition,'\t',end='', file=dataFile)
                print(nDoneMain,'\t', end='', file=dataFile)
                print(subject,'\t',task,'\t', round(noisePercent,3),'\t', end='', file=dataFile)
                print(thisTrial['hemifield'],'\t', end = '', file = dataFile)
                print(thisTrial['leftStreamFlip'],'\t', end='', file=dataFile)
                print(thisTrial['rightStreamFlip'],'\t', end='', file=dataFile)
                print(thisTrial['upResponseFirst'],'\t', end='', file=dataFile)
                i = 0
                eachCorrect = np.ones(numRespsWanted)*-999; eachApproxCorrect = np.ones(numRespsWanted)*-999
                for i in range(numRespsWanted): #scored and printed to dataFile in left first, right second order even if collected in different order
                    if i==0:
                        sequenceStream = sequenceStream1; correctAnswerIdxs = correctAnswerIdxsStream1; wordList = wordList1;
                    else: sequenceStream = sequenceStream2; correctAnswerIdxs = correctAnswerIdxsStream2; wordList = wordList2;
               
                    correct,approxCorrect,responsePosRelative = (
                            handleAndScoreResponse(passThisTrial,responses[i],responsesAutopilot[i],task,sequenceStream,cuesSerialPos,correctAnswerIdxs[i],wordList) )
                    eachCorrect[i] = correct
                    eachApproxCorrect[i] = approxCorrect
                for i in range(numWordsInStream):
                    print(wordList1[i],'\t',end='',file=dataFile)
                for i in range(numWordsInStream):
                    print(sequenceStream1[i],'\t',end='',file=dataFile)
                for i in range(numWordsInStream):
                    print(wordList2[i],'\t',end='',file=dataFile)
                for i in range(numWordsInStream):
                    print(sequenceStream2[i],'\t',end='',file=dataFile)
                print(numCasesInterframeLong, file=dataFile) #timingBlips, last thing recorded on each line of dataFile
                print('correct=',correct,' approxCorrect=',approxCorrect,' eachCorrect=',eachCorrect, ' responsePosRelative=', responsePosRelative)
                numTrialsCorrect += eachCorrect.all() #so count -1 as 0
                numTrialsApproxCorrect += eachApproxCorrect.all()
                numTrialsEachCorrect += eachCorrect #list numRespsWanted long
                numTrialsEachApproxCorrect += eachApproxCorrect #list numRespsWanted long
                    
                if exportImages:  #catches one frame of response
                     myWin.getMovieFrame() #I cant explain why another getMovieFrame, and core.wait is needed
                     framesSaved +=1; core.wait(.1)
                     myWin.saveMovieFrames('images_sounds_movies/frames.png') #mov not currently supported 
                     expStop=True
                core.wait(.1)
                #if feedback: play_high_tone_correct_low_incorrect(correct, passThisTrial=False)
                nDoneMain+=1
                
                dataFile.flush(); logging.flush()
                print('nDoneMain=', nDoneMain,' trials.nTotal=',trials.nTotal) #' trials.thisN=',trials.thisN
                if (trials.nTotal > 6 and nDoneMain > 2 and nDoneMain %
                     ( trials.nTotal*pctCompletedBreak/100. ) ==1):  #dont modulus 0 because then will do it for last trial
                        nextText.setText('Press "SPACE" to continue!')
                        nextText.draw()
                        progressMsg = 'Completed ' + str(nDoneMain) + ' of ' + str(trials.nTotal) + ' trials'
                        NextRemindCountText.setText(progressMsg)
                        NextRemindCountText.draw()
                        myWin.flip() # myWin.flip(clearBuffer=True) 
                        waiting=True
                        while waiting:
                           if autopilot: break
                           elif expStop == True:break
                           for key in event.getKeys():      #check if pressed abort-type key
                                 if key in ['space','ESCAPE']: 
                                    waiting=False
                                 if key in ['ESCAPE']:
                                    expStop = True
                        myWin.clearBuffer()
                core.wait(.2); time.sleep(.2)
        block = 2
         #end main trials loop
timeAndDateStr = time.strftime("%H:%M on %d %b %Y", time.localtime())
msg = 'Finishing at '+timeAndDateStr
print(msg); logging.info(msg)
if expStop:
    msg = 'user aborted experiment on keypress with trials done=' + str(nDoneMain) + ' of ' + str(trials.nTotal+1)
    print(msg); logging.error(msg)

#if not doStaircase and (nDoneMain >0):
#    msg = 'Of ' + str(nDoneMain)+' trials, on '+str(numTrialsCorrect*1.0/nDoneMain*100.)+'% of all trials all targets reported exactly correct'
#    print(msg); logging.info(msg)
#    msg= 'All targets approximately correct in '+ str( round(numTrialsApproxCorrect*1.0/nDoneMain*100,1)) + '% of trials'
#    print(msg); logging.info(msg)
#    for i in range(numRespsWanted):
#        msg = 'stream'+str(i)+': '+str( round(numTrialsEachCorrect[i]*1.0/nDoneMain*100.,2) ) + '% correct'
#        print(msg); logging.info(msg)
#        msg = 'stream' + str(i) + ': '+ str( round(numTrialsEachApproxCorrect[i]*1.0/nDoneMain*100,2) ) +'% approximately correct'
#        print(msg); logging.info(msg)

if eyetracking:
  if eyetrackFileGetFromEyelinkMachine:
    eyetrackerFileWaitingText = visual.TextStim(myWin,pos=(-.1,0),colorSpace='rgb',color = (1,1,1),alignHoriz='center', alignVert='center', units='norm',autoLog=autoLogging)
    eyetrackerFileWaitingText.setText('Waiting for eyetracking file from Eyelink computer. Do not abort eyetracking machine or file will not be saved?')
    eyetrackerFileWaitingText.draw()
    myWin.flip()
    msg = tracker.closeConnectionToEyeTracker(eyeMoveFile) #this requests the data back and thus can be very time-consuming, like 20 min or more
    print(msg); print(msg,file=logF) #""Eyelink connection closed successfully" or "Eyelink not available, not closed properly"
  else: 
    print('You will have to get the Eyelink EDF file off the eyetracking machine by hand')
logging.flush(); dataFile.close()
myWin.close() #have to close window if want to show a plot
if quitFinder:
        applescript="\'tell application \"Finder\" to launch\'" #turn Finder back on
        shellCmd = 'osascript -e '+applescript
        os.system(shellCmd)