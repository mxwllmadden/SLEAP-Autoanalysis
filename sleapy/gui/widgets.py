import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from typing import List

class ParameterWindow(ttk.Frame):
    def __init__(self, container, paramlabels : List[str], 
                 paramvars : List[tk.StringVar]):
        super().__init__(container)
        # Use the kwargs provided
        self.paramlabels = paramlabels
        self.paramvars = paramvars
        # Create the parameters entry windows etc etc.
        for ind, (label, var) in enumerate(zip(paramlabels, paramvars)):
            tk.Label(self, text = label, anchor="w",width = 20).grid(column=0, row=ind,padx=10,pady=10,sticky="e")
            tk.Entry(self, width=18, textvariable=var).grid(column=1,row=ind,padx=10,pady=10,sticky="w")

class ConsoleOutput(ttk.Frame):
    def __init__(self, master=None, max_lines=1000, **kwargs):
        super().__init__(master, **kwargs)
        self.text = ScrolledText(self, wrap=tk.WORD, font=('Courier', 10), bg='black', fg='#9b4dca')
        self.text.pack(fill='both', expand=True)
        self.text.config(state='disabled')
        self.max_lines = max_lines  # Limit the number of lines

    def write(self, message):
        self.text.config(state='normal')
        self.text.insert('end', message + '\n')
        self._limit_lines()  # Remove excess lines
        self.text.config(state='disabled')
        self.text.see('end')

    def clear(self):
        self.text.config(state='normal')
        self.text.delete('1.0', 'end')
        self.text.config(state='disabled')

    def _limit_lines(self):
        line_count = int(self.text.index('end-1c').split('.')[0])  # Get total line count
        if line_count > self.max_lines:
            self.text.delete('1.0', f'{line_count - self.max_lines + 1}.0')  # Remove oldest lines



# Example Usage
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("800x400")

    console = ConsoleOutput(root, max_lines=50)  # Limit to 50 lines
    console.pack(fill='both', expand=True)

    # Simulate output
    def add_log():
        for i in range(100):
            console.write(f"Log entry {i + 1}")

    button = tk.Button(root, text="Generate Logs", command=add_log)
    button.pack()

    root.mainloop()
