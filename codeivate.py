import sublime
from .codeivated import Prefs
from .codeivated.FeedBack import FeedBack
from .codeivated import Auth
from .codeivated.Listener import Listener

def plugin_loaded():
    Prefs.setup()
    Prefs.setOptions()

    print( "loaded" )
