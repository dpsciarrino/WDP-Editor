import tkinter as tk

class OutputFrame(tk.Frame):
    def __init__(self, app, window):
        self._app = app
        self._window = window
        
        tk.Frame.__init__(self, self._window, bg='WHITE', height=20)

        broadcaster = app.outputManager
        self.textBox = broadcaster.generateTextBox(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.textBox.grid(row=0, column=0, sticky="NEWS")
        broadcaster.scrollbar.grid(row=0, column=1, sticky="NS")
    
    @property
    def app(self):
        return self._app
    
    def printLine(self, text):
        self.app.outputManager.broadcast(text)
