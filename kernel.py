import numpy as np

import operatori as o
import formule as f


class problema:

    def __init__(self, dati, incognite):

        self.Mu = f.moto_rett_unif()
        self.Ma = f.moto_unif_acc()
        self.D = f.dinamica()
        self.P=f.piano_inclinato()

        self.teorie = [ self.Ma, self.D, self.P] #self.Mu,

        self.dati=dati
        self.incognite=incognite

        self.soluzioni=[]

    def imposta(self):
        for t in self.teorie:
            for v in t.var:
                for d in self.dati:
                    if v.nome == d.nome:
                        v.valore = d.valore

        self.leggi = []

        self.Mu.legge_oraria()
        self.Ma.legge_oraria()
        self.Ma.legge_velocita()
        self.Ma.legge_velocita_spazio()
        self.D.legge_Newton()
        self.P.componente_x()
        self.P.componente_y()

        self.leggi=[ self.Ma.l_o, self.Ma.l_v,self.Ma.l_v_x, self.D.l_N, self.P.c_x, self.P.c_y] #self.Mu.l_o,

        '''
        for v in self.Ma.l_o.var:
            print('l_o ', v.nome)

        for v in self.D.l_N.var:
            print('l_N ', v.nome)
        '''

        return self.leggi

    def risolvi(self):
        if len(self.incognite) == 0:
            return
        e = self.trova_soluzioni()
        if e==1:
            self.risolvi()
        '''e = 1
        while e == 1:
             #for i in range(len(self.dati)):
             #   print(self.dati[i].nome, self.dati[i].valore)

             e = self.trova_soluzioni()'''
        if len(self.incognite)==0:
            return
        else:
            d=self.trova_soluzioni_2()
            if d==1:
                self.risolvi()

        for i in self.incognite:
            print('incognita ' + i.nome + 'non trovata')

    def trova_soluzioni_2(self):
        nomi_dati = []
        nomi_incognite=[]
        for d in self.dati:
            nomi_dati.append(d.nome)
        for i in self.incognite:
            nomi_incognite.append(i.nome)
        self.imposta()
        print('giroooo doppiooo')
        # nuovi_dati = []
        # incognite_trovate = []
        controllo = 0

        coppie = []

        n = len(self.incognite)
        for i in range(n):
            for j in range(i + 1, n):
                coppie.append([self.incognite[i], self.incognite[j]])
        nomi_nuove_incognite=[]
        for incognita in self.incognite:
            for legge in self.leggi:
                nomi=[]
                for j in legge.var:
                    nomi.append(j.nome)
                if incognita.nome in nomi:
                    for h in legge.var:
                        if not ((h.nome == incognita.nome) or (h.nome=='costante')):
                            print(h.nome)
                            if not ((h.nome in nomi_dati) or (h.nome in nomi_incognite) or (h.nome in nomi_nuove_incognite) ):
                                nomi_nuove_incognite.append(h.nome)
                                coppie.append([incognita,h])

        for coppia in coppie:
            i1 = coppia[0]
            i2 = coppia[1]

            print('cerco ' + i1.nome + ' e ' + i2.nome)
            c1 = 0
            possibili_leggi = []
            for l in self.leggi:
                nomi = []
                for j in l.var:
                    nomi.append(j.nome)

                if (i1.nome in nomi) and (i2.nome in nomi):
                    for variabile in l.var:
                        if variabile.nome == i1.nome:
                            v1 = variabile
                        if variabile.nome == i2.nome:
                            v2 = variabile
                    if l.grado(v1) == 1 and l.grado(v2) == 1:
                        c1m1 = l.m1.coefficiente(v1)
                        c1m2 = l.m2.coefficiente(v1)
                        c2m1 = l.m1.coefficiente(v2)
                        c2m2 = l.m2.coefficiente(v2)
                        var1 = c1m1.variabili()
                        var1.extend(c1m2.variabili())
                        var2 = c2m1.variabili()
                        var2.extend(c2m2.variabili())
                        if not ((v1 in var2) or (v2 in var1)):
                            nomi.remove(i1.nome)
                            nomi.remove(i2.nome)
                            for j in nomi:
                                if j == 'costante':
                                    nomi.remove(j)
                            if all(n in nomi_dati for n in nomi):
                                possibili_leggi.append(l)
                elif len(possibili_leggi)>0:
                    if i1.nome in nomi :
                        for variabile in l.var:
                            if variabile.nome == i1.nome:
                                v1 = variabile
                        if l.grado(v1) == 1:
                            nomi.remove(i1.nome)
                            for j in nomi:
                                if j == 'costante':
                                    nomi.remove(j)
                            if all(n in nomi_dati for n in nomi):
                                possibili_leggi.append(l)
                    if i2.nome in nomi :
                        for variabile in l.var:
                            if variabile.nome == i2.nome:
                                v1 = variabile
                        if l.grado(v1) == 1:
                            nomi.remove(i2.nome)
                            for j in nomi:
                                if j == 'costante':
                                    nomi.remove(j)
                            if all(n in nomi_dati for n in nomi):
                                possibili_leggi.append(l)

            if len(possibili_leggi) > 1:
                controllo = 1
                print(possibili_leggi[0].nome, possibili_leggi[1].nome)
                sol1, sol2 = o.sistema_2x2(possibili_leggi[0], possibili_leggi[1], i1, i2).soluzione()

                print(possibili_leggi[1].m2.nome, possibili_leggi[1].m2.valore)
                i1.valore = sol1.valore
                i2.valore = sol2.valore
                if i1 in self.incognite:
                    self.incognite.remove(i1)
                    self.soluzioni.append(sol1)
                if i2 in self.incognite:
                    self.incognite.remove(i2)
                    self.soluzioni.append(sol2)
                self.dati.extend([i1, i2])
                return controllo
        return controllo

    '''def trova_soluzioni_2_old(self):#non considera le eventuali incognite sottointese
        nomi_dati=[]
        for d in self.dati:
            nomi_dati.append(d.nome)
        self.imposta()
        print('giroooo doppiooo')
        #nuovi_dati = []
        #incognite_trovate = []
        controllo=0

        coppie=[]
        n=len(self.incognite)
        for i in range(n):
            for j in range(i+1,n):
                coppie.append([self.incognite[i],self.incognite[j]])

        for coppia in coppie:
            i1=coppia[0]
            i2=coppia[1]

            print('cerco ' + i1.nome + ' e ' + i2.nome)
            c1 = 0
            possibili_leggi=[]
            for l in self.leggi:
                nomi=[]
                for j in l.var:
                    nomi.append(j.nome)

                if (i1.nome in nomi) and (i2.nome in nomi):
                    for variabile in l.var:
                        if variabile.nome == i1.nome:
                            v1=variabile
                        if variabile.nome == i2.nome:
                            v2=variabile
                    if l.grado(v1) == 1 and l.grado(v2) == 1:
                        c1m1 =l.m1.coefficiente(v1)
                        c1m2 = l.m2.coefficiente(v1)
                        c2m1 = l.m1.coefficiente(v2)
                        c2m2 = l.m2.coefficiente(v2)
                        var1=c1m1.variabili()
                        var1.extend(c1m2.variabili())
                        var2=c2m1.variabili()
                        var2.extend(c2m2.variabili())
                        if not ((v1 in var2) or (v2 in var1)):
                            nomi.remove(i1.nome)
                            nomi.remove(i2.nome)
                            for j in nomi:
                                if j == 'costante':
                                    nomi.remove(j)
                            if all(n in nomi_dati for n in nomi):
                                possibili_leggi.append(l)

            if len(possibili_leggi)>1:
                controllo=1
                sol1,sol2=o.sistema_2x2(possibili_leggi[0], possibili_leggi[1], i1, i2).soluzione()
                self.soluzioni.extend([sol1,sol2])
                i1.valore=sol1.valore
                i2.valore=sol2.valore
                self.incognite.remove(i1)
                self.incognite.remove(i2)
                self.dati.extend([i1,i2])
                return controllo
        return controllo'''

    def trova_soluzioni(self):

        self.imposta()
        print('giroooo')
        nuovi_dati=[]
        incognite_trovate=[]
        controllo = 0
        for i in self.incognite:
            print(i.nome)

        for x in self.incognite:
            #print('cerco ' + x.nome)
            sol = o.operazione()
            c1=0
            for l in self.leggi:
                c = 0
                #z = o.variabile()
                for v in l.var:
                    #print(l.nome, v.nome)
                    if v.nome == x.nome:  # cerca il nome della variabile, da per scontato di trovarne una sola

                        print('trovato ', v.nome)
                        c1=1


                        nomi_dati = []
                        nomi = []

                        for d in self.dati:
                            nomi_dati.append(d.nome)
                        for j in l.var:
                            nomi.append(j.nome)

                        #for j in nomi:
                        #    print('prima', l.nome, j)

                        nomi.remove(v.nome)

                        for j in nomi:
                            if j == 'costante':
                                nomi.remove(j)

                        #for j in nomi:
                        #    print('dopo',j)


                        if all(n in nomi_dati for n in nomi):
                            c=1
                            controllo = 1
                            #print(v.nome)
                            sol = l.soluzione(v)
                            sol.risultato()
                            v.valore = sol.valore
                            self.soluzioni.append(sol)

                            incognite_trovate.append(x)
                            #self.incognite.remove(x)
                            nuovi_dati.append(v)

                            '''
                            for nome in nomi_dati:
                                print('dato' + nome)
    
                            for nome in nomi:
                                print('serve' + nome)
                            '''
                            print('soluzione ', v.nome, v.valore)
                            #break
                #if c==1:
                #    break
            if c1 == 0:
                print('icognita ' + x.nome + ' non trovata ')
        for i in incognite_trovate:
            self.incognite.remove(i)
        self.dati.extend(nuovi_dati)
        return controllo



'''
def risolvi (dati, incognite, s):

    teorie = []

    Mu=f.moto_rett_unif()
    Ma = f.moto_unif_acc()
    D = f.dinamica()

    teorie.append(Mu)
    teorie.append(Ma)
    teorie.append(D)

    for t in teorie:
        for v in t.var:
            for d in dati:
                if v.nome == d.nome:
                    v.valore = d.valore

    leggi = []

    Mu.legge_oraria()
    Ma.legge_oraria()
    Ma.legge_velocita()
    D.legge_Newton()

    leggi.append(Mu.l_oria)
    leggi.append(Ma.l_oria)
    leggi.append(Ma.l_v)
    leggi.append(D.l_N)


    
    possibili_soluzioni=[]

    for l in leggi:
        for v in l.var:
            for x in incognite:
                if v.nome == x.nome:
                    if not l in possibili_soluzioni:
                        possibili_soluzioni.append(l)
    
    return possibili_soluzioni
    
    soluzioni=[]
    controllo=0
    for x in incognite:
        sol=o.operazione()
        for l in leggi:
            c = 0
            z=o.variabile()
            for v in l.var:
                if v.nome == x.nome: #cerca il nome della variabile
                    c=1
                    z=v
            if c==1:
                lv=l.var
                lv.remove(z)
                for v in lv :
                    if v.nome == 'costante':
                        lv.remove(v)

                nomi_dati=[]
                nomi=[]

                for d in dati:
                    nomi_dati.append(d.nome)
                for v in lv:
                    nomi.append(v.nome)


                if all(v in nomi_dati for v in nomi):
                    controllo=1

                    sol=l.soluzione(z)
                    sol.risultato()
                    z.valore=sol.valore
                    soluzioni.append(sol)

                    incognite.remove(x)
                    dati.append(z)
                    #print(z.nome)
        if c==0:
            print('icognita '+ x.nome + ' non trovata ')

    s.extend(soluzioni)

    return s, controllo, dati, incognite

'''




#PROVA

x=o.variabile()
x.nome='posizione'
#x.valore= 2

x0=o.variabile()
x0.nome='posizione iniziale'
x0.valore= 0

y=o.variabile()
y.valore= 5
y.nome='forza'

z=o.variabile()
z.nome='reazione vincolare'
#z.valore= 3

d=o.variabile()
d.nome='angolo inclinazione'
#d.valore= np.pi / 6

v=o.variabile()
v.nome='velocità'
v.valore=4

v0=o.variabile()
v0.nome='velocità iniziale'
#v0.valore=8

a=o.variabile()
a.nome='accelerazione'
a.valore=2

t=o.variabile()
t.nome='tempo'
t.valore=2

k=o.variabile()
k.nome='massa'
k.valore=6

dati=[ x0, v, t,a]

incognite=[x]


P=problema(dati,incognite)
#P.imposta()
P.risolvi()
s=P.soluzioni

''' serviva con la funzione risolvi...
e=1
while e==1:
    s,e , dati, incognite=risolvi(dati,incognite,s)
'''

print(len(s))
for i in range(len(s)):
    print(s[i].nome, s[i].valore)







