import pafy
import sys
import urwid
import pyperclip
import urllib
import os
import subprocess
import time
import re



URL = raw_input("Enter URL\n")

######global variables###########3
title=""
author=""
vid_len=0
avail_stream_VideoO=None
avail_stream_audioO=None
avail_stream_both=None
downSeconloop=None
downThirdloop=None	
basecommand = "aria2c -j 10 -x 16 -m 0 -k 1M -s 25 -c "
filename=""
comp_command=""
downurl=None
dwndir = "~/Desktop"

###################Getting info about video#################


def getpafy(URL):
	try:
		vid = pafy.new(str(URL))
		global author
		global title 
		global vid_len 
		global avail_stream_both
		global avail_stream_audioO 
		global avail_stream_VideoO 
		author = vid.author
		title = vid.title
		vid_len = vid.length
		avail_stream_both = vid.streams
		avail_stream_audioO = vid.audiostreams
		avail_stream_VideoO = vid.videostreams	
	except RuntimeError,e:
		print str(e)
		sys.exit()
	except IOError,e:
		print str(e)
		print("please check the network Connection")
		retry = raw_input("Retry? y/n  ")
		if retry in ('Y','y'):
			getpafy(URL)	
		elif retry in ('N','n'):
			sys.exit()
	except ValueError,e: 
		print str(e)
		print "Please check URL provided"
		sys.exit()

#############parsing url for first time###########
getpafy(URL) # recursively call for parsing until Success
########################################################

#########################definitions#########################################
def on_clicked_cont(button):			##to call when continue pressed
	raise urwid.ExitMainLoop()
def menuVAOnly(button):			#called when user selects video/audio only in second loop
	raise urwid.ExitMainLoop()
def chosen_URL(button,choice):  #######show url of chosen format #####modify so that it calls axel to dowload the given url ############### called when a particular stream is selected
	v_chosen = urwid.Text([u'Video Format :-  ', str(choice), u'\n'])
	v_URL = urwid.Text([u'Downloadable URL :-  ', str(choice.url), u'\n'])
	done = urwid.Button(u'Copy URL to Clipboard')
	down = urwid.Button(u'Download using aria')
	ext = urwid.Button(u'Exit')
        urwid.connect_signal(done, 'click', Copy_exit,choice)
        urwid.connect_signal(ext, 'click', exit_program)
        urwid.connect_signal(down,'click',Down_aria,choice)
       	main1.original_widget = urwid.Filler(urwid.Pile([v_chosen,v_URL,urwid.AttrMap(done, None, focus_map='reversed'),urwid.AttrMap(down, None, focus_map='reversed'),urwid.AttrMap(ext, None, focus_map='reversed')]))
       	
##############################Displaying Video formats definitions########################
def menuAV(title, avail_stream_both):	###menu displaying formats with both audio and video ######### 2nd loop
	body = [urwid.Text(title), urwid.Divider()]
			
	for c in avail_stream_both:
	        button = urwid.Button(str(c) + " ----->" + str(c.resolution))
	        urwid.connect_signal(button, 'click', chosen_URL, c)
	        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	button = urwid.Button("Only Video/Audio Formats")
	urwid.connect_signal(button, 'click', menuVAOnly)
	body.append(urwid.AttrMap(button, None, focus_map='reversed'))

	button = urwid.Button("EXIT")
	urwid.connect_signal(button, 'click', exit_program)
	body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	
	return urwid.ListBox(urwid.SimpleFocusListWalker(body))

##########################################################################333

def menuVAOnlyMenu(title, avail_stream_VideoO,avail_stream_audioO):	###menu displaying formats with only audio or video ## must handle cases with audio and video alone ## for 3rd loop
	body = [urwid.Text(title), urwid.Divider()]
			
	for x in avail_stream_VideoO:
	        button = urwid.Button(str(x).split('@',1)[0]  + "---->" +x.resolution)
	        urwid.connect_signal(button, 'click', chosen_URL, x)
	        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	for x1 in avail_stream_audioO:
	        button = urwid.Button(str(x1))
	        urwid.connect_signal(button, 'click', chosen_URL, x1)
	        body.append(urwid.AttrMap(button, None, focus_map='reversed'))

	button = urwid.Button("EXIT")
	urwid.connect_signal(button, 'click', exit_program)
	body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	
	return urwid.ListBox(urwid.SimpleFocusListWalker(body))
	
#################3333##################################################
       	
def Copy_exit(button,choice):		####called when user selects copy to clipboard
	pyperclip.copy(str(choice.url))
	spam = pyperclip.paste()   
	sys.exit()
	
def Down_aria(button,choice):   ### called when user select download using aria ## it modifys flags which are further used to decide which loop to enter ### modifies "folename" "url" and "comp_command"(command to be executed with aria)
	global filename
	global comp_command
	global downSeconloop
	global downThirdloop
	global downurl
	filename = title + "." + choice.extension
	comp_command = basecommand + "-o " + filename 
	if str(choice.mediatype) == "normal" :
		downSeconloop=1
	elif  str(choice.mediatype) == "video" or str(choice.mediatype) == "audio"   :
		downThirdloop=1
	downurl = urllib.unquote(str(choice.url))
	raise urwid.ExitMainLoop()

def exit_program(button):  		####called when EXIT called
	sys.exit()



############################# print basic video info######################## 1st Loop info #################333#####can be done in a function too
palette = [('banner', 'black', 'light gray'),]
txt = urwid.Text(('banner', u"Hello !!! \nRequested Video Information....\n "))
p_title = urwid.Text(("Title :-  %s" %title))
p_author = urwid.Text(("Channel :-  %s" %author))
p_len = urwid.Text(("Length :-  "+"%d"%(vid_len/60) + ":" + "%d"%(vid_len%60)))
button_cont = urwid.Button(u'Press Enter to Continue') #continue button
urwid.connect_signal(button_cont, 'click', on_clicked_cont)
button_exit= urwid.Button(u'Press Enter to Exit') #exit button
urwid.connect_signal(button_exit, 'click', exit_program)
div = urwid.Divider(top=0)
pile = urwid.Pile([txt,p_title,p_author,p_len,div,urwid.AttrMap(button_cont, None , focus_map='reversed'),urwid.AttrMap(button_exit, None, focus_map='reversed')])
main2=urwid.Filler(pile)

####### starting first loop #########
loop = urwid.MainLoop(main2, palette=[('reversed', 'standout', '')])
loop.run()
####### First loop ending , Clear Screen for next screen

print "" #Dummy print for clear to work ?? find reason for this
subprocess.call("clear")
####################################################




##############starting the second loop###########displaying files with both audio and video
main1 = urwid.Padding(menuAV(u'Available Formats {normal:- contains both audio and video}', avail_stream_both), left=2, right=2)
top = urwid.Overlay(main1, urwid.SolidFill(u'\N{MEDIUM SHADE}'),align='center', width=('relative', 60),valign='middle', height=('relative', 90),min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
####################exiting audioVideo loop############check if download was requested###########################
if downSeconloop==1:    ######
	
	regex = re.compile('[^a-zA-Z0-9.]')
	filename = regex.sub('_', str(filename))
	filename=filename.replace("__","_")
	filename=filename.replace("__","_")
	print filename
	print "downloadinf to %s\n" %dwndir
	a=os.system("aria2c --out "+str(filename)+" -j 10 -x 16 -m 0 -k 1M -s 25  " +"-d %s" %dwndir + "  \"%s\"  " %downurl)
	#print a
if downSeconloop==1:      ###if download was for a/v files ####exit as furher videos not needed
	sys.exit()
################################################################33#################################3########




###########starting 3rd loop ###########################333###############################
##########skipping 3rd iteratio if already downloaded##########
if downSeconloop != 1 :   ############## execute only if video from 2nd loop not selecetd ###### known after first loop 2nd loop is executed and user choses "only audio/video" option
	
	main1 = urwid.Padding(menuVAOnlyMenu(u'Available Formats {Only Video OR Only Audio}', avail_stream_VideoO,avail_stream_audioO), left=2, right=2)
	top = urwid.Overlay(main1, urwid.SolidFill(u'\N{MEDIUM SHADE}'),align='center', width=('relative', 60),valign='middle', height=('relative', 90),min_width=20, min_height=9)
	urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()

###########################################################333
#################download from 3rd loop######################333
if downThirdloop == 1 :               ####downThirdloop=1 means a video from third loop is selected for downloads
	regex = re.compile('[^a-zA-Z0-9.]')
	filename = regex.sub('_', str(filename))
	filename=filename.replace("__","_")
	filename=filename.replace("__","_")
	print filename 
	print "downloadinf to %s\n" %dwndir
	a=os.system("aria2c --out "+str(filename)+" -j 10 -x 16 -m 0 -k 1M -s 25  " +"-d %s" %dwndir + "  \"%s\"  " %downurl)
sys.exit()

#####################################exit after all########################
