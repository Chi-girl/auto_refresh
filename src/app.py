import threading
import os

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

class Action(threading.Thread):
    def __init__ (self, func, args, callback):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.callback = callback

    def run (self):
        res = None

        if type(self.args) is tuple:
            res = self.func(*self.args)
        elif type(self.args) is dict:
            res = self.func(**self.args)
        else:
            res = self.func(self.args)

        if(self.callback is not None):
            self.callback(res)

class App(threading.Thread):
    def __init__ (self, options, functions, interface):
        threading.Thread.__init__(self)
        self.options = options
        self.functions = functions
        self.interface = interface
        self.stringvar = {}
        self.process_running = False
        self.window = None

    def window_close(self):
        self.window.quit()

    def create_stringvar(self, name):
        self.stringvar[name] = tk.StringVar()

    def run_action(self, func_name, args, callback=None):
        if not self.process_running:
            def result(res):
                callback(res)
                self.process_running = False

            self.process_running = True
            
            action = Action(self.functions[func_name], args, result)
            action.start()

    def create_window(self, custom_options=None):
        options = {
            "width": 350,
            "height": 450,
            "icon": None,
            "resizable": False,
            "title": "App",
            "theme": "arc" 
        }

        # override default
        for key in self.options.keys():
            options[key] = self.options[key]
        if custom_options is not None:
            for key in custom_options.keys():
                options[key] = custom_options[key]
        
        if self.window is None:
            window = ThemedTk(theme=options['theme'])
        else:
            window = tk.Toplevel(self.window)

        # apply options
        if not options['resizable']:
            window.resizable(0,0)
        if options['icon'] is not None:
            window.iconphoto(False, tk.PhotoImage(file=options['icon']))
        window.title(options['title'])

        # set coordinates and window size
        window_x = int(window.winfo_screenwidth() / 2 - options['width'] / 2)
        window_y = int(window.winfo_screenheight() / 2 - options['height'] / 2)
        window.geometry(f"{options['width']}x{options['height']}+{window_x}+{window_y}")

        return window

    def run (self):
        self.window = self.create_window()
        self.window.protocol("WM_DELETE_WINDOW", self.window_close)
        self.interface(self)
        self.window.mainloop()