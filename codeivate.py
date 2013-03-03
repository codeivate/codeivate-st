#see wordcount for example
#http://www.sublimetext.com/docs/2/api_reference.html
import sublime
import sublime_plugin

#import functools
#import os
#import csv
# from subprocess #import Popen
#import subprocess
#import codeivated.ActivityMonitor
import codeivated.Auth as Auth
from codeivated.Listener import Listener
from codeivated.Prefs import Pref
from codeivated.Pushover import ThreadPushover

#am = codeivated.ActivityMonitor.ActivityMonitor()


print "starting"
print Pref.user_id




#sublime.set_timeout(Auth.check_creds, 10000)

if Pref.user_id == False or Pref.user_token == False :
    sublime.set_timeout(Auth.validate_creds_startup, 10000)
#Auth.validate_creds()
   


##window = sublime.active_window()    
##window.show_quick_panel(['a','b'], on_d)
# window.show_input_panel("Goto Line:", "", on_d, None, None)

# class BoostCommand(sublime_plugin.ApplicationCommand):

#     def run(self):
#         self.window.show_input_panel("Goto Line:", "", self.on_done, None, None)
#         pass

#     def on_done(self, text):
#         try:
#             line = int(text)
#             if self.window.active_view():
#                 self.window.active_view().run_command("goto_line", {"line": line} )
#         except ValueError:
#             pass

# class powerupCommand(sublime_plugin.WindowCommand):

#     def run(self, block):
#         print block
        
#         self.window.show_input_panel("Goto Line:", "", self.on_done, None, None)
#         pass

#     def on_done(self, text):
#         try:
#             line = int(text)
#             if self.window.active_view():
#                 self.window.active_view().run_command("goto_line", {"line": line} )
#         except ValueError:
#             pass


# class set_idle_enabled(sublime_plugin.ApplicationCommand):

#     def __init__(self):
#         #sublime.message_dialog('derp')
#         #l = codeivated.Listener.Listener()
#         self.codeivator = codeivated.ActivityMonitor.ActivityMonitor()
#         self.codeivator.start()

#     def description(self):
#         print "pre desc"
#         return 'Disable' if Pref.enabled else 'Enable'

