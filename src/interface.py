import tkinter as tk
from tkinter import ttk

import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

header_text = "Data Preprocessing Tool"
#subheader_text = ""

success_message = "Refresh file is now available"
input_error_message = "Invalid"

# directories = [("Path 1", None), ("Historical data", [".xlsx", ".csv"]),("Latest data", [".xlsx", ".csv"])]
directories = [("Data Dump Path", None)]

def interface(app):
    main_frame = ttk.Frame(app.window, borderwidth=10)
    main_frame.pack(expand=True, fill=tk.BOTH)

    text_frame = ttk.Frame(main_frame)
    input_frame = ttk.Frame(main_frame)
    loading_frame = ttk.Frame(main_frame)

    text_frame.place(relx=0, rely=0, relwidth=1, relheight=0.2)
    input_frame.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.55)
    loading_frame.place(relx=0.05, rely=0.78, relwidth=0.9, relheight=0.175)

    # TEXT FRAME
    header = ttk.Label(text_frame, text=header_text, font="bold 13", anchor="s")
    header.pack(expand=True, fill=tk.BOTH)
    #subheader = ttk.Label(text_frame, text=subheader_text, wraplength='320', justify="center")
    #subheader.pack(expand=True)


    # INPUT FRAME
    for key, extensions in directories:
        app.create_stringvar(key)

    def validate():
        invalid = [key for index, (key, extensions) in enumerate(directories) if app.stringvar[key].get() == ""]
        return len(invalid) == 0

    def progress(status, value):
        app.stringvar['status'].set(status)
        loading_bar.step(value)

    def response(res):
        if res == "success":
            messagebox.showinfo("Success", success_message)
        else:
            messagebox.showerror('Error', res)

    def execute():
        if validate():
            args = {k.lower().replace(" ", "_"):app.stringvar[k].get() for k, extensions in directories}
            args['progress'] = progress
            #args['refresh_type'] = Refresh_Type.get() 
            
            #TODO
            # Add your if else :app.run_action()
            app.run_action("analyze", args, callback=response)
        else:
            messagebox.showerror('Error', input_error_message)

    for key, extensions in directories:
        create_field(input_frame, key, app.stringvar[key], onchange=lambda: progress("Ready!", 0) if validate() else None, extensions=extensions)
        
    #TODO:
    # Refresh_OPTIONS = ["Process1", "Process2"] 
    #Refresh_OPTIONS = ["Weekly Refresh","Monthly Refresh"]
    #Refresh_Type = ttk.Combobox(loading_frame, values=Refresh_OPTIONS,text=subheader_text, justify="center")
    #Refresh_Type.current(0) #Default value
    #Refresh_Type.pack(expand=True,fill=tk.X,side=tk.TOP)

    execute_btn = ttk.Button(input_frame, text="Run", command=execute)
    execute_btn.pack(expand=True, fill=tk.X)

    # LOADING FRAME
    app.create_stringvar("status")
    app.stringvar['status'].set("Please input the required directories.")
    progress_label = ttk.Label(loading_frame, textvariable=app.stringvar["status"], anchor="s")
    progress_label.pack(expand=True, fill=tk.BOTH)
    loading_bar = ttk.Progressbar(loading_frame,orient="horizontal", length=100)
    loading_bar.pack(expand=True, fill=tk.X)

def create_field(parent, label, stringvar, onchange, extensions=None):
    container_frame = ttk.Frame(parent)
    container_frame.pack(fill=tk.X)
    directory_label = ttk.Label(container_frame, text=label, justify='left')
    directory_label.pack(fill=tk.X)

    def input_changed():
        stringvar.set(get_file(extensions))
        onchange()

    input_container_frame = ttk.Frame(container_frame, height=30)
    input_container_frame.pack(fill=tk.X)
    directory_entry = ttk.Entry(input_container_frame, textvariable=stringvar)
    directory_entry.place(relx=0, rely=0, relheight=1, relwidth=0.7)
    directory_btn = ttk.Button(input_container_frame, text="Set", command=input_changed)
    directory_btn.place(relx=0.71, rely=0, relheight=1, relwidth=0.29)

def get_file(extensions):
    if extensions is not None:
        fileObj = filedialog.askopenfile(filetypes=[("Excel files", " ".join(extensions))])
        path = fileObj.name if fileObj is not None else ""
    else:
        path = filedialog.askdirectory()
    return path