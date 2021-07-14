import random
from tkinter import *
from functools import partial

s = Tk()
s.title('Torneo di Ping Pong')
width = s.winfo_screenwidth()
height = s.winfo_screenheight()
s.geometry('%dx%d' % (width, height))
tit = Label(s, text='Scrivi il numero di partecipanti al torneo')
tit.grid(row=0,column=1)
n=IntVar()
Entry(s,textvariable=n).grid(row=1,column=1)
Button(s,text='ok',width=20,command=s.destroy).grid(row=2,column=1)
s.mainloop()
N=n.get()

m = Tk()
m.title('Torneo di Ping Pong')
m.geometry('%dx%d' % (width, height))
tit = Label(m, text='Scrivi il nome dei/degli %d giocatori' % N)
tit.grid(row=0,column=1)

entries=[]
for i in range(1,N+1):
    entry=StringVar()
    entries.append(entry)
    Label(m, text='%d' % i).grid(row=i)
    Entry(m,textvariable=entry).grid(row=i,column=1)   
Button(m,text='ok',width=20,command=m.destroy).grid(row=i+1,column=1)
m.mainloop()

players=['']*N
for i in range(N):
    players[i]=entries[i].get()

if N%2==1:
    odd=1
elif N%2==0:
    odd=0

Npartite = int((N-odd)/2)

random.shuffle(players)

def chooseWinners(players,tit=None):
    random.shuffle(players)
    Npartite=len(players)//2
    b=['']*Npartite*2
    WinnersList = list()
    cw = Tk()
    if tit==None:
        if Npartite==8:
            tit='OTTAVI DI FINALE'
        elif Npartite==4:
            tit='QUARTI DI FINALE'
        elif Npartite==2:
            tit='SEMIFINALI'
        elif Npartite==1:
            tit='FINALE'
    cw.title(tit)
    cw.geometry('%dx%d' % (width, height))
    Label(cw,text=tit+': Seleziona i vincitori').grid(row=0,column=1)
    def delete(default):
        del WinnersList[:]
        for j in range(len(b)):
            b[j].configure(highlightbackground=default)
	    b[j].configure(background=default)
    def btn(butidx):
        WinnersList.append(b[butidx].cget('text'))
        b[butidx].configure(highlightbackground='#00ff00')
        b[butidx].configure(background='#00ff00')

    for i in range(Npartite):
        Label(cw,text='Vincitore partita: ').grid(row=i+1,column=0)
        b[i] = Button(cw,text=players[i],command=partial(btn,i))
        b[i].grid(row=i+1,column=1)
        b[i+Npartite] = Button(cw,text=players[i+Npartite],command=partial(btn,i+Npartite))
        b[i+Npartite].grid(row=i+1,column=2)
    defhbg = b[0].cget('highlightbackground')
    Button(cw,text='Cancella',width=10,command=partial(delete,defhbg)).grid(row=i+2,column=1)
    Button(cw,text='Fatto!',width=10,command=cw.destroy).grid(row=i+2,column=2)
    cw.mainloop()
    return WinnersList

if N!=4 and N!=8 and N!=16:
    qf = Tk()
    qf.title('PRIMA FASE')
    qf.geometry('%dx%d' % (width, height))
    Label(qf,text='PRIMA FASE').grid(row=0)
    for i in range(Npartite):
        Label(qf,text='Partita %d: ' %(i+1) +players[i]+' vs '+players[i+Npartite]).grid(row=i+1)
    if odd:
        Label(qf,text='Riposa %s' % players[-1]).grid(row=i+2)
    Button(qf,text='Inizia!',width=20,command=qf.destroy).grid(row=i+3)
    qf.mainloop()

    if N>16 and N<32:
        Npass = 16-Npartite-odd
    elif N>8 and N<16:
        Npass = 8-Npartite-odd
    elif N>4 and N<8:
        Npass = 4-Npartite-odd 

    pfw = Tk()
    pfw.title('PRIMA FASE')
    pfw.geometry('%dx%d' % (width, height))
    Label(pfw,text='PRIMA FASE: Scrivi i punteggi').grid(row=0,column=1)
    res = list()
    entry = ['']*Npartite*2
    for i in range(Npartite):
        entry[i]=IntVar()
        entry[i+Npartite]=IntVar()
        Label(pfw,text=players[i]).grid(row=i+1,column=0)
        Entry(pfw,textvariable=entry[i]).grid(row=i+1,column=1)
        Label(pfw,text=' vs ').grid(row=i+1,column=2)
        Entry(pfw,textvariable=entry[i+Npartite]).grid(row=i+1,column=3)
        Label(pfw,text=players[i+Npartite]).grid(row=i+1,column=4)   
    Button(pfw,text='Fatto!',width=10,command=pfw.destroy).grid(row=i+2,column=2)
    if odd:
        Label(pfw,text='Passano al turno successivo i %d vincitori, i %d perdenti col punteggio più alto e il vincitore dello spareggio' %(Npartite,Npass)).grid(row=i+3,column=2)
    else:
        Label(pfw,text='Passano al turno successivo i %d vincitori e i %d perdenti col punteggio più alto' %(Npartite,Npass)).grid(row=i+3,column=2)
    pfw.mainloop()

    for i in range(Npartite*2):
        res.append(entry[i].get())

    w=list()
    l=list()
    lidx = list()
    for i in range(Npartite):
        if res[i]>res[i+Npartite]:
            w.append(players[i])
            l.append(res[i+Npartite])
            lidx.append(i+Npartite)
        else:
            w.append(players[i+Npartite])
            l.append(res[i])
            lidx.append(i)
    if Npass>0:
        for i in range(Npass):
            BestL = max(l)
            iBestL = l.index(BestL)
            w.append(players[lidx[iBestL]])
            lidx.pop(iBestL)
            l.remove(BestL)
    elif Npass==0:
        BestL=0

    if odd:
        sp1, sp2 = False, False
        if max(l)==BestL:
            sp1 = True
            s = Tk()
            s.title('SPAREGGIO PRELIMINARE')
            s.geometry('%dx%d' % (width, height))
            Label(s,text='SPAREGGIO PRELIMINARE').grid(row=0)
            Label(s,text=players[lidx[l.index(max(l))]]+' vs '+w[-1]).grid(row=1)
            Button(s,text='Inizia!',width=20,command=s.destroy).grid(row=2)
            Label(s,text='Il vincitore passa al turno successivo e il perdente va allo spareggio').grid(row=3)
            s.mainloop()
            WS1 = chooseWinners([players[lidx[l.index(max(l))]],w[-1]],'SPAREGGIO PRELIMINARE')
            LS1 = list(set([players[lidx[l.index(max(l))]],w[-1]])-set(WS1))[0]
            w[-1] = WS1[0]
        elif l.count(max(l))==2:
            sp2 = True
            p1 = players[lidx[l.index(max(l))]]
            lidx.pop(l.index(max(l)))
            l.remove(max(l))
            p2 = players[lidx[l.index(max(l))]]
            s = Tk()
            s.title('SPAREGGIO PRELIMINARE')
            s.geometry('%dx%d' % (width, height))
            Label(s,text='SPAREGGIO PRELIMINARE').grid(row=0)
            Label(s,text=p1+' vs '+p2).grid(row=1)
            Button(s,text='Inizia!',width=20,command=s.destroy).grid(row=2)
            Label(s,text='Il vincitore va allo spareggio e il perdente viene eliminato').grid(row=3)
            s.mainloop()
            WS1 = chooseWinners([p1,p2],'SPAREGGIO PRELIMINARE')
        s = Tk()
        s.title('SPAREGGIO')
        s.geometry('%dx%d' % (width, height))
        Label(s,text='SPAREGGIO').grid(row=0)
        if sp1:
            Label(s,text=LS1+' vs '+players[-1]).grid(row=1)
        elif sp2:
            Label(s,text=WS1[0]+' vs '+players[-1]).grid(row=1)
        else:
            Label(s,text=players[lidx[l.index(max(l))]]+' vs '+players[-1]).grid(row=1)
        Button(s,text='Inizia!',width=20,command=s.destroy).grid(row=2)
        s.mainloop()
        if sp1:
            WS = chooseWinners([LS1,players[-1]],'SPAREGGIO')
        elif sp2:
            WS = chooseWinners([WS1[0],players[-1]],'SPAREGGIO')
        else:
            WS = chooseWinners([players[lidx[l.index(max(l))]],players[-1]],'SPAREGGIO')
        w = w+WS

    if len(w)==16:
        WOct = chooseWinners(w)
        WQrt = chooseWinners(WOct)
        WSemi = chooseWinners(WQrt)
        LSemi = list(set(WQrt)-set(WSemi))
    elif len(w)==8:
        WQrt = chooseWinners(w)
        WSemi = chooseWinners(WQrt)
        LSemi = list(set(WQrt)-set(WSemi))
    elif len(w)==4:
        WSemi = chooseWinners(w)
        LSemi = list(set(w)-set(WSemi))
elif N==16:
    WOct = chooseWinners(players)
    WQrt = chooseWinners(WOct)
    WSemi = chooseWinners(WQrt)
    LSemi = list(set(WQrt)-set(WSemi))
elif N==8: 
    WQrt = chooseWinners(players)
    WSemi = chooseWinners(WQrt)
    LSemi = list(set(WQrt)-set(WSemi))   
elif N==4: 
    WSemi = chooseWinners(players)
    LSemi = list(set(players)-set(WSemi))

WFin = chooseWinners(WSemi)
Wfin = chooseWinners(LSemi,'FINALINA')

e = Tk()
e.title('Classifica finale')
e.geometry('%dx%d' % (width, height))
Label(e,text='1. %s'%str(WFin[0]),fg='red').grid(row=0)
Label(e,text='2. %s'%str(list(set(WSemi)-set(WFin))[0])).grid(row=1)
Label(e,text='3. %s'%str(Wfin[0])).grid(row=2)
Label(e,text='4. %s'%str(list(set(LSemi)-set(Wfin))[0])).grid(row=3)
Button(e,text='Fine',width=20,command=e.destroy).grid(row=4)
e.mainloop()




