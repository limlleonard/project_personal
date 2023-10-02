from tkinter import *
import math
import random
r4=3
class Trigo90():
  def __init__(self,inp=[]):
    self.inp=inp
    self.v1=[]
    self.gd='' #guide
    self.wn=self.sn=0 #winkel / seite nummer
    self.fmessage=['',
    'Alle Eingaben müssen Zahlen sein', #1
    'Alle Zahlen müssen größer als 0 sein',
    'Die Winkel Summe ist kleiner als 180°', #3
    'Bitte genau 2 Zahlen eingeben',
    'Bitte mindestens 1 Seitelänge eingeben', #5
    'Die große Seite ist der große Winkel gegenüber']
  def gen(self):
    if bool(random.getrandbits(1)): #2 Seite sind gegeben
      a1=random.randint(0,2)
      if a1==0: # 2 kathete sind gegeben
        s1=random.randint(2,9)
        s2=random.randint(2,9)
        sl=[s1,s2,float('nan')]
      else: #1 katheter und hypothenose sind gegeben
        while True:
          s1=random.randint(2,9)
          s2=random.randint(2,9)
          if s1!=s2: break
        if a1==1: sl=[min(s1,s2),float('nan'),max(s1,s2)]
        else: sl=[float('nan'),min(s1,s2),max(s1,s2)]
      wl=[float('nan'),float('nan'),math.radians(90)]
    else: #1 Seite und 1 Winkel sind gegeben
      sl=[random.randint(2,9),float('nan'),float('nan')]
      random.shuffle(sl)
      if bool(random.getrandbits(1)):
        wl=[math.radians(random.randint(20,80)),float('nan'),math.radians(90)]
      else: wl=[float('nan'),math.radians(random.randint(20,80)),math.radians(90)]
    self.v1=sl+wl
    return self.v1
  def summe(self,ab,w1,w2): #alpha oder beta
    w3=math.pi-w1-w2
    if ab: self.gd+='α=180°-β-γ='
    else: self.gd+='β=180°-α-γ='
    self.gd+=str(round(math.degrees(w3)))+'°\n'
    return w3
  def satz(self,abc,s1,s2):
    if abc==3:
      s3q=s1**2+s2**2
      s3=s3q**(1/2)
      self.gd+=f'c²=a²+b²={s1}²+{s2}²={round(s3q,r4)}\n'
      self.gd+=f'c={round(s3,r4)}\n'
    else:
      s3q=s2**2-s1**2
      s3=s3q**(1/2)
      if abc==1: #the first side is to be calculated
        self.gd+=f'a²=c²-b²={s2}²-{s1}²={round(s3q,r4)}\n'
        self.gd+=f'a={round(s3,r4)}\n'
      elif abc==2:
        self.gd+=f'b²=c²-a²={s2}²-{s1}²={round(s3q,r4)}\n'
        self.gd+=f'b={round(s3,r4)}\n'
    return s3
  def sinw(self,s1,s2):
    sinw=s1/s2
    w=math.asin(sinw)
    self.gd+=f'sinα=a/c={round(s1,r4)}/{round(s2,r4)}={round(sinw,r4)}\n'
    self.gd+=f'α={round(math.degrees(w))}°\n'
    return w
  def sins(self,abc,s,w):
    if abc==3:
      s2=s*math.sin(w)
      s3=s*math.cos(w)
      self.gd+=f'sinα=a/c\n'
      self.gd+=f'a=c ⸱ sinα={s} ⸱ sin{round(math.degrees(w))}={s} ⸱ {round(math.sin(w),r4)}={round(s2,r4)}\n'
      self.gd+=f'b=c ⸱ cosα={s} ⸱ cos{round(math.degrees(w))}={s} ⸱ {round(math.cos(w),r4)}={round(s3,r4)}\n'
    else:
      s2=s*math.tan(w)
      s3=s/math.cos(w)
      if abc==1:
        self.gd+=f'tanβ=b/a\n'
        self.gd+=f'b=a ⸱ tanα={s} ⸱ tan{round(math.degrees(w))}={s} ⸱ {round(math.tan(w),r4)}={round(s2,r4)}\n'
        self.gd+=f'cosβ=a/c\n'
        self.gd+=f'c=a/cosβ={s}/cos{round(math.degrees(w))}={s}/{round(math.cos(w),r4)}={round(s3,r4)}\n'
      elif abc==2:
        self.gd+=f'tanα=a/b\n'
        self.gd+=f'a=b ⸱ tanα={s} ⸱ tan{round(math.degrees(w))}={s} ⸱ {round(math.tan(w),r4)}={round(s2,r4)}\n'
        self.gd+=f'cosα=b/c\n'
        self.gd+=f'c=b/cosα={s}/cos{round(math.degrees(w))}={s}/{round(math.cos(w),r4)}={round(s3,r4)}\n'
    return s2,s3
  def proof(self):
    for e in self.inp:
      if not len(e): self.v1.append(float('nan'))
      else:
        try:num1=float(e)
        except ValueError: return 1
        if num1<=0: return 2
        self.v1.append(num1)
    if sum([0 if math.isnan(i) else i for i in self.v1[3:]])>=180: return 3
    for i in range(3):
      if not math.isnan(self.v1[i]): self.sn+=1
      if not math.isnan(self.v1[i+3]): self.wn+=1
    if self.sn+self.wn!=3: return 4
    if not self.sn: return 5
    if self.sn==2: #es ist noch überprüfbar in diesem Beispiel
      #aber in ein allgemein Dreieck, nicht
      if math.isnan(self.v1[0]) and self.v1[2]<=self.v1[1] or math.isnan(self.v1[1]) and self.v1[2]<=self.v1[0]:
        return 6
    return 0
  def cal(self):
    a,b,c,alphade,betade,gammade=self.v1
    alpha=math.radians(alphade)
    beta=math.radians(betade)
    gamma=math.radians(gammade)
    if self.sn==1 and self.wn==2:
      if math.isnan(alpha): alpha=self.summe(True,beta,gamma)
      elif math.isnan(beta): beta=self.summe(False,alpha,gamma)
      if not math.isnan(a):
        b,c=self.sins(1,a,beta)
      elif not math.isnan(b):
        a,c=self.sins(2,b,alpha)
      elif not math.isnan(c):
        a,b=self.sins(3,c,alpha)
    elif self.sn==2 and self.wn==1:
      if math.isnan(a): a=self.satz(1,b,c)
      elif math.isnan(b): b=self.satz(2,a,c)
      elif math.isnan(c): c=self.satz(3,a,b)
      alpha=self.sinw(a,c)
      beta=self.summe(False,alpha,gamma)
    else: pass
    self.v1=[a,b,c,alpha,beta,gamma]
  def exe1(self):
    f1=self.proof()
    if not f1: self.cal()
    return self.fmessage[f1],self.gd.split("\n"),self.v1
class App():
  def __init__(self, master):
    self.master = master
    root.geometry('500x500+200+100') #size and initial position
    root.title('Trigonometrie')
    root.option_add('*Font', '30')
    self.v1=[]
    self.fehler=''
    self.gd=[]
    self.step1=0
    self.solved=False
    self.tosolve=False
    tw=6 #text width
    # self.defaultFont = Tk.font.nametofont("TkDefaultFont")
    # self.defaultFont.configure(size=20)
    root.option_add( "*font", "lucida 16" )
    self.f1=Frame(root)
    self.la=Label(self.f1, text="a:").grid(row=0)
    self.ea=Entry(self.f1,width=tw)
    self.ea.grid(row=0,column=1)
    self.lb=Label(self.f1, text="b:").grid(row=0,column=2)
    self.eb=Entry(self.f1,width=tw)
    self.eb.grid(row=0,column=3)
    self.lc=Label(self.f1, text="c:").grid(row=0,column=4)
    self.ec=Entry(self.f1,width=tw)
    self.ec.grid(row=0,column=5)
    self.lal=Label(self.f1, text="α:").grid(row=1)
    self.eal=Entry(self.f1,width=tw)
    self.eal.grid(row=1,column=1)
    self.lbe=Label(self.f1, text="β:").grid(row=1,column=2)
    self.ebe=Entry(self.f1,width=tw)
    self.ebe.grid(row=1,column=3)
    self.lga=Label(self.f1, text="γ:").grid(row=1,column=4)
    self.ega=Entry(self.f1,width=tw)
    self.ega.insert(0,90)
    self.ega.configure(state='disabled')#["state"] = DISABLED
    self.ega.grid(row=1,column=5)
    self.f1.pack()
    self.le=[self.ea,self.eb,self.ec,self.eal,self.ebe,self.ega]#list of entry
    self.f2=Frame(root)
    self.b1=Button(self.f2,text='Neu',command=self.gen)
    self.b1.grid(row=0)
    self.b2=Button(self.f2,text='Lösung',command=self.answer)
    self.b2.grid(row=0,column=2)
    self.b3=Button(self.f2,text='Zurücksetzen',command=self.reset)
    self.b3.grid(row=0,column=3)
    # self.b4=Button(self.f2,text='Test1',command=self.test1)
    # self.b4.grid(row=0,column=4)
    self.f2.pack()
    self.lf=Label(root,text='')
    self.lf.pack()
    self.ea=Text(root, width=24, height=9)
    self.ea.pack()
  def gen(self):
    if not self.tosolve:
      trigo1=Trigo90()
      self.v1=trigo1.gen()
      self.show()
      self.tosolve=True
  def show(self,err='',gd='',en=True): #show result
    if not self.v1:
      for e1 in self.le:
        e1.delete(0,END)
    elif en: #if update entry
      for n1 in range(len(self.le)-1):
        if not len(self.le[n1].get()) and not math.isnan(self.v1[n1]):
          # second condition is used to generate homework
          if n1<3: #side
            self.le[n1].insert(0,round(self.v1[n1],2))
          else:
            self.le[n1].insert(0,round(math.degrees(self.v1[n1])))
    self.lf.config(text = err)
    self.ea.insert(END,gd)
  def answer(self):
    gd1=''
    if not self.solved:
      trigo1=Trigo90([i.get() for i in self.le])
      self.fehler,self.gd,self.v1=trigo1.exe1()
      if self.gd: self.gd.pop() #pop the empty element
      self.solved=True
    if self.gd: gd1=self.gd.pop(0)+'\n'
    if self.fehler:
      self.show(self.fehler,gd1,False)
      self.solved=False
    elif gd1: self.show('Weiter klicken',gd1,False)
    else: self.show('Fertig')
  def reset(self):
    self.v1=[]
    self.lt=[]
    self.solved=self.tosolve=False
    self.step1=0
    self.lf.config(text = '')
    self.show()
    self.ea.delete("1.0","end")
if __name__ == '__main__':
  root = Tk()
  app = App(root)
  def keyp(event): app.answer()
  root.bind("<Return>",keyp)
  root.mainloop()