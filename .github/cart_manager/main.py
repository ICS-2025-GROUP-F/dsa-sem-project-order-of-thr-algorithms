import sys
import os


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.MainWindow import MainApplication

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()