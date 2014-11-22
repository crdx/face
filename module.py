import traceback
import imp

class Module():
    def __init__(self, module_filename):
        # the filename e.g. mod_list.py
        self.filename = module_filename

        # the filename without extension
        self.name = module_filename[:-3]

        # start marked as unloaded, so this will hold true if anything goes
        # terribly wrong with loading the module later on
        self.loaded = False

        self.load()

    def load(self):
        try:
            self.module = __import__(self.name)
            print("[+] Loaded {0}".format(self.name))
            self.loaded = True
        except Exception:
            print("[!] Failed to load {0}:".format(self.name))
            traceback.print_exc()

    def reload(self):
        if not self.loaded:
            self.load()
        else:
            try:
                imp.reload(self.module)
                print("[/] Reloaded {0}".format(self.name))
            except Exception:
                print("[!] Failed to reload {0}:".format(self.name))
                traceback.print_exc()
                self.loaded = False

    # Return "True" to halt further processing of modules.
    def handle_event(self, event_handled, p):
        # skip if we aren't loaded
        if not self.loaded:
            return event_handled

        # all modules always have their global event handler called
        self.call_method("global_handler", event_handled, p)

        # if this event hasn't been handled yet, see if this module will handle
        # it
        if not event_handled:
            return self.call_method("on_{0}".format(p.event.type), event_handled, p)
        else:
            return event_handled
        
    # Return "True" to halt further processing of modules.
    def call_method(self, method_name, event_handled, p):
        if method_name in dir(self.module):
            method = getattr(self.module, method_name)
            try:
                # pass the module's return value back
                return method(p)
            except Exception:
                print("Failed to call method {0} in {1}:".format(method_name, self.name))
                traceback.print_exc()

        # we didn't call this module, so maintain current state
        return event_handled
