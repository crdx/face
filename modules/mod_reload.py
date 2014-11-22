name = "Module reloader"
desc = "Reloads modules"

def on_pubmsg(p):
    words = p.event.arguments[0].split()

    if words[0] == "!r":
        p.connection.privmsg(p.event.target, "Rehashing")
        p.face.reload()

        # we've handled this event
        return True
