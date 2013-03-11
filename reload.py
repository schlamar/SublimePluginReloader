
import imp
import os
import sys

import sublime
import sublime_plugin


def _in_package_path(mod_file):
    ppath = sublime.packages_path()
    return os.path.commonprefix([mod_file, ppath]) == ppath


def _is_plugin(mod_file):
    '''All modules with more than one nested package are not
    considered as plugin by Sublime.
    '''
    ppath_level = len(sublime.packages_path().split(os.sep))
    mod_level = len(os.path.dirname(mod_file).split(os.sep))
    return mod_level - ppath_level == 1


def reload_plugins():
    plugins = list()
    libraries = list()
    for mod_name, mod in sys.modules.items():
        if hasattr(mod, '__file__'):
            if _in_package_path(mod.__file__):
                if _is_plugin(mod.__file__):
                    plugins.append(mod)
                else:
                    libraries.append(mod_name)

    for mod_name in libraries:
        sys.modules.pop(mod_name)

    for mod in plugins:
        if hasattr(mod, 'plugin_unloaded'):
            mod.plugin_unloaded()

        try:
            imp.reload(mod)
        except Exception as e:
            # Some errors can happen.
            # For example unloaded plugins are still in sys.modules.
            print ('Can\'t reload %s: %s.' % (mod.__name__, e))


class ReloadPluginsCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        reload_plugins()
