#!/usr/bin/env python3
#!/bin/sh
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 20:57:58 2018

@author: J. Chichon, J.L. Vilas
"""

import tkinter as tk
from tkinter import filedialog as fd
from os import system
from subprocess import check_call

CHIMERA_PATH = '/home/vilas/scipion/software/em/chimera-1.10.1/bin/chimera'

CHIMERA_COMAND = 'chimeraVisualizatoin.cmd'

class Browse(tk.Frame):
    """ file browser and exutation.
    """

    def __init__(self, master, initialdir='', filetypes=()):
        super().__init__(master)
        self._listOfPath = []
        self._listOfvoxelsize = []
        self._listBox = None
        self.filepath = tk.StringVar()
        self.varDropDown = tk.StringVar()
        self._initaldir = initialdir
        self._filetypes = filetypes
        self._create_widgets()
        self._create_header()
        self._display_widgets()

    def _create_header(self):
        self._logo = tk.PhotoImage(file="logo.png")
        self._logpos = tk.Label(self, image=self._logo)

    def _create_widgets(self):
#        #tk.Label(self, text='Map').grid(row=0)
#        #tk.Label(self, text='Voxel Size').grid(row=1)
        self._entry = tk.Entry(self, textvariable=self.filepath)
#        #self._entry.grid(row=0, column=1)
        self._voxelSize = tk.Entry(self, textvariable=1)
#        #self._entry.grid(row=1, column=1)
        self._button = tk.Button(self, text="Browse", command=self.browse)
        self._Addbutton = tk.Button(self, text="Add", command=self.addToList)
        self._listBox = tk.Listbox(self)
        self._buttonRun = tk.Button(self, text="Visualize", command=self.visualize)

    def _display_widgets(self):
        self._logpos.pack(side="top")
        tk.Label(self, text='Image/Volume/Map path').pack()
        self._entry.pack(fill='x', expand=True)
        tk.Label(self, text='voxel size').pack()
        self._voxelSize.pack(fill='x')
        self._button.pack(anchor='e', side = tk.LEFT)
        self._Addbutton.pack(anchor='e', side = tk.LEFT)
        self.varDropDown.set("SPA")
        self._chosebox = tk.OptionMenu(self, self.varDropDown, "Fluorescence", "SPA", "Tomo/Xrays")
        self._chosebox.pack(anchor='e', side = tk.LEFT)
        tk.Label(self, text='Dealing with flourescence').pack()
        tk.Label(self, text='images, each image channel must').pack()
        tk.Label(self, text='be introduced separately').pack()
        tk.Label(self, text='in order green, red, blue, gray').pack()
        self._listBox.pack(side =  tk.TOP)
        
        self._buttonRun.pack(anchor='e', side = tk.BOTTOM)

    def browse(self):
        """ Browses a file from the entry.
        """
        self.filepath.set(fd.askopenfilename(initialdir=self._initaldir,
                                             filetypes=self._filetypes))

    def addToList(self):
        """ add a file or path to the list.
        """
        Vsize = self._voxelSize.get()
        self._listOfvoxelsize.append(Vsize)
        VolPath = self._entry.get()
        self._listOfPath.append(VolPath)
        self._listBox.insert(tk.END, VolPath)
 
    def visualize(self):
        """ chimera visualization
        """

        fhCmd = open(CHIMERA_COMAND, 'w')
        
        
        counter=0
        for item in self._listOfPath:
            if (self.varDropDown.get() == 'SPA'):
                fhCmd.write("open %s\n" % item)
                fhCmd.write("volume #%s voxelSize %s\n color pink" % 
                            (counter, (self._listOfvoxelsize[counter]) ) )
            if (self.varDropDown.get() == 'Fluorescence'):
                fhCmd.write("open %s\n" % item)
                if (counter % 3 == 0):
                    fhCmd.write("volume #%s style solid color green, voxelSize %s\n" % 
                            (counter, (self._listOfvoxelsize[counter]) ) )
                if (counter % 3 == 1):
                    fhCmd.write("volume #%s style solid color red, voxelSize %s\n" % 
                            (counter, (self._listOfvoxelsize[counter]) ) )
                if (counter % 3 == 2):
                    fhCmd.write("volume #%s style solid color blue, voxelSize %s\n" % 
                            (counter, (self._listOfvoxelsize[counter]) ) )

                
            if (self.varDropDown.get() == 'Tomo/Xrays'):
                fhCmd.write("open %s\n" % item)
                fhCmd.write("volume #%s voxelSize %s\n" % 
                            (counter, (self._listOfvoxelsize[counter]) ) )
            counter = counter + 1;
        fhCmd.close()
        runcommand = CHIMERA_PATH+ ' ' + CHIMERA_COMAND
        print(runcommand)
        system(runcommand)

if __name__ == '__main__':
    root = tk.Tk()
       
    file_browser = Browse(root, initialdir=r"C:\Users",
                                filetypes=(('All files','*.*'),
                                                            ("All files", "*.*")))
    file_browser.pack(fill='x', expand=True)

    

    root.mainloop()