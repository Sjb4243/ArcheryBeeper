from Queue import Queue

#handling inputs
#If there's no match return None so we know to do nothing later on
#Otherwise return whatever the queue finished as, could be exit or a successful completion
#Doesnt reall matter because we don't do anything with it after
#Otherwise if its a function then execute it

def handle_keydown(event, keymap):
    func = keymap.get(event.key)
    if not func:
        return None
    #Passing the state back to main menu, not even sure if this is needed

    if isinstance(func, Queue):
        state = func.process_events()
        return state
    else:
        return func()
