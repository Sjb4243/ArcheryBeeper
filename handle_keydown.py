from Queue import Queue

def handle_keydown(event, keymap):
    func = keymap.get(event.key)
    if not func:
        return None
    if isinstance(func, Queue):
        state = func.process_events()
        return state
    else:
        return func()
