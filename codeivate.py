import sublime
import sublime_plugin
import webbrowser

from .codeivated import Prefs
from .codeivated.FeedBack import FeedBack
from .codeivated import Auth
from .codeivated.Listener import Listener

# import compileall
# compileall.compile_dir('/home/paul/.config/sublime-text-3/Packages/codeivate-st/codeivated/', force=True)

__version__      = '3.0.10'
__authors__      = ['"Paul Sinclair" <paul@codeivate.com>']

def plugin_loaded():
    Prefs.setup()
    Prefs.setOptions()
    Prefs.version = __version__

    # print(dir(Prefs))

    if Prefs.user_id is False or Prefs.user_token is False:
        sublime.set_timeout(Auth.validate_creds_startup, 10000)
    print("Codeivate started v."+__version__)

    # Auth.validate_creds()



class CodeivateOpenUserSummaryCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        webbrowser.open_new_tab('http://www.codeivate.com/summary')

class CodeivateOpenLeaderboardCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        webbrowser.open_new_tab('http://www.codeivate.com/users/leaderboard')


class CodeivateTagCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        current_tag = ""
        if sublime.active_window().id() in Prefs.tag :
            current_tag = Prefs.tag.sublime.active_window().id()
        sublime.active_window().show_input_panel("Tag this project", str(current_tag), self.on_input, None, None)

    def on_input(self, tag):
        if tag.strip() == "":
            tag = False
        else:
            tag = str(tag)

        #http://docs.python.org/2/library/stdtypes.html
        ##https://github.com/titoBouzout/SideBarEnhancements/search?q=def+file&ref=cmdform

        d = sublime.active_window().project_data()
        tag_data = {'tag':{sublime.active_window().id() : tag}}
        if d is None :
            d = {'codeivate' : [tag_data]}
        elif 'codeivate' not in d:
            d.update({'codeivate':[tag_data]})
        else :
            d['codeivate'].append([tag_data])

        Prefs.tag.update(tag_data)
        # print('sss')
        # dir(d)
        window = sublime.active_window()

        window = sublime.active_window()
        window.set_project_data(d)
