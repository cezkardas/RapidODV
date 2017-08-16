#first import is sometimes neccessary for export to .exe
import matplotlib.backends.backend_tkagg
import matplotlib.pyplot as plt
from cycler import cycler 

import csv, os 
from os import path

from matplotlib.dates import DateFormatter


from tkinter import *
from tkinter.filedialog import askopenfilename 


x=[]
y=[]
d=[]
items = []

class MyFrame(Frame):
    
    def __init__(self):
        
       
        
        #structure of the main window 
        Frame.__init__(self)
        self.names = []
        self.var = IntVar()
        self.v = IntVar()
      
        self.listbox = Listbox(self, selectmode=MULTIPLE)
               
        self.master.title("RapidODV 1.0.0")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)

        self.checkbutton = Checkbutton(self, text="Use Y2 axis", variable=self.var, onvalue=1, offvalue=0)
        self.button = Button(self, text="Browse", command=self.load_file, width=25)
        self.button2 = Button(self, text="Load headers", command=self.load_headers, width=25)
        self.button3 = Button(self, text="Select Y2", command=self.select_secondary, width=25)
        self.button4 = Button(self, text="Plot", command=self.edit_csv, width=25)
        
        self.checkbutton.grid(row=1, column=0, sticky=W)
        self.button.grid(row=2, column=0, sticky=W)
        self.button2.grid(row=3, column=0, sticky=W)
        self.button3.grid(row=7, column= 0, sticky=W)
        self.button4.grid(row=8, column=0, sticky=W)
        
    def load_file(self, parent=__init__):
        
        #browsing for .csv files and loading it
        self.filecount=1;
        fname = askopenfilename(filetypes=(("CSV", "*.csv"),("All files", "*.*") ))
        if fname:
            try:
                self.name=fname
            except:                    
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return
        
        #destroying widgets if left over after previous files
        try:
            for i in self.checkbuttons:
                i.destroy()
        except:
            pass
       
    def load_headers(self, parent=__init__):
        
        #destroying widgets; fail-safe for when user does not go back to loading
        #or reloads headers after unchecking the box
        try:
            self.entry1.destroy()
            self.entry2.destroy()
            for i in self.checkbuttons:
                i.destroy()
        except:
            pass
        
        #opening file for access
        inf = open(self.name)
        reader = csv.reader(inf)
        
        #Axis title input textbox
        self.entry1=Entry(self)
        self.entry1.grid(row=4, column=0, sticky=W)
        self.entry1.insert(END, "Enter Y1 axis title")
        
        #Initialization of parameter list
        self.listbox.delete(0,END)
        self.listbox.grid(row=6, column=0, sticky=W)
        
        for row in reader:
            for col in range(len(row)):
                self.listbox.insert(col, row[col])
            break

        #Secondary axis title input texbox
        if self.var.get()==1:
            self.entry2=Entry(self)
            self.entry2.grid(row=5, column=0, sticky=W)
            self.entry2.insert(END, "Enter Y2 axis title")
        else:
            #unnecessary Select Y2 button disappears
            self.button4.grid(row=7, column=0, sticky=W)
        inf.close()
        return
    
    
    def select_secondary(self, parent=__init__):
        
        if self.var.get()==1:
            
            
            try:
                for i in self.checkbuttons:
                    i.destroy()
            except:
                pass
            
            inf = open(self.name)
            reader = csv.reader(inf)    
            
            items = self.listbox.curselection()
            
            #reading parameter names from first line 
            MODES=[]
            mod=[]
        
            for i in range(1,len(items)):
                inf.seek(0)
                for line in reader:
                    mod.append(i)
                    mod.append(line[items[i]])
                    MODES.append(mod)
                    mod=[]
                    break
                
            for i in range(len(items)-1):
                self.names.append(MODES[i][1])
           
            
            #creating checkbuttons for secondary axis selection
            self.checkbuttons=[]
         
            for text, mode in MODES:
                dtemp = IntVar()
                d.append(dtemp)
                self.checkbuttons.append(Checkbutton(self, text=mode, variable=d[text-1], onvalue=1, offvalue=0))
                self.checkbuttons[text-1].grid(row=7+text, column=0, sticky=W)
                
            
           #placing plot button below the checkbuttons
            self.button4.grid(row=8+len(items), column=0, sticky=W)
            inf.close()
        else:
            print("Y2 not activated")
            
        return

    def edit_csv(self):
        
        #redundant file access, listbox - used when Y2 is not in use
        listofy=[] 
        listofx=[]
        
        basename=os.path.splitext(self.name)[0]
        
        inf = open(self.name)
        reader = csv.reader(inf)

        items = self.listbox.curselection()
        
        if self.var.get()==0:
            MODES=[]
            mod=[]
        
            for i in range(1,len(items)):
                inf.seek(0)
                for line in reader:
                    mod.append(i)
                    mod.append(line[items[i]])
                    MODES.append(mod)
                    mod=[]
                    break
                
            for i in range(len(items)-1):
                self.names.append(MODES[i][1])
            
        #end of redundant code
      
        
        #creating and formatting the plot
        fig, ax = plt.subplots(figsize=(15,7))   
    
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M:%S'))
        ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
        
        ax2ncol=0
        ax1ncol=0
                
        #creating data sets from previously chosen data
        for i in range(1,len(items)):
            inf.seek(0)
            for _ in range(3):
                next(inf)
            y=[]
            x=[]
            for line in reader:
                if (("nie" not in line[items[i]]) and ("NaN" not in line[items[i]]) and float(line[items[i]])>=0):
                    x.append(line[items[0]])
                    y.append(line[items[i]])
                          
            listofy.append(y)
            listofx.append(x)
         
        #creating secondary axis if necessary
        if self.var.get()==1:
           
            ax2 = ax.twinx()
            ax2.set_ylabel("%s" % self.entry2.get())
            ax2.yaxis.tick_right()
            ax2.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M:%S'))
            ax2.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
            ax2.set_prop_cycle(cycler('color', ['c', 'm', 'y', 'k', 'r', 'g', 'b'])+cycler('lw', [1, 2, 3, 4, 5, 6, 7]))
            print(self.names)
            for yno in range(len(listofy)):
                #plotting chosen parameters on the secondary axis
                if d[yno].get()==1:
                    ax2ncol+=1
                    if ax2ncol>3:
                        ax2ncol=3
                    ax2.plot_date(listofx[yno], listofy[yno], linewidth=1, fmt="-.", label="Y2: %s" % self.names[yno])
                    box2=ax2.get_position()
                    ax2.set_position([box2.x0, box2.y0 + box2.height * 0.1,box2.width, box2.height * 0.9])
                    ax2.legend(loc='upper right', bbox_to_anchor=(1.1, -0.2), ncol=ax2ncol)
                    
                else: 
                    ax1ncol+=1
                    if ax1ncol>4:
                        ax1ncol=4
                    
                    ax.plot_date(listofx[yno], listofy[yno], linewidth=0.8, fmt="-", label="Y1: %s" % self.names[yno])
        else:
            #plotting all parameters on primary axis if no secondary axis selected
            for yno in range(len(listofy)):
                ax1ncol+=1
                if ax1ncol>4:
                    ax1ncol=4
               
                ax.plot_date(listofx[yno], listofy[yno], linewidth=0.8, fmt="-", label="Y1: %s" % self.names[yno])
                
        #more plot formatting
        box=ax.get_position()
        

        ax.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9])
        ax.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2), ncol=ax1ncol)
        ax.grid()
        ax.set_ylabel("%s" % self.entry1.get())    
        
        fig.autofmt_xdate()
        
        title=os.path.basename(basename)
        title=os.path.splitext(title)[0]
        plt.title("%s" % title)
        
        #saving the plot
        #filename changes with iteration number during the same runtime
        plt.savefig('%s_graph_%s.png' % (basename,self.filecount), dpi=600)
        self.filecount+=1
        
        plt.close()
        
        #flushing data storage, destroying unnecessary widgets for next run
        listofy=[]
        listofx=[]
        
       
        for i in self.checkbuttons:
            i.destroy()
       
        for i in d:
            i.set=0
            
        self.listbox.destroy()
        self.entry1.destroy()      
        self.entry2.destroy()   
        self.listbox = Listbox(self, selectmode=MULTIPLE)
        del self.names[:]
        del d[:]
        
if __name__ == "__main__":
    
    MyFrame().mainloop()
    
