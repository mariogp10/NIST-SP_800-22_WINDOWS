# -*- coding: utf-8 -*-
import src.view.MainWindow as MW


if __name__ == '__main__':
    # Construir zip de despli
    # Inicializar objetos
    mainwin = MW.MainWindow()
    #mainwin.iconbitmap("media/logo-keigo-ventana.ico")

    # Launch Main Windows
    mainwin.mainloop()