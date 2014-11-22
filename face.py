#!/usr/bin/env python3

import sys, os, traceback, imp

import irc.client
import irc.events

from module import Module
from wrapper import Wrapper
import config
import util

class Face(irc.client.SimpleIRCClient):
    def __init__(self):
        irc.client.SimpleIRCClient.__init__(self)
        sys.path.append(config.modules_dir)

    # Where it all begins. Load modules, and connect.
    def go(self):
        self.load_modules()

        try:
            print("Connecting to {0} on port {1}".format(config.server, config.port))
            self.connect(config.server, config.port, config.nickname)
        except irc.client.ServerConnectionError as x:
            print(x)
            sys.exit(1)

        for event in irc.events.all:
            # 0 = highest priority
            self.connection.add_global_handler(event, self.global_handler, 0)

        try:
            self.start()
        except KeyboardInterrupt:
            self.connection.close()

    # This global handler receives all events and dispatches them to the
    # relevant modules.
    def global_handler(self, connection, event):
        p = Wrapper(self, connection, event, config, util)

        event_handled = False

        # tell all modules that this event has fired
        for module in self.modules:
            # a module returning True means it declares it's handled the
            # event and no further events should be handled (aside from
            # the global handler)
            event_handled = module.handle_event(event_handled, p)

    # Reload our own config, our modules, and ensure config changes are applied.
    def reload(self):
        # reload all the things
        imp.reload(config)
        imp.reload(util)
        self.load_modules()

        # if the nickname in the config file has changed then change our
        # nickname on IRC as well
        if self.connection.get_nickname() != config.nickname:
            self.connection.nick(config.nickname)

    # Loop through all modules, reload any existing ones and freshly load
    # any we haven't seen before.
    def load_modules(self):
        # load the filenames of all modules that exist in the modules directory
        module_filenames = [ f for f in os.listdir(config.modules_dir) if f.endswith(".py") and f != '__init__.py' ]

        print("Searching for modules")

        # create the modules list if not already set
        if not hasattr(self, "modules"):
            self.modules = []

        # reload any loaded modules rather than loading them from scratch
        if len(self.modules) > 0:
            for module in self.modules:
                # if it exists in the filenames list above, remove it as we
                # don't want to to load it again
                if module.filename in module_filenames:
                    module_filenames.remove(module.filename)

                # load it instead
                module.reload()

        # load all remaining unloaded modules
        for module_filename in module_filenames:
            self.modules.append(Module(module_filename))

    # Called when first connecting to the server. Join any channels we're
    # configured to join.
    def on_welcome(self, connection, event):
        print("> {0}".format(event.arguments[0]))

        for channel in config.channels:
            print("Joining {0}".format(channel))
            connection.join(channel)

    # Called when getting disconnected.
    def on_disconnect(self, connection, event):
        # TODO reconnect instead
        sys.exit(0)

def main():
    print("Starting up {0}".format(config.nickname))
    face = Face();
    face.go();

if __name__ == "__main__":
    main()
