
import imp
import os
import sys

import sublime
import sublime_plugin


def _in_package_path(filename):
    ppath = sublime.packages_path()
    return os.path.commonprefix([filename, ppath]) == ppath


def _is_plugin(mod_name):
    '''All modules with more than one nested package are not
    considered as plugin by Sublime.
    '''
    return len(mod_name.split('.')) <= 2


def reload_plugins():
    plugins = list()
    libraries = list()
    for mod_name, mod in sys.modules.items():
        if hasattr(mod, '__file__'):
            if _in_package_path(mod.__file__):
                if _is_plugin(mod_name):
                    plugins.append(mod)
                else:
                    libraries.append(mod_name)

    for mod_name in libraries:
        sys.modules.pop(mod_name)

    for mod in plugins:
        imp.reload(mod)


class ReloadPluginsCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        reload_plugins()

