import sublime
import sublime_plugin
import codeivated.Auth as Auth
from codeivated.Listener import Listener
from codeivated.Prefs import Pref
from codeivated.Pushover import ThreadPushover


if Pref.user_id == False or Pref.user_token == False :
    sublime.set_timeout(Auth.validate_creds_startup, 10000)
