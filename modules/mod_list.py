name = "Module lister"
desc = "Lists modules"

def on_pubmsg(p):
    if p.event.arguments[0].startswith("!listmodules"):
        unloaded = []
        for module in p.face.modules:
            if not module.loaded:
                unloaded.append(module.name)
            else:
                line = "{0}: ".format(module.name)
                line += module.module.name if hasattr(module.module, "name") else "???"
                line += " ({0})".format(module.module.desc) if hasattr(module.module, "desc") else " (???)"
                p.connection.privmsg(p.event.target, line)

        if len(unloaded) > 0:
            p.connection.privmsg(p.event.target, "Unloaded modules: {0}".format(", ".join(unloaded)))
