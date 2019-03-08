class StackFSM:
    def __init__(self):
        self.stack = []

    def update(self, *args, **kwargs):
        stateFn = self.getCurrentState()
        if stateFn is not None:
            stateFn(*args, **kwargs)

    def getCurrentState(self):
        return self.stack[-1] if len(self.stack) else None

    def popState(self):
        return self.stack.pop()

    def pushState(self, state):
        if state != self.getCurrentState():
            self.stack.append(state)
