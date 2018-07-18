#!/usr/bin/python
#  -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
import subprocess
from subprocess import call, Popen, PIPE
import sys
from threading  import Thread
from Queue import Queue, Empty
global builder
global winstatus
global textbuffer2
global end_iter
end_iter = None
import time
import os
import psutil
import filecmp

def enqueue_output(out, queue):
	for line in iter(out.readline, b''):
		queue.put(line)
	out.close()

def copyfiles(self, filename, drivenumber, direction):
	print(filename, drivenumber, direction)
	return


def verify(self, filename, drivenumber, direction, starttrack, endtrack):
	print ("Running Verify")
	global builder
	global end_iter
	ON_POSIX = 'posix' in sys.builtin_module_names
	print (self, filename, drivenumber, direction, starttrack, endtrack)

	Popen(['mkdir /tmp/xumgui'], bufsize=0, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	Popen(['rm -rf /tmp/xumgui/*'], bufsize=0, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

	# p = Popen(['d64copy -vvv -s{0} -e{1} {2} /tmp/xumgui/verifyimageread.d64'.format(starttrack, endtrack, drivenumber)], bufsize=1, universal_newlines=True, stdout=PIPE, stderr=PIPE, shell=True, close_fds=ON_POSIX)


	commandstring = ('d64copy -vvv {0} /tmp/xumgui/verifyimageread.d64')
	print (commandstring.format(drivenumber))
	p = Popen([commandstring.format(drivenumber)], bufsize=1, universal_newlines=True, stdout=PIPE, stderr=PIPE, shell=True, close_fds=ON_POSIX)


	builder.get_object("textview").show()
	q = Queue()
	q2 = Queue()
	t = Thread(target=enqueue_output, args=(p.stdout, q))
	t2 = Thread(target=enqueue_output, args=(p.stderr, q2))
	t.daemon = True  # thread dies with the program
	t2.daemon = True  # thread dies with the program
	t.start()
	t2.start()


	# read line without blocking
	while p.poll() == None: # no return code, yet. process till running
		try:
			line = q.get_nowait()  # or q.get(timeout=.1)
		except Empty:
			# print('no output yet')
			a = 0
		else:  # got line
			end_iter = textbuffer2.get_end_iter()
			textbuffer2.insert(end_iter, line) # sys.stdout.write(line)
		try:
			line2 = q2.get_nowait()  # or q.get(timeout=.1)
		except Empty:
			# print('no output yet')
			a = 0
		else:  # got line
			end_iter = textbuffer2.get_end_iter()
			textbuffer2.insert(end_iter, line2)  # sys.stdout.write(line)

		if end_iter != None:
			builder.get_object("textview").scroll_to_iter(end_iter, 0.0, False, 0.5, 1.0)

		while Gtk.events_pending():
			Gtk.main_iteration()
		continue

	result = filecmp.cmp(filename, '/tmp/xumgui/verifyimageread.d64')
	if result:
		resultstring = "Verify OK!"
	else:
		resultstring = "Verify failed!"

	textbuffer2.insert(end_iter, resultstring)
	builder.get_object("textview").scroll_to_iter(end_iter, 0.0, False, 0.5, 1.0)
	print ("Filename: ", filename)
	print ("Result: ", result)
	return


def copytracks(self, filename, drivenumber, direction, starttrack, endtrack):
	global winstatus
	global textbuffer2
	global builder
	global end_iter

	retcode = 0
	# endtrack = 3
	#filename = 'hostages.d64'
	ON_POSIX = 'posix' in sys.builtin_module_names

	# print ("Pre Command")

	if endtrack == 35:
		endtrack = ""
	else:
		endtrack = "-e"+str(endtrack)

	print endtrack
	#p = Popen(['d64copy -vvv -s{0} -e{1} \"{2}\" {3}'.format(starttrack, endtrack, filename, drivenumber)], bufsize=1, universal_newlines=True, stdout=PIPE, stderr=PIPE, shell=True, close_fds=ON_POSIX)


	# p = Popen(['d64copy -vvv {0} -e{1} \"{2}\" {3}'.format(starttrack, endtrack, filename, drivenumber)], bufsize=1, universal_newlines=True, stdout=PIPE, stderr=PIPE, shell=True, close_fds=ON_POSIX)

	commandstring = ('d64copy -vvv -s{0} {1} \"{2}\" {3}')
	print (commandstring.format(starttrack, endtrack, filename, drivenumber))
	# p = Popen([commandstring.format(starttrack, endtrack, filename, drivenumber)], bufsize=1, universal_newlines=True, stdout=PIPE, stderr=PIPE, shell=True, close_fds=ON_POSIX)
	p = Popen([commandstring.format(starttrack, endtrack, filename, drivenumber)], bufsize=1, universal_newlines=True, stdout=PIPE, stderr=PIPE, shell=True, close_fds=ON_POSIX)

	# print ("Post Command")

	# p = Popen(['nohup d64copy -vvv -s{0} -e{1} {2} {3}'.format(starttrack, endtrack, filename, drivenumber)], bufsize=1, universal_newlines=True, stdout=PIPE, stderr=PIPE, shell=True, close_fds=ON_POSIX, preexec_fn=os.setpgrp)
	# ... do other things here
	builder.get_object("cancelbutton").set_label("Cancel")
	winstatus.show()
	builder.get_object("textview").show()
	q = Queue()
	q2 = Queue()
	t = Thread(target=enqueue_output, args=(p.stdout, q))
	t2 = Thread(target=enqueue_output, args=(p.stderr, q2))
	t.daemon = True  # thread dies with the program
	t2.daemon = True  # thread dies with the program
	t.start()
	t2.start()


	# read line without blocking
	while p.poll() == None: # no return code, yet. process till running
		try:
			line = q.get_nowait()  # or q.get(timeout=.1)
		except Empty:
			# print('no output yet')
			a = 0
		else:  # got line
			end_iter = textbuffer2.get_end_iter()
			textbuffer2.insert(end_iter, line) # sys.stdout.write(line)
		try:
			line2 = q2.get_nowait()  # or q.get(timeout=.1)
		except Empty:
			# print('no output yet')
			a = 0
		else:  # got line
			end_iter = textbuffer2.get_end_iter()
			textbuffer2.insert(end_iter, line2)  # sys.stdout.write(line)

		builder.get_object("textview").scroll_to_iter(end_iter, 0.0, False, 0.5, 1.0)
		while Gtk.events_pending():
			Gtk.main_iteration()
		continue

	# print (builder.get_object("trackpcfverify").get_active())
	# trackpcfverify
	verifybutton = builder.get_object("trackpcfverify").get_active()
	if verifybutton:
		verify(self, filename, drivenumber, direction, starttrack, endtrack)

	textbuffer2.insert(end_iter, '')
	textbuffer2.insert(end_iter, '')
	end_iter = textbuffer2.get_end_iter()
	builder.get_object("textview").scroll_to_iter(end_iter, 0.0, False, 0.5, 1.0)

	builder.get_object("cancelbutton").set_label("OK")
	return


def copynib(self, filename, drivenumber, direction, starttrack, endtrack):
	print(filename, drivenumber, direction, starttrack, endtrack)
	return


def other(self, filename, drivenumber, direction, starttrack, endtrack):
	print(filename, drivenumber, direction, starttrack, endtrack)
	return


class Handler:
	def gtk_main_quit(self, *args):
		Gtk.main_quit()
		return


	def go_button_clicked(self, gobutton):
		category = gobutton.get_name()[:-2]
		filename = builder.get_object(category+"path").get_filename()
		alltabs = ["filepcf", "filefpc", "trackpcf", "trackfpc", "nibpcf", "nibfpc"]
		if category == "filepcf":
			modenumber = 0
		elif category == "filefpc":
			modenumber = 1
		elif category == "trackpcf":
			modenumber = 2
		elif category == "trackfpc":
			modenumber = 3
		elif category == "nibpcf":
			modenumber = 4
		elif category == "nibfpc":
			modenumber = 5
		else:
			print("determining Category failed!")
			modenumber = None
		#find chosen drive number
		drivegroup = builder.get_object(alltabs[modenumber]+"chosendrive")
		active = next(
			radio for radio in
			drivegroup.get_group()
			if radio.get_active()
		) # print ("Drive   : " + str(active.get_name()))
		drive = active.get_name()
		drive = drive[-2:]
		if drive == "ve":
			drivenumber = 8
		elif drive == "e9":
			drivenumber = 9
		elif drive == "10":
			drivenumber = 10
		elif drive == "11":
			drivenumber = 11
		else:
			print ("else")
			drivenumber = 12

		starttrack = int((builder.get_object(category + "st").get_value()))
		endtrack = int((builder.get_object(category + "et").get_value()))

		# Decide which transfer function is wanted
		if category == "filepcf":
			copyfiles(self, filename, drivenumber, "pcf")
		elif category == "filefpc":
			copyfiles(self, filename, drivenumber, "fpc")
		elif category == "trackpcf":
			copytracks(self, filename, drivenumber, "pcf", starttrack, endtrack)
		elif category == "trackfpc":
			copytracks(self, filename, drivenumber, "fpc", starttrack, endtrack)
		elif category == "nibpcf":
			copynib(self, filename, drivenumber, "pcf", starttrack, endtrack)
		elif category == "nibfpc":
			copynib(self, filename, drivenumber, "fpc", starttrack, endtrack)
		else:
			print("Could not execute category sub!")
		return


	def cancelbutton(self, cancelbutton):
		result = Popen(['killall d64copy'], bufsize=0, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		print (result)
		Popen(['cbmctrl reset'], bufsize=0, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		Popen(['rm -rf /tmp/xumgui/*'], bufsize=0, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		winstatus.hide()
		return


builder = Gtk.Builder()
builder.add_from_file("xumgui.ui")
builder.connect_signals(Handler())
# window = builder.get_object("window1")
# window.show_all()

# just for debugging - KILLME!
Popen(['killall d64copy'], bufsize=0, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
winstatus = builder.get_object("winstatus")  # type: GObject
textbuffer2 = builder.get_object("textbuffer2")
Gtk.main()
