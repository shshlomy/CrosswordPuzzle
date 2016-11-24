__author__ = 'shepss'
__author__ = 'shepss'


"""
PYTHON 3.1!!!!
TO DO
**********
1.write ? instead of white space inside the word
2. write an android and an ios application for the mobile and send it in milions :-)
2.high lite reolved word with yellow - should change the ListBox to a text widgest
http://www.tkdocs.com/tutorial/text.html

3.Add a clear button which will clear all the text
4..Add index to the query to make it fasternumbers: [] <class 'list'>
content for Find_wordByNum: ckckck
Wordlength1: ()


"""
from tkinter import *
import codecs
import sys
import sqlite3 as lite
import re
import tkinter.messagebox
##python 3.1
con = lite.connect('C:\Python31\DB\excel.db')
#con = lite.connect('C:\Python31\Tashbets_Project\excel.db')

class Application(Frame):
    # search for any word that match e.g seraching moon will retrieve moonlight1
    def Find_wordByNum(self,event):
     self.DB_list=[]
     content=self.word_ent1.get()
     numbers= re.findall('\d+', content)
     print ("numbers:",numbers,type(numbers))
     if len(numbers)==1:
          Wordlength1=int(numbers[0])
     else:
          Wordlength1=()
          for i in numbers:
              Wordlength1+=(int(i),)
     content = ''.join(i for i in content if not i.isdigit())# remove digits
     content=content.strip() #remove white spaces
     print ("content for Find_wordByNum:",content)
     print ("Wordlength1:",Wordlength1)
     with con:
      cur = con.cursor()
      cur.execute("select name,rowid from Data2 where name like ?",("%"+content+"%",))
      rows = cur.fetchall()
      self.show_txt.delete(0,END)
      #self.show_txt.delete(1.0,END)
      if rows==[]:
            tkinter.messagebox.showerror ("!!!לא נמצא מידע!!!", "נסה שנית,לא נמצא מידע")
      elif Wordlength1!=():
         EndOfRows=len(rows)
         Iteration,flag=0,0
         for row in rows:
             Iteration+=1
             if Wordlength1 in self.GetTupple(row[0]):
                 self.DB_list.append(row[1])
                 self.show_txt.insert(END,row[0]+"\n",justify="right")
                 flag=1
             elif Iteration==EndOfRows and flag==0:
                     tkinter.messagebox.showerror ("!!!לא נמצא מידע", "!!!לא נמצא מידע")
                     break
      else:
          for row in rows:
             self.DB_list.append(row[1])
             self.show_txt.insert(END,row[0]+"\n")

    def GetTupple(self,content):
         TupMain=()
         content=content.strip(",")
         AfterSplitShave=[s for s in content.split("=")]
         for s in AfterSplitShave:
             if s.find(" ")!=-1:# is there is more than one word write (1,(3,4))
                 m=s.split(" ")
                 TupSuB=()
                 for i in m:
                     TupSuB+=(len(i),)
                 TupMain+=(TupSuB,)
             else: TupMain+=(len(s),)
         return TupMain


    # search by number of letter e.g. search for H_ouse will bring House
    def Search_ByLetter(self,event):
     content=self.word_ent3.get()
     content=content.replace(" ",".")
     with con:
      cur = con.cursor()
      cur.execute("select name from Data2")
      rows = cur.fetchall()
      self.show_txt.delete(0,END)
      #self.show_txt.delete(1.0,END)
      Flag=0
      for row in rows:
             matchObj = re.search( '(\W|^)'+content+'(\W|$)', row[0], re.M|re.I)
             if matchObj:
                 self.show_txt.insert(END,row[0]+"\n")
                 Flag=1
      if Flag==0:
             tkinter.messagebox.showerror ("לא נמצא מידע!!", "!!!לא נמצא מידע")

    #insert new output to the Database
    def Insert_Output(self,event):
         content=self.word_ent2.get()
         print("content insdie Insert_Output",content)
         with con:
              cur = con.cursor()
              cur.execute("select name from Data2 where name like ?",("%"+content+"%",))
              rows = cur.fetchall()
              if rows==[]:
                  cur.execute("INSERT INTO Data2 VALUES (?)",(content,))
                  con.commit()
                  tkinter.messagebox.showinfo("הידד !!מידע הוכנס בהצלחה", "מידע הוכנס בהצלחה")
              else:
                 tkinter.messagebox.showerror ("!!!מידע כבר קיים", "!!!מידע כבר קיים")

    """this function will update the database with the player data"""
    def set_list(self,event):
     try:
          self.index = self.show_txt.curselection()[0]
          print ("self.index",self.index)
          ModifyText=self.enter1.get()
          print ("ModifyText",ModifyText)
          Rowid=self.DB_list[int(self.index)]
          print ("Rowid",Rowid)
          with con:
              cur = con.cursor()
              cur.execute("update Data2 set name=? where rowid=?",(ModifyText,Rowid))
              con.commit()
              tkinter.messagebox.showinfo("מידע עודכן בהצלחה!!", "מידע עודכן בהצלחה!!")
     except IndexError:
         index = tkinter.END

    def get_list(self,event):
        """function to read the listbox selection and put the result in an entry widget"""
        # get selected line index
        self.index = self.show_txt.curselection()[0]
        print("slef.index",self.index)
        # get the line's text
        self.seltext = self.show_txt.get(self.index)
        # delete previous text in enter1
        self.enter1.delete(0, 5000)
        # now display the selected text
        self.enter1.insert(0, self.seltext)


    def createWidgets(self):
        self.inst_lbl=Label(self,text=":לחיפוש ביטוי כלשהו לחץ חפש")
        self.inst_lbl.grid(row=0,column=1,sticky = E)

        #find a phare
        self.word_ent1=Entry(self)
        self.word_ent1.grid(row=1,column=1,columnspan=8,sticky = E)
        self.word_ent1.bind('<Return>', self.Find_wordByNum)



        self.search_btn=Button(self,text="חפש",command=lambda:self.Find_wordByNum(self,))
        self.search_btn.grid(row=1,column=0,columnspan=4,sticky = E)


        self.inst_lb3=Label(self,text=":לחיפוש מילה מדויקת לחץ חפש")
        self.inst_lb3.grid(row=2,column=1,sticky = E)

        #find exact word or by regexpressino
        self.word_ent3=Entry(self)
        self.word_ent3.grid(row=3,column=1,columnspan=8,sticky = E)
        self.word_ent3.bind('<Return>', self.Search_ByLetter)


        self.search_btn3=Button(self,text="חפש",command=lambda:self.Search_ByLetter(self,))
        self.search_btn3.grid(row=3,column=0,columnspan=4,sticky = E)

        self.inst_lbl=Label(self,text=":להכנסת הגדרה חדשה")
        self.inst_lbl.grid(row=4,column=1,sticky = E)

        # Entry to insert new Data
        self.word_ent2=Entry(self)
        self.word_ent2.grid(row=5,column=1,columnspan=8,sticky = E)
        self.word_ent2.bind('<Return>',self.Insert_Output)

        # button to insert new text
        self.insert_btn=Button(self,text="הכנס",command=lambda:self.Insert_Output(self,))
        self.insert_btn.grid(row=5,column=0,columnspan=2,sticky = E)


        self.Vscrollbar = Scrollbar(root,orient=VERTICAL,bg='Grey')
        self.Hscrollbar = Scrollbar(root,orient=HORIZONTAL,bg='Grey')



        self.show_txt=Listbox(self,width=100,height=30,yscrollcommand=self.Vscrollbar.set,xscrollcommand=self.Hscrollbar.set)
        #self.show_txt=Text(self,width=80,height=30,font=("Arial",12),yscrollcommand=self.Vscrollbar.set,xscrollcommand=self.Hscrollbar.set)
        self.show_txt.grid(row=7,column=0,columnspan=2,sticky = E)
        self.show_txt.bind('<ButtonRelease-1>', self.get_list)
        self.Vscrollbar.config(command=self.show_txt.yview)
        self.Hscrollbar.config(command=self.show_txt.xview)
         #self.show_txt.pack(side=TOP, fill=BOTH, expand=TRUE)
        self.Vscrollbar.pack(side=RIGHT, fill=Y)
        self.Hscrollbar.pack(side=BOTTOM, fill=X)

        self.enter1 = Entry(self, width=70, bg='Grey',font=("Arial",12),justify="right")
        self.enter1.grid(row=6, column=0,columnspan=2,sticky = E)
        self.enter1.insert(66, 'לחץ על שורה בכדי לערוך אותה')
        # pressing the return key will update edited line
        self.enter1.bind('<Return>',self.set_list)
        # or double click left mouse button to update line
        self.enter1.bind('<Double-1>',self.set_list)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.DB_list=[]
        self.pack()
        self.createWidgets()

root = Tk()
root.title("תשבצ-און")
root.geometry("900x700")
app = Application(master=root)

app.mainloop()
root.destroy()
con.close()