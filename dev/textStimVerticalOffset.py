#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Text is not vertically centered. Instead, 'center' coordinate it is drawn at is actually a point partway up from the text's vertical center. 
"""

from __future__ import division

from psychopy import visual, core, event

# Create a window to draw in
win = visual.Window((800.0, 800.0), allowGUI=False, winType='pyglet',
            monitor='testMonitor', units ='deg', screen=0)
win.recordFrameIntervals = True

# Choose some fonts. If a list is provided, the first font found will be used.
fancy = ['Monotype Corsiva', 'Palace Script MT', 'Edwardian Script ITC']
sans = ['Gill Sans MT', 'Arial', 'Helvetica', 'Verdana']
serif = ['Times', 'Times New Roman']
comic = 'Comic Sans MS'  # the short name won't work

upper = visual.TextStim(win, text="YXIXM", pos=(0, 2),  # and can have line breaks
    color=[-1.0, -1, 1],
    units='deg',
    height = 3.0,
    alignHoriz='center', alignVert='center',
    font = sans 
    )
lower = visual.TextStim(win, text="YXIXM", pos=(0, -2),  # and can have line breaks
    color=[-1.0, -1, 1],
    units='deg',
    height = 3.0,
    alignHoriz='center', alignVert='center',
    font = sans
    )

fixationPoint= visual.PatchStim(win,colorSpace='rgb',color=(1,1,1),size=5,units='pix')
horizontalMeridian = visual.Line(win, start=(-5,0), end=(5,0), fillColor=(0,1,1))
vertLine = visual.Line(win, start=(0,-2), end=(0,2), fillColor=(1,0,-.3))
trialClock = core.Clock()
t = lastFPSupdate = 0

# Continues the loop until any key is pressed
stop = False
while not stop:
    upper.draw()
    lower.draw()
    fixationPoint.draw()
    horizontalMeridian.draw()
    vertLine.draw()
    win.flip()
    keysPressed = event.getKeys()            #print 'keysPressed = ', keysPressed
    if len(keysPressed)>0:
        if keysPressed[-1].upper() in ['BACKSPACE','DELETE','ESCAPE','SPACE']:
            stop = True

win.close()
core.quit()

# The contents of this file are in the public domain.
