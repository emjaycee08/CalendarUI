from tkinter import *
from tkinter import ttk
from tkinter import simpledialog, messagebox
import calendar as cal
import pandas as pd
import datetime as dt
import os


class ChoCal:
    def __init__(self, year=dt.date.today().year,
                 month=dt.date.today().month,
                 ):
        self.year = year
        self.month = month

    def createcal(self):
        cal.setfirstweekday(cal.SUNDAY)
        cm = [cal.monthcalendar(self.year, i + 1) for i in range(12)]
        monthy = self.month - 1
        mo = [i for i in cal.month_name if i != '']
        monthdict = {i: d for i, d in zip(mo, cm)}
        days = cal.weekheader(3).split()
        df = pd.DataFrame(monthdict[mo[monthy]],
                          index=[f'Week {i + 1}' for i in range(len(monthdict[mo[monthy]]))],
                          columns=days)
        df = df.replace(0, '   ')
        df.index.name = f'{mo[monthy]} {self.year}'
        return df

    @staticmethod
    def monrang(year, month):
        return cal.monthrange(year, month)[1]

    @staticmethod
    def mds():
        return cal.mdays[1:]

    @staticmethod
    def caldays(ye: int, mo: int, da: int):
        y = dt.datetime.today().year
        m = dt.datetime.today().month
        d = dt.datetime.today().day
        r = str(dt.date(ye, mo, da) - dt.date(y, m, d))[:-9]
        if r:
            return r


class CalGui:
    RUN = False
    TOP = None

    def __init__(self, root=Tk()):
        self.root = root
        self.sd = []
        self.rdr = []
        self.txfile = ''
        self.root.geometry("1200x700")
        self.root.overrideredirect(False)
        self.root.resizable(False,False)
        self.root.config(background='#3C6255')
        self.root.bind_all('<Control-Left>', self.mtc)
        self.root.bind_all('<Control-Right>', self.mtc)
        self.root.bind_all('<Shift-Left>', self.dtc)
        self.root.bind_all('<Shift-Right>', self.dtc)
        self.root.bind_all('<Alt-Left>', self.yrc)
        self.root.bind_all('<Alt-Right>', self.yrc)
        self.root.bind_all('<Control-i>', self.resapp)
        self.bt = {}
        # slider for year
        self.sc1 = Scale(self.root, from_=1950, to=2080, orient=HORIZONTAL,
                         command=self.ccal, background='#3C6255', fg='white',
                         font='verdana 8 bold')
        self.sc1.set(dt.datetime.today().year)
        self.sc1.pack(pady=3, padx=3, fill='both')
        self.bt['sc1'] = self.sc1
        # slider for months
        self.sc2 = Scale(self.root, from_=1, to=12, orient=HORIZONTAL,
                         command=self.ccal, background='#3C6255', fg='white',
                         font='verdana 8 bold')
        self.sc2.set(dt.datetime.today().month)
        self.sc2.pack(pady=2, padx=2, fill='both')
        self.bt['sc2'] = self.sc2
        # slider for days
        self.sc3 = Scale(self.root, from_=1, to=31, orient=HORIZONTAL,
                         command=self.ccal, background='#3C6255', fg='white',
                         font='verdana 8 bold')
        self.sc3.set(dt.datetime.today().day)
        self.sc3.pack(pady=3, padx=3, fill='both')
        self.bt['sc3'] = self.sc3
        # showing the calendar
        self.text = Text(self.root, font='consolas 25 bold', height=7, background='#EAE7B1',
                         foreground='#61876E', relief=SUNKEN, pady = 50)
        self.text.tag_add('bd', '1.0', END)
        self.text.tag_config('bd', justify='center')
        self.text.tag_config('thg', background='dark orange', foreground='black')
        self.text.tag_config('hg', background='dark slate blue', foreground='white')
        self.text.pack(pady=20, fill='x')
        self.bt['text'] = self.text

        self.gset = IntVar()
        self.lvar = StringVar()
        # for position of date today
        self.label = ttk.Label(self.root, textvariable=self.lvar, background='#3C6255', foreground='white')
        self.label.pack(pady=2)
        # for position of buttons
        self.frb = ttk.Frame(self.root)
        self.frb.pack(side=BOTTOM, pady=25)
        # current date button
        self.stb = Button(self.frb, text='Current Date/Set', command=self.sdat,
                          bg='#3C6255', fg='white', activebackground='green',
                          activeforeground='white', highlightthickness=0, bd=0, font='verdana 10 bold')
        self.stb.bind_all('<Control-c>', self.sdat)
        self.stb.pack(side=LEFT, padx=(0, 2))
        self.bt['stb'] = (self.stb, '<Control-c>', self.sdat)
        # calculate button
        self.cdb = Button(self.frb, text='Calculate', command=self.calcd,
                          bg='#3C6255', fg='white', activebackground='green',
                          activeforeground='white', highlightthickness=0, bd=0, font='verdana 10 bold')
        self.cdb.bind_all('<Control-equal>', self.calcd)
        self.cdb.pack(side=LEFT, padx=(0, 2))
        self.bt['cdb'] = (self.cdb, '<Control-equal>', self.calcd)
        # highlight color button
        self.hcbb = Button(self.frb, text='Highlight Color', command=self.colorh,
                           bg='#3C6255', fg='white', activebackground='green',
                           activeforeground='white', highlightthickness=0, bd=0, font='verdana 10 bold')
        self.hcbb.bind_all('<Control-h>', self.colorh)
        self.hcbb.pack(side=LEFT, padx=(0, 2))
        self.bt['hcbb'] = (self.hcbb, '<Control-h>', self.colorh)
        # bg color button
        self.clbcb = Button(self.frb, text='Background Color', command=self.calbg,
                            bg='#3C6255', fg='white', activebackground='green',
                            activeforeground='white', highlightthickness=0, bd=0, font='verdana 10 bold')
        self.clbcb.bind_all('<Control-b>', self.calbg)
        self.clbcb.pack(side=LEFT, padx=(0, 2))
        self.bt['clbcb'] = (self.clbcb, '<Control-b>', self.calbg)
        # save color button
        self.setb = Button(self.frb, text='Saving Colors', command=self.savs,
                           bg='#3C6255', fg='white', activebackground='green',
                           activeforeground='white', highlightthickness=0, bd=0, font='verdana 10 bold')
        self.setb.bind_all('<Control-s>', self.savs)
        self.setb.pack(side=LEFT, padx=(0, 2))
        self.bt['setb'] = (self.setb, '<Control-s>', self.savs)
        # set default theme button
        self.setd = Button(self.frb, text='Setting Default Theme', command=self.setcor,
                           bg='#3C6255', fg='white', activebackground='green',
                           activeforeground='white', highlightthickness=0, bd=0, font='verdana 10 bold')
        self.setd.bind_all('<Control-d>', self.setcor)
        self.setd.pack(side=LEFT, padx=(0, 2))
        self.bt['setd'] = (self.setd, '<Control-d>', self.setcor)
        # close button
        self.but = Button(self.frb, text='Close', command=self.root.destroy,
                          bg='#3C6255', fg='white', activebackground='black',
                          activeforeground='white', highlightthickness=0, bd=0, font='verdana 10 bold')
        self.but.pack(side=LEFT)
        self.bt['but'] = self.but

        if 'Calset' in os.listdir():
            orpa = os.path.join(os.getcwd(), 'Calset')
            if 'setnext.txt' in os.listdir(orpa):
                with open(os.path.join(orpa, 'setnext.txt')) as setfile:
                    sf = eval(setfile.read())
                self.text.tag_config('hg', background=sf[0],
                                     foreground=sf[1])
                self.label.config(foreground=sf[2])
                self.text.config(background=sf[3], foreground=sf[4])

    def resapp(self, event=None):
        if self.root.overrideredirect():
            self.text.config(font='consolas 34 bold')
            self.frb.pack(side=TOP, pady=5)
            self.root.overrideredirect(False)
            self.root.resizable(True, True)
            a = str(self.root.winfo_geometry())
            h = int(a.partition('x')[2].partition('+')[0])
            w = int(a.partition('x')[0])
            self.root.minsize(w, h)
            del a, h, w
        else:
            self.text.config(font='consolas 37 bold')
            self.frb.pack(pady=25)
            self.root.update()
            self.root.overrideredirect(True)
            self.root.state('zoomed')

    def dtc(self, event=None):
        # Moving the scale of the day.

        if event.keysym == 'Right':
            ad = self.sc3.get() + 1
            self.sc3.set(ad)
        else:
            ad = self.sc3.get() - 1
            self.sc3.set(ad)

    def mtc(self, event=None):
        # Moving the scale of the month.

        if event.keysym == 'Right':
            ad = self.sc2.get() + 1
            self.sc2.set(ad)
        else:
            ad = self.sc2.get() - 1
            self.sc2.set(ad)

    def yrc(self, event=None):
        # Moving the scale of the year.

        if event.keysym == 'Right':
            ad = self.sc1.get() + 1
            self.sc1.set(ad)
        else:
            ad = self.sc1.get() - 1
            self.sc1.set(ad)

    def ccal(self, event=None):
        # Creating Calendar according to the scales of the years, months and days.

        self.label.config(font='verdana 30 bold')
        cc = ChoCal(self.sc1.get(), self.sc2.get())
        self.sc3.config(to=cc.monrang(self.sc1.get(), self.sc2.get()))
        self.text.config(state='normal')
        self.text.delete('1.0', END)
        self.text.insert(END, cc.createcal(), 'bd')
        self.tdcol()
        sch1 = self.text.search(str(self.sc3.get()), '3.6', END)
        sch2 = f'{sch1}+{len(str(self.sc3.get()))}c'
        gt = self.text.get(sch1, sch2)
        self.text.delete(sch1, sch2)
        self.text.insert(sch1, gt, ('hg'))
        self.text.config(state='disabled')
        if self.cald():
            self.lvar.set(self.cald())
        else:
            self.tn()

    def tdcol(self):
        # Highlight Color of today's date.

        if self.sc2.get() == dt.date.today().month and self.sc1.get() == dt.date.today().year:
            sch1 = self.text.search(str(dt.datetime.today().day), '3.6', END)
            sch2 = f'{sch1}+{len(str(dt.datetime.today().day))}c'
            gt = self.text.get(sch1, sch2)
            self.text.delete(sch1, sch2)
            self.text.insert(sch1, gt, ('thg'))

    def cald(self, event=None):
        # Calculation between two dates for how many days left.

        if self.sd:
            c = str(dt.date(self.sc1.get(),
                            self.sc2.get(), self.sc3.get()) - dt.date(self.sd[0],
                                                                      self.sd[1], self.sd[2]))[:-9]
            if c:
                f, _ = c.split()
                if int(f) < 0:
                    return f'The range are {c}, before this day {dt.date(self.sd[0], self.sd[1], self.sd[2])}'
                elif int(f) > 0:
                    return f'The range are {c}, after this day {dt.date(self.sd[0], self.sd[1], self.sd[2])}'
        else:
            c = ChoCal.caldays(self.sc1.get(), self.sc2.get(), self.sc3.get())
            if c:
                f, _ = c.split()
                if int(f) < 0:
                    return f'{c} have passed to today {dt.date.isoformat(dt.datetime.today())}'
                elif int(f) > 0:
                    return f'{c} to go from today {dt.date.isoformat(dt.datetime.today())}'

    def tn(self):
        # Running the seconds display and colored them.

        import random
        if CalGui.RUN:
            colors = [str(i) for i in range(10)] + ['a', 'b', 'c', 'd', 'e', 'f']
            ctk = '#'
            if self.cald() == None:
                for i in range(6):
                    ctk += ''.join(random.choice(colors))
                self.label.config(foreground=ctk)
                self.lvar.set(f'Today is {str(dt.datetime.today())[:-7]}')
                self.root.after(1000, self.tn)
        else:
            if self.cald() == None:
                self.lvar.set(f'Today is {str(dt.datetime.today())[:-7]}')
                self.root.after(1000, self.tn)

    def scald(self, event=None):
        # Setting year, month and day as default on set date check button.

        self.label.config(font='verdana 30 bold')
        self.label.pack(pady=7)
        if self.gset.get():
            self.sd.clear()
            self.sd.extend((self.sc1.get(), self.sc2.get(), self.sc3.get()))
            if self.cald():
                self.lvar.set(self.cald())
            else:
                self.tn()
        else:
            self.sd.clear()
            if self.cald():
                self.lvar.set(self.cald())
            else:
                self.tn()

    def sdat(self, event=None):
        # Set the scale to default values of year, month and day.

        if self.gset.get():
            self.sc1.set(self.sd[0])
            self.sc2.set(self.sd[1])
            self.sc3.set(self.sd[2])
        else:
            self.sc1.set(dt.date.today().year)
            self.sc2.set(dt.date.today().month)
            self.sc3.set(dt.date.today().day)


    def calcd(self, event=None):
        # Calculate the days left that represent years, months, weeks, and days.

        if CalGui.SELF:
            CalGui.SELF = False
            self.label.config(font='verdana 27 bold')
            self.label.pack(pady=9)
            if self.sd:
                de = dt.date(self.sc1.get(),
                             self.sc2.get(), self.sc3.get()) - dt.date(self.sd[0],
                                                                       self.sd[1], self.sd[2])
            else:
                de = dt.date(self.sc1.get(), self.sc2.get(), self.sc3.get()) - dt.date.today()
            td = de.days
            pt = {365: 0, 30: 0, 7: 0, 1: 0}
            for i in pt:
                if td // i:
                    pt[i] = td // i
                    td = td - (i * pt[i])
            td = sum([k * l for k, l in pt.items()])

            if td:
                nt = ['years', 'months', 'weeks', 'days']
                tm = list(pt)
                pt = {nt[i]: pt[tm[i]] for i in range(4) if pt[tm[i]]}
                if td >= 7 or td < -1:
                    sent = f"{td} days left and equal to: "
                    for i, j in pt.items():
                        if j > 1 or j < -1:
                            sent += ''.join(f'{j} {i}, ')
                        else:
                            sent += ''.join(f'{j} {str(i)[:-1]}, ')
                    self.lvar.set(sent[:-2] + '.')
                else:
                    if td > 1:
                        self.lvar.set(f"{td} days left.")
                    else:
                        self.lvar.set(f"{td} day left.")
            else:
                CalGui.SELF = True
                self.label.config(font='verdana 30 bold')
                self.label.pack(pady=7)
                messagebox.showinfo('T-Tech Calendar', 'No days left!')

        else:
            CalGui.SELF = True
            self.label.config(font='verdana 30 bold')
            self.label.pack(pady=7)
            self.lvar.set(self.cald())

    def colorh(self, event=None):
        # Changing color on the highlight and the foreground.

        from CreateColors import create_colors as cco

        if not CalGui.TOP:
            if not 'tkcols.txt' in os.listdir():
                cco()
                with open('tkcols.txt') as cols:
                    lc = eval(cols.read())
            else:
                with open('tkcols.txt') as cols:
                    lc = eval(cols.read())

            def high(event=None):
                try:
                    if not rt1.get():
                        spb.configure(background=lc[lc.index(spb.get())])
                        self.text.tag_config('hg', background=lc[lc.index(spb.get())])
                    else:
                        spb.configure(foreground=lc[lc.index(spb.get())])
                        self.text.tag_config('hg', foreground=lc[lc.index(spb.get())])
                except:
                    pass

            def chc(event=None):
                CalGui.TOP = None
                cco()
                tl.unbind_all("<q>")
                tl.unbind_all("<Q>")
                tl.unbind_all('<f>')
                tl.unbind_all('<Control-t>')
                tl.unbind_all('<Control-g>')
                for i in self.bt:
                    if isinstance(self.bt[i], tuple):
                        self.bt[i][0].config(state='normal')
                        self.bt[i][0].bind_all(self.bt[i][1], self.bt[i][2])
                    else:
                        if i != 'text':
                            self.bt[i].config(state='normal')
                tl.destroy()

            def fcs(event=None):
                if event.keysym == 'f':
                    spb.focus()
                elif event.keysym == 't':
                    rt1.set(False)
                elif event.keysym == 'g':
                    rt1.set(True)

            for i in self.bt:
                if isinstance(self.bt[i], tuple):
                    self.bt[i][0].config(state='disable')
                    self.bt[i][0].unbind_all(self.bt[i][1])
                else:
                    self.bt[i].config(state='disable')
            tl = Toplevel()
            tl.resizable(False, False)
            tl.wm_attributes("-topmost", 1)
            tl.title('Color Highlight')
            tl.overrideredirect(True)
            tl.bind_all("<q>", chc)
            tl.bind_all("<Q>", chc)
            tl.bind_all('<f>', fcs)
            tl.bind_all('<Control-t>', fcs)
            tl.bind_all('<Control-g>', fcs)
            spb = Spinbox(tl, command=high, values=lc, font='Helvetica 20 bold')
            spb.pack(side=LEFT, padx=5)
            rt1 = BooleanVar()
            rbt1 = ttk.Radiobutton(tl, text='H', variable=rt1, value=False)
            rbt2 = ttk.Radiobutton(tl, text='F', variable=rt1, value=True)
            rbt1.pack(pady=2, padx=5)
            rbt2.pack(pady=2, padx=5)
            CalGui.TOP = tl
            spb.focus_set()

    def calbg(self, event=None):
        # Changing colors for the Calendar background and foreground(the text).

        from CreateColors import create_colors as cco

        if not CalGui.TOP:
            if not 'tkcols.txt' in os.listdir():
                cco()
                with open('tkcols.txt') as cols:
                    lc = eval(cols.read())
            else:
                with open('tkcols.txt') as cols:
                    lc = eval(cols.read())

            def clc(event=None):
                try:
                    if not rt2.get():
                        spb2.configure(background=lc[lc.index(spb2.get())])
                        self.text.config(background=lc[lc.index(spb2.get())])
                    else:
                        spb2.configure(foreground=lc[lc.index(spb2.get())])
                        self.text.configure(foreground=lc[lc.index(spb2.get())])
                except:
                    pass

            def chc(event=None):
                CalGui.TOP = None
                cco()
                tl.unbind_all("<q>")
                tl.unbind_all("<Q>")
                tl.unbind_all('<f>')
                tl.unbind_all('<Control-t>')
                tl.unbind_all('<Control-g>')
                tl.grab_release()
                for i in self.bt:
                    if isinstance(self.bt[i], tuple):
                        self.bt[i][0].config(state='normal')
                        self.bt[i][0].bind_all(self.bt[i][1], self.bt[i][2])
                    else:
                        if i != 'text':
                            self.bt[i].config(state='normal')
                tl.destroy()

            def fcs(event=None):
                if event.keysym == 'f':
                    spb2.focus()
                elif event.keysym == 't':
                    rt2.set(False)
                elif event.keysym == 'g':
                    rt2.set(True)

            for i in self.bt:
                if isinstance(self.bt[i], tuple):
                    self.bt[i][0].config(state='disable')
                    self.bt[i][0].unbind_all(self.bt[i][1])
                else:
                    self.bt[i].config(state='disable')
            tl = Toplevel()
            tl.resizable(False, False)
            tl.wm_attributes("-topmost", 1)
            tl.title('Color Background')
            tl.overrideredirect(True)
            tl.bind_all("<q>", chc)
            tl.bind_all("<Q>", chc)
            tl.bind_all('<f>', fcs)
            tl.bind_all('<Control-t>', fcs)
            tl.bind_all('<Control-g>', fcs)
            spb2 = Spinbox(tl, values=lc, command=clc, font='Helvetica 20 bold')
            spb2.pack(side=LEFT, padx=5)
            rt2 = BooleanVar()
            cbr1 = ttk.Radiobutton(tl, text='B', variable=rt2, value=False)
            cbr2 = ttk.Radiobutton(tl, text='F', variable=rt2, value=True)
            cbr1.pack(pady=2, padx=5)
            cbr2.pack(pady=2, padx=5)
            CalGui.TOP = tl
            spb2.focus_set()

    def savs(self, event=None):
        # Saving the color theme that has been set.

        import json

        dirc = os.getcwd()
        if 'Calset' in os.listdir():
            os.chdir('Calset')
        else:
            os.mkdir('Calset')
            os.chdir('Calset')
        ask = messagebox.askyesno('T-Tech Calendar', 'Save setting color?')
        if ask:
            if 'stc.txt' in os.listdir():
                ask = messagebox.askyesno('T-Tech Calendar', 'Adding more setting?')
                if ask:
                    std = {}
                    with open('stc.txt') as sett:
                        gj = json.load(sett)
                        std = {'Highlight': self.text.tag_cget("hg", "background"),
                               'Foreground': self.text.tag_cget("hg", "foreground"),
                               'Label': str(self.label.cget('foreground')),
                               'CB': str(self.text.cget('background')),
                               'CF': str(self.text.cget('foreground'))
                               }
                        gj['stc'].append(std)
                    with open('stc.txt', 'w') as sett:
                        json.dump(gj, sett)
                    os.chdir(dirc)

                else:
                    os.chdir(dirc)
                    messagebox.showinfo('T-Tech Calendar', 'Saving setting aborted!')
            else:
                std = {}
                with open('stc.txt', 'w') as sett:
                    std['stc'] = []
                    std['stc'].append({'Highlight': self.text.tag_cget("hg", "background"),
                                       'Foreground': self.text.tag_cget("hg", "foreground"),
                                       'Label': str(self.label.cget('foreground')),
                                       'CB': str(self.text.cget('background')),
                                       'CF': str(self.text.cget('foreground'))
                                       })
                    json.dump(std, sett)
                os.chdir(dirc)
        else:
            if 'stc.txt' in os.listdir():
                with open('stc.txt') as sett:
                    gj = json.load(sett)

                def cbf(event=None):
                    cbbx.focus_set()

                def chosensett(event=None):
                    rw = int(ev.get()[:ev.get().find(':')])
                    with open('stc.txt') as sett:
                        rd = json.load(sett)
                    std = rd['stc'][rw]
                    for i in self.bt:
                        if isinstance(self.bt[i], tuple):
                            self.bt[i][0].config(state='normal')
                            self.bt[i][0].bind_all(self.bt[i][1], self.bt[i][2])
                        else:
                            if i != 'text':
                                self.bt[i].config(state='normal')
                    self.text.tag_config('hg', background=std['Highlight'],
                                         foreground=std['Foreground'])
                    self.text.config(background=std['CB'], foreground=std['CF'])
                    self.label.config(foreground=std['Label'])
                    for i in self.bt:
                        if isinstance(self.bt[i], tuple):
                            self.bt[i][0].config(state='disable')
                            self.bt[i][0].unbind_all(self.bt[i][1])
                        else:
                            self.bt[i].config(state='disable')
                    hback = self.text.tag_cget("hg", "background")
                    hfore = self.text.tag_cget("hg", "foreground")
                    labc = self.label.cget("foreground")
                    cback = self.text.cget("background")
                    cfore = self.text.cget("foreground")
                    messagebox.showinfo('Info setting Now',
                                        f'Highlight: {hback}\nForeground: {hfore}\nLabel Color: {labc}\nCalBackground: {cback}\nCalForeground: {cfore}')

                def delsett(event=None):
                    rw = int(ev.get()[:ev.get().find(':')])
                    with open('stc.txt') as sett:
                        rd = json.load(sett)
                    if len(rd['stc']) > 1:
                        del rd['stc'][rw]
                        with open('stc.txt', 'w') as sett:
                            json.dump(rd, sett)
                        cbbx.config(state='normal')
                        cbbx.delete(0, END)
                        cbbx['values'] = [f'{i}: {rd["stc"][i]}' for i in range(len(rd['stc']))]
                        cbbx.current(0)
                        cbbx.config(state='readonly')
                    else:
                        os.remove('stc.txt')
                        chc()

                def chc(event=None):
                    CalGui.TOP = None
                    tl.unbind_all("<q>")
                    tl.unbind_all("<Q>")
                    tl.unbind_all('<f>')
                    tl.unbind_all('<c>')
                    tl.unbind_all('<d>')
                    for i in self.bt:
                        if isinstance(self.bt[i], tuple):
                            self.bt[i][0].config(state='normal')
                            self.bt[i][0].bind_all(self.bt[i][1], self.bt[i][2])
                        else:
                            if i != 'text':
                                self.bt[i].config(state='normal')
                    os.chdir(dirc)
                    tl.destroy()

                for i in self.bt:
                    if isinstance(self.bt[i], tuple):
                        self.bt[i][0].config(state='disable')
                        self.bt[i][0].unbind_all(self.bt[i][1])
                    else:
                        self.bt[i].config(state='disable')

                tl = Toplevel()
                tl.resizable(False, False)
                tl.wm_attributes("-topmost", 1)
                tl.title('Choose Event')
                tl.overrideredirect(True)
                tl.bind_all("<q>", chc)
                tl.bind_all("<Q>", chc)
                tl.bind_all('<c>', chosensett)
                tl.bind_all('<d>', delsett)
                label = Label(tl, text='Please select recorded Setting')
                label.pack(pady=5)
                ev = StringVar()
                cbbx = ttk.Combobox(tl, textvariable=ev, font='Helvetica 12 bold')
                cbbx['values'] = [f'{i}: {gj["stc"][i]}' for i in range(len(gj['stc']))]
                cbbx.current(0)
                cbbx.config(state='readonly')
                cbbx.pack(padx=5)
                tl.bind_all('<f>', cbf)
                fr = Frame(tl)
                fr.pack()
                butcho = Button(fr, text='Select setting', command=chosensett)
                butcho.pack(side=LEFT, pady=5)
                buteve = Button(fr, text='Delete setting', command=delsett)
                buteve.pack(side=RIGHT, pady=5)
                CalGui.TOP = tl
                cbbx.focus_set()
            else:
                messagebox.showinfo('T-Tech Calendar', 'No colors saved yet!')
                os.chdir(dirc)

    def setcor(self, event=None):
        # Setting the theme colors as default.

        dirc = os.getcwd()
        if 'Calset' in os.listdir():
            os.chdir('Calset')
        else:
            os.mkdir('Calset')
            os.chdir('Calset')
        if 'setnext.txt' in os.listdir():
            ask = messagebox.askyesno('T-Tech Calendar', '"Yes" Delete theme setting, "No" Save existing theme')
            if ask:
                os.remove('setnext.txt')
                messagebox.showinfo('T-Tech Calendar', 'The setting back to original')
            else:
                tak = [self.text.tag_cget("hg", "background"),
                       self.text.tag_cget("hg", "foreground"),
                       str(self.label.cget("foreground")),
                       str(self.text.cget("background")),
                       str(self.text.cget("foreground")),
                       ]
                tak = {i: j for i, j in enumerate(tak)}
                with open('setnext.txt', 'w') as stf:
                    stf.write(str(tak))
                messagebox.showinfo('T-Tech Calendar', 'This theme will be set as default theme!')
        else:
            tak = [self.text.tag_cget("hg", "background"),
                   self.text.tag_cget("hg", "foreground"),
                   str(self.label.cget("foreground")),
                   str(self.text.cget("background")),
                   str(self.text.cget("foreground")),
                   ]
            tak = {i: j for i, j in enumerate(tak)}
            with open('setnext.txt', 'w') as stf:
                stf.write(str(tak))
            messagebox.showinfo('T-Tech Calendar', 'This theme will be set as default theme!')
        os.chdir(dirc)


def main():
    # Starting the app.

    pth = None
    if 'CalGui.ico' in os.listdir():
        pth = f'{os.getcwd()}\\CalGui.ico'
    if 'Caldata' in os.listdir():
        os.chdir('Caldata')
    else:
        os.mkdir('Caldata')
        os.chdir('Caldata')
    start = CalGui()
    if pth:
        start.root.iconbitmap(default=pth)
    start.root.title('T-Tech Calendar')
    start.root.mainloop()


if __name__ == "__main__":
    main()