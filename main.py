import tkinter as tk
import logging
from views.main_view import MainView

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler("app.log"),
                                  logging.StreamHandler()])
    
    root = tk.Tk()
    root.title("Traducator Fisiere")
    root.geometry('480x360')
    root.configure(background="#f0f0f0")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    MainView(root)

    root.resizable(False, False)
    root.mainloop()
