

import collections
import csv
import numpy as np
from cmath import sqrt
import time
from datetime import date, datetime
import sched
import os
import io
from numpy import memmap, mean
import math


goniometriche=['coseno', 'arccoseno', 'seno', 'arcseno']
trascendenti=['coseno', 'arccoseno', 'seno', 'arcseno', 'esponenziale', 'logaritmo', 'radice', 'potenza']

operazioni_elementari=['piu','meno','per','diviso']

class variabile :
    def __init__(self):
        self.nome='variabile'
        self.valore=0
        self.relazione=[]
        self.l=[self]
        self.var=[self]
        self.grado_variabili=[]
        self.tipo_variabili=[]
        self.tipo=[]
    def variabili(self):
        return self.var

    def coefficiente(self,v):
        c = variabile()
        if v.nome == self.nome :
            c.nome='1'
            c.valore=1
        else:
            c.nome='0'

        return c


    def tipo_var(self):
        self.tipo_variabili.append([self.nome, []])
        return self.tipo_variabili

    def grado(self):
        self.grado_variabili.append([self.nome, 1])
        return self.grado_variabili

class piu :
    def __init__(self, var1, var2):
        self.l=[]
        self.l.append(self)
        self.v1 = var1
        self.v2 = var2
        self.var=[]
        self.grado_variabili=[]
        self.tipo_variabili=[]
        self.r = variabile()
        self.nome='('+ self.v1.nome + ' + ' + self.v2.nome +')'
        self.valore= self.v1.valore + self.v2.valore
        self.relazione = []

        self.tipo=self.v1.tipo
        for t in self.v2.tipo:
            if not t in self.tipo:
                self.tipo.append(t)

        '''
        if isinstance(self.v1, variabile):
            self.var.append(self.v1)
        else:
            self.var.extend(self.v1.var)
        if isinstance(self.v2, variabile):
            self.var.append(self.v2)
        else:
            self.var.extend(self.v2.var)
        '''

    def risultato (self):
        self.r.nome = '('+ self.v1.nome + ' + ' + self.v2.nome +')'
        self.r.valore = self.v1.valore + self.v2.valore
        return self.r

    def coefficiente(self, v):
        if self.v1.coefficiente(v).valore == 0:
            if self.v2.coefficiente(v).valore == 0:
                c=variabile()
                c.nome='0'
                #print('qui')
                return c
            else:
                return self.v2.coefficiente(v)
        else:

            if self.v2.coefficiente(v).valore == 0:
                return self.v1.coefficiente(v)
            else:
                return piu(self.v1.coefficiente(v), self.v2.coefficiente(v))


    def coefficiente1(self, v):
        c=operazione()
        c.l.append(piu(self.v1.coefficiente(v), self.v2.coefficiente(v)))
        return c

    def variabili(self):
        self.v1.variabili()
        for v in self.v1.var:
            if not v in self.var:
                self.var.append(v)
        self.v2.variabili()
        for v in self.v2.var:
            if not v in self.var:
                self.var.append(v)
        return self.var

    def tipo_var(self):
        for v in self.variabili():
            v_tipo=[]
            if v in self.v1.variabili():
                for t in self.v1.tipo_var():
                    if t[0] == v.nome:
                        for t1 in t[1]:
                            if not t1 in v_tipo:
                                v_tipo.append(t1)

                if v in self.v2.variabili():
                    for t in self.v2.tipo_var():
                        if t[0] == v.nome:
                            for t1 in t[1]:
                                if not t1 in v_tipo:
                                    v_tipo.append(t1)
            else:
                for t in self.v2.tipo_var():
                    if t[0] == v.nome:
                        for t1 in t[1]:
                            if not t1 in v_tipo:
                                v_tipo.append(t1)

            self.tipo_variabili.append([v.nome, v_tipo])

        return self.tipo_variabili

    def grado(self):
        for v in self.var:
            if v in self.v1.variabili():
                for deg in self.v1.grado():
                    if deg[0] == v.nome:
                        d1=deg[1]
                if v in self.v2.variabili():
                    for deg in self.v2.grado():
                        if deg[0] == v.nome:
                            d2 = deg[1]
                    self.grado_variabili.append([v.nome, np.max([d1,d2])])
                else:
                    self.grado_variabili.append([v.nome, d1])
            else:
                for deg in self.v2.grado():
                    if deg[0] == v.nome:
                        d2 = deg[1]
                self.grado_variabili.append([v.nome, d2])
        return self.grado_variabili

    def inversa (self, res, v):

        if v.nome == self.v1.nome:
            return meno(res, self.v2)
        else:
            return meno(res, self.v1)

    def relazioni_alle_variabili(self):
        self.v1.relazione.extend(self.relazione)
        self.v2.relazione.extend(self.relazione)

class meno :
    def __init__(self, var1, var2):
        self.l = []
        self.l.append(self)
        self.v1 = var1
        self.v2 = var2
        self.var=[]
        self.grado_variabili=[]
        self.tipo_variabili = []
        self.r = variabile()
        self.nome = '(' + self.v1.nome + ' - ' + self.v2.nome + ')'
        self.valore = self.v1.valore - self.v2.valore
        self.relazione = []
        self.tipo = self.v1.tipo
        for t in self.v2.tipo:
            if not t in self.tipo:
                self.tipo.append(t)
        '''
        if isinstance(self.v1, variabile):
            self.var.append(self.v1)
        else:
            self.var.extend(self.v1.var)
        if isinstance(self.v2, variabile):
            self.var.append(self.v2)
        else:
            self.var.extend(self.v2.var)
        '''

    def risultato (self):
        self.r.nome = '(' + self.v1.nome + ' - ' + self.v2.nome + ')'
        self.r.valore = self.v1.valore - self.v2.valore
        return self.r

    def coefficiente(self, v):
        if self.v1.coefficiente(v).valore == 0:
            if self.v2.coefficiente(v).valore == 0:
                c=variabile()
                c.nome='0'

                return c
            else:
                return self.v2.coefficiente(v)
        else:
            #print(self.v1.coefficiente(v).nome)
            if self.v2.coefficiente(v).valore == 0:
                #print(self.v2.coefficiente(v).nome)
                return self.v1.coefficiente(v)
            else:
                #print('qui', self.v2.nome, v.nome, self.v2.coefficiente(v).nome )
                return meno(self.v1.coefficiente(v), self.v2.coefficiente(v))

    def coefficiente1(self, v):
        c=operazione()
        c.l.append(meno(self.v1.coefficiente(v), self.v2.coefficiente(v)))
        return c

    def variabili(self):
        self.v1.variabili()
        for v in self.v1.var:
            if not v in self.var:
                self.var.append(v)
        self.v2.variabili()
        for v in self.v2.var:
            if not v in self.var:
                self.var.append(v)
        return self.var

    def tipo_var(self):
        for v in self.variabili():
            v_tipo = []
            if v in self.v1.variabili():
                for t in self.v1.tipo_var():
                    if t[0] == v.nome:
                        for t1 in t[1]:
                            if not t1 in v_tipo:
                                v_tipo.append(t1)

                if v in self.v2.variabili():
                    for t in self.v2.tipo_var():
                        if t[0] == v.nome:
                            for t1 in t[1]:
                                if not t1 in v_tipo:
                                    v_tipo.append(t1)
            else:
                for t in self.v2.tipo_var():
                    if t[0] == v.nome:
                        for t1 in t[1]:
                            if not t1 in v_tipo:
                                v_tipo.append(t1)

            self.tipo_variabili.append([v.nome, v_tipo])

        return self.tipo_variabili

    def grado(self):
        for v in self.var:
            if v in self.v1.variabili():
                for deg in self.v1.grado():
                    if deg[0] == v.nome:
                        d1=deg[1]
                if v in self.v2.variabili():
                    for deg in self.v2.grado():
                        if deg[0] == v.nome:
                            d2 = deg[1]
                    self.grado_variabili.append([v.nome, np.max([d1,d2])])
                else:
                    self.grado_variabili.append([v.nome, d1])
            else:
                for deg in self.v2.grado():
                    if deg[0] == v.nome:
                        d2 = deg[1]
                self.grado_variabili.append([v.nome, d2])
        return self.grado_variabili

    def inversa (self, res, v):

        if v.nome == self.v1.nome:
            return piu(res, self.v2)
        else:
            return meno(self.v1, res)

    def relazioni_alle_variabili(self):
        self.v1.relazione.extend(self.relazione)
        self.v2.relazione.extend(self.relazione)

class per :
    def __init__(self, var1, var2):
        self.l = []
        self.l.append(self)
        self.v1 = var1
        self.v2 = var2
        self.var=[]
        self.grado_variabili=[]
        self.tipo_variabili = []
        self.r = variabile()
        self.nome = '(' + self.v1.nome + ' * ' + self.v2.nome + ')'
        self.valore = self.v1.valore * self.v2.valore
        self.relazione = []
        self.tipo = self.v1.tipo
        for t in self.v2.tipo:
            if not t in self.tipo:
                self.tipo.append(t)

        '''
        if isinstance(self.v1, variabile):
            self.var.append(self.v1)
        else:
            self.var.extend(self.v1.var)
        if isinstance(self.v2, variabile):
            self.var.append(self.v2)
        else:
            self.var.extend(self.v2.var)
        '''

    def risultato (self):
        self.r.nome = '(' + self.v1.nome + ' * ' + self.v2.nome + ')'
        self.r.valore = self.v1.valore * self.v2.valore
        return self.r

    def coefficiente(self, v):
        if self.v1.coefficiente(v).valore == 0:
            if self.v2.coefficiente(v).valore == 0:
                c=variabile()
                c.nome='0'
                return c
            else:
                return per(self.v1, self.v2.coefficiente(v))
        else:
            if self.v2.coefficiente(v).valore == 0:
                return per(self.v2, self.v1.coefficiente(v))
            else:
                return per(self.v1.coefficiente(v), self.v2.coefficiente(v)) #sbagliatoooo!!!

    def coefficiente1(self, v):
        c=operazione()
        c.l.append(per(self.v1.coefficiente(v), self.v2.coefficiente(v)))
        return c

    def variabili(self):
        self.v1.variabili()
        for v in self.v1.var:
            if not v in self.var:
                self.var.append(v)
        self.v2.variabili()
        for v in self.v2.var:
            if not v in self.var:
                self.var.append(v)
        return self.var

    def tipo_var(self):
        for v in self.variabili():
            v_tipo = []
            if v in self.v1.variabili():
                for t in self.v1.tipo_var():
                    if t[0] == v.nome:
                        for t1 in t[1]:
                            if not t1 in v_tipo:
                                v_tipo.append(t1)

                if v in self.v2.variabili():
                    for t in self.v2.tipo_var():
                        if t[0] == v.nome:
                            for t1 in t[1]:
                                if not t1 in v_tipo:
                                    v_tipo.append(t1)
            else:
                for t in self.v2.tipo_var():
                    if t[0] == v.nome:
                        for t1 in t[1]:
                            if not t1 in v_tipo:
                                v_tipo.append(t1)

            self.tipo_variabili.append([v.nome, v_tipo])

        return self.tipo_variabili

    def grado(self):
        for v in self.var:
            if v in self.v1.variabili():
                for deg in self.v1.grado():
                    if deg[0] == v.nome:
                        d1=deg[1]
                if v in self.v2.variabili():
                    for deg in self.v2.grado():
                        if deg[0] == v.nome:
                            d2 = deg[1]
                    self.grado_variabili.append([v.nome, d1+d2])
                else:
                    self.grado_variabili.append([v.nome, d1])
            else:
                for deg in self.v2.grado():
                    if deg[0] == v.nome:
                        d2 = deg[1]
                self.grado_variabili.append([v.nome, d2])
        return self.grado_variabili

    def inversa (self, res, v):

        if v.nome == self.v1.nome:
            return diviso(res, self.v2)
        else:
            return diviso(res, self.v1)

    def relazioni_alle_variabili(self):
        self.v1.relazione.extend(self.relazione)
        self.v2.relazione.extend(self.relazione)

class diviso :
    def __init__(self, var1, var2):
        self.l = []
        self.l.append(self)
        self.v1 = var1
        self.v2 = var2
        self.var=[]
        self.grado_variabili=[]
        self.tipo_variabili = []
        self.r = variabile()
        self.nome = '(' + self.v1.nome + ' : ' + self.v2.nome + ')'
        if self.v2.valore == 0:
            self.nome = self.nome + 'divisione per 0'
            self.valore=0
        else:
            self.valore = self.v1.valore / self.v2.valore
        self.relazione = []

        self.tipo = self.v1.tipo
        for t in self.v2.tipo:
            if not t in self.tipo:
                self.tipo.append(t)

        '''
        if isinstance(self.v1, variabile):
            self.var.append(self.v1)
        else:
            self.var.extend(self.v1.var)
        if isinstance(self.v2, variabile):
            self.var.append(self.v2)
        else:
            self.var.extend(self.v2.var)
        '''

    def risultato (self):
        self.r.nome = self.nome
        self.r.valore = self.valore
        return self.r

    def coefficiente(self, v):
        if self.v1.coefficiente(v).valore == 0:
            if self.v2.coefficiente(v).valore == 0:
                c=variabile()
                c.nome='0'
                #print('qui')
                return c
            else:
                return diviso(self.v2.coefficiente(v), self.v1)#è il coefficiente di v a denominatore!
        else:
            #print(self.v1.coefficiente(v).nome)
            if self.v2.coefficiente(v).valore == 0:
                return diviso(self.v1.coefficiente(v), self.v2 )
            else:
                return diviso(self.v1.coefficiente(v), self.v2.coefficiente(v)) #sbagliatoooo!!!

    def coefficiente1(self, v):
        c=operazione()
        c.l.append(piu(self.v1.coefficiente(v), self.v2.coefficiente(v)))
        return c

    def variabili(self):
        self.v1.variabili()
        for v in self.v1.var:
            if not v in self.var:
                self.var.append(v)
        self.v2.variabili()
        for v in self.v2.var:
            if not v in self.var:
                self.var.append(v)
        return self.var

    def tipo_var(self):
        for v in self.variabili():
            v_tipo = []
            if v in self.v1.variabili():
                for t in self.v1.tipo_var():
                    if t[0] == v.nome:
                        for t1 in t[1]:
                            if not t1 in v_tipo:
                                v_tipo.append(t1)

                if v in self.v2.variabili():
                    for t in self.v2.tipo_var():
                        if t[0] == v.nome:
                            for t1 in t[1]:
                                if not t1 in v_tipo:
                                    v_tipo.append(t1)
            else:
                for t in self.v2.tipo_var():
                    if t[0] == v.nome:
                        for t1 in t[1]:
                            if not t1 in v_tipo:
                                v_tipo.append(t1)

            self.tipo_variabili.append([v.nome, v_tipo])

        return self.tipo_variabili

    def grado(self):
        for v in self.var:
            if v in self.v1.variabili():
                for deg in self.v1.grado():
                    if deg[0] == v.nome:
                        d1=deg[1]
                if v in self.v2.variabili():
                    for deg in self.v2.grado():
                        if deg[0] == v.nome:
                            d2 = deg[1]
                    self.grado_variabili.append([v.nome, d1 - d2])
                else:
                    self.grado_variabili.append([v.nome, d1])
            else:
                for deg in self.v2.grado():
                    if deg[0] == v.nome:
                        d2 = deg[1]
                self.grado_variabili.append([v.nome, d2])
        return self.grado_variabili

    def inversa (self, res, v):

        if v.nome == self.v1.nome:
            return per(res, self.v2)
        else:
            return diviso(self.v1, res)

    def relazioni_alle_variabili(self):
        self.v1.relazione.extend(self.relazione)
        self.v2.relazione.extend(self.relazione)

class operazione:
    def __init__(self):
        self.l=[]
        self.var=[]
        self.grado_variabili=[]
        self.tipo_variabili=[]
        self.nome='lista operazioni'
        self.valore=0
        self.relazione=[]
        self.r=variabile() #risultato dell'operatore
        self.tipo=[]

    def risultato(self):

        if len(self.l)>0:
            self.nome = self.l[-1].risultato().nome
            self.valore = self.l[-1].risultato().valore
            self.r=self.l[-1].risultato()
            return self.r
        else :
            self.nome = 'nessuna operazione'

    def coefficiente(self,v):
        return self.l[-1].coefficiente(v)

    def coefficiente1(self,v):
        c=operazione()
        n=len(self.l)
        for i in range(n):
            if isinstance(self.l[n-1-i], per):
                if v in self.l[n-1-i].v2.variabili():
                    if v == self.l[n-1-i].v2:
                        c.l.append(self.l[n-1-i].v1)
                    else:
                        c.l.append(per(self.l[n-1-i].v1, self.l[n-1-i].v2.coefficiente(v) ))

                    if v in self.l[n - 1 - i].v1.variabili():
                        if v == self.l[n - 1 - i].v1:
                            c.l.append(self.l[n - 1 - i].v2)
                        else:
                            c.l.append(per(self.l[n - 1 - i].v2, self.l[n - 1 - i].v1.coefficiente(v)))



    def grado(self):
        self.grado_variabili=self.l[-1].grado()
        return self.grado_variabili

    def variabili(self):
        for o in self.l:
            o.variabili()
            for v in o.var:
                if not v in self.var:
                    self.var.append(v)

        return self.var

    def tipo_var(self):
        self.tipo_variabili = self.l[-1].tipo_var()
        return self.tipo_variabili

    def tipo_operazione(self):
        self.tipo = self.l[-1].tipo
        return self.tipo

    '''def variabili_old(self):
        n = len(self.l)
        if isinstance(self.l[0].v1, variabile):
            self.var.append(self.l[0].v1)
        else:
            self.var.extend(self.l[0].v1.var)
        if isinstance(self.l[0].v2, variabile):
            self.var.append(self.l[0].v2)
        else:
            self.var.extend(self.l[0].v2.var)

        for i in range(1,n):
            if isinstance(self.l[i].v2, variabile):
                self.var.append(self.l[i].v2)
            else:
                self.var.extend(self.l[i].v2.var)


        return self.var'''

    def  relazioni_alle_variabili (self):
        for v in self.var:
            for rel in self.relazione:
                if not rel in v.relazione:
                    v.relazione.append(rel)
        '''for i in range(len(self.l)):
            for rel in self.relazione:
                self.l[i].relazione.append(rel)'''

class coseno:
    def __init__(self,var):
        self.v=var
        self.nome='cos('+ self.v.nome + ')'
        self.valore= np.cos(self.v.valore)
        self.l=[self]
        self.r=variabile()
        self.var=[]
        self.grado_variabili=[]
        self.tipo_variabili = []
        self.relazione=[]
        self.tipo=self.v.tipo
        self.tipo.append('goniometrica')

    def risultato(self):
        self.r.nome = self.nome
        self.r.valore=self.valore
        return self.r

    def variabili(self):
        if isinstance(self.v, variabile):
            self.var.append(self.v)
        else:
            self.v.variabili()
            self.v.var
        return self.var

    def tipo_var(self):
        self.tipo_variabili=self.v.tipo_var()
        for t in self.tipo_variabili:
            t[1].append('goniometrica')
        return self.tipo_variabili


    def grado(self):

        for deg in self.v.grado():
            self.grado_variabili.append([deg[0], deg[1]])
        return self.grado_variabili

    def relazioni_alle_variabili(self):
        self.v.relazione.extend(self.relazione)

    def inversa (self, res):

        return arccoseno(res)

class arccoseno:
    def __init__(self,var):
        self.v=var
        self.nome='arccos('+ self.v.nome + ')'
        self.valore= np.arccos(self.v.valore)
        self.l=[self]
        self.r=variabile()
        self.var=[]
        self.grado_variabili = []
        self.tipo_variabili = []
        self.relazione=[]

        self.tipo=self.v.tipo
        self.tipo.append('goniometrica')

    def risultato(self):
        self.r.nome = self.nome
        self.r.valore=self.valore
        return self.r

    def variabili(self):
        if isinstance(self.v, variabile):
            self.var.append(self.v)
        else:
            self.v.variabili()
            self.v.var
        return self.var

    def tipo_var(self):
        self.tipo_variabili=self.v.tipo_var()
        for t in self.tipo_variabili:
            t[1].append('goniometrica')
        return self.tipo_variabili

    def grado(self):

        for deg in self.v.grado():
            self.grado_variabili.append([deg[0], deg[1]])
        return self.grado_variabili

    def relazioni_alle_variabili(self):
        self.v.relazione.extend(self.relazione)

    def inversa (self, res):

        return coseno(res)

class seno:
    def __init__(self,var):
        self.v=var
        self.nome='sen('+ self.v.nome + ')'
        self.valore= np.sin(self.v.valore)
        self.l=[self]
        self.r=variabile()
        self.var=[]
        self.grado_variabili = []
        self.tipo_variabili = []
        self.relazione=[]

        self.tipo=self.v.tipo
        self.tipo.append('goniometrica')

    def risultato(self):
        self.r.nome = self.nome
        self.r.valore=self.valore
        return self.r

    def variabili(self):
        if isinstance(self.v, variabile):
            self.var.append(self.v)
        else:
            self.v.variabili()
            self.v.var
        return self.var

    def tipo_var(self):
        self.tipo_variabili=self.v.tipo_var()
        for t in self.tipo_variabili:
            t[1].append('goniometrica')
        return self.tipo_variabili

    def grado(self):

        for deg in self.v.grado():
            self.grado_variabili.append([deg[0], deg[1]])
        return self.grado_variabili

    def relazioni_alle_variabili(self):
        self.v.relazione.extend(self.relazione)

    def inversa (self, res):

        return arcseno(res)

class arcseno:
    def __init__(self,var):
        self.v=var
        self.nome='arcsen('+ self.v.nome + ')'
        self.valore= np.arcsin(self.v.valore)
        self.l=[self]
        self.r=variabile()
        self.var=[]
        self.grado_variabili = []
        self.tipo_variabili = []
        self.relazione=[]
        self.tipo=self.v.tipo
        self.tipo.append('goniometrica')

    def risultato(self):
        self.r.nome = self.nome
        self.r.valore=self.valore
        return self.r

    def variabili(self):
        if isinstance(self.v, variabile):
            self.var.append(self.v)
        else:
            self.v.variabili()
            self.v.var
        return self.var

    def tipo_var(self):
        self.tipo_variabili=self.v.tipo_var()
        for t in self.tipo_variabili:
            t[1].append('goniometrica')
        return self.tipo_variabili

    def grado(self):

        for deg in self.v.grado():
            self.grado_variabili.append([deg[0], deg[1]])
        return self.grado_variabili

    def relazioni_alle_variabili(self):
        self.v.relazione.extend(self.relazione)

    def inversa (self, res):

        return seno(res)

class esponenziale: #c'è un problema nel valore se le variabili sono di tipo diverso, es. int e float
    def __init__(self, var, base):
        self.v=var
        self.b=base
        self.nome = str(self.b) + '^('+ self.v.nome + ')'
        self.valore= self.b**self.v.valore #np.power(self.b, self.v.valore)
        self.l=[self]
        self.r=variabile()
        self.var=[]
        self.grado_variabili = []
        self.tipo_variabili = []
        self.relazione=[]
        self.tipo=self.v.tipo
        self.tipo.append('esponenziale')

    def risultato(self):
        self.r.nome = self.nome
        self.r.valore=self.valore
        return self.r

    def variabili(self):
        if isinstance(self.v, variabile):
            self.var.append(self.v)
        else:
            self.v.variabili()
            self.v.var
        return self.var

    def tipo_var(self):
        self.tipo_variabili=self.v.tipo_var()
        for t in self.tipo_variabili:
            t[1].append('esponenziale')
        return self.tipo_variabili

    def grado(self):

        for deg in self.v.grado():
            self.grado_variabili.append([deg[0], deg[1]])
        return self.grado_variabili

    def relazioni_alle_variabili(self):
        self.v.relazione.extend(self.relazione)

    def inversa (self, res):

        return logaritmo(res,self.b)

class logaritmo:
    def __init__(self,var, base):
        self.v=var
        self.b=base
        self.nome = 'log_' + str(self.b) + '(' + self.v.nome + ')'
        self.valore= np.log(self.v.valore) / np.log(self.b)
        self.l=[self]
        self.r=variabile()
        self.var=[]
        self.grado_variabili = []
        self.tipo_variabili = []
        self.relazione=[]
        self.tipo = self.v.tipo
        self.tipo.append('logaritmica')

    def risultato(self):
        self.r.nome = self.nome
        self.r.valore=self.valore
        return self.r

    def variabili(self):
        if isinstance(self.v, variabile):
            self.var.append(self.v)
        else:
            self.v.variabili()
            self.v.var
        return self.var

    def tipo_var(self):
        self.tipo_variabili=self.v.tipo_var()
        for t in self.tipo_variabili:
            t[1].append('logaritmica')
        return self.tipo_variabili

    def grado(self):

        for deg in self.v.grado():
            self.grado_variabili.append([deg[0], deg[1]])
        return self.grado_variabili

    def relazioni_alle_variabili(self):
        self.v.relazione.extend(self.relazione)

    def inversa (self, res):

        return esponenziale(res, self.b)

class potenza:
    def __init__(self, var, esponente):
        self.v = var
        self.b = esponente
        self.nome = self.v.nome + '^('+ str(self.b) + ')'
        self.valore = np.power(self.v.valore, self.b)
        self.l=[self]
        self.r=variabile()
        self.var=[]
        self.grado_variabili=[]
        self.tipo_variabili = []
        self.relazione=[]

        self.tipo=self.v.tipo

    def risultato(self):
        self.r.nome = self.nome
        self.r.valore=self.valore
        return self.r

    def coefficiente(self, v):
        c = variabile()
        if v.nome == self.nome:
            c.nome = '1'
            c.valore = 1
        else:
            c.nome = '0'

        return c

    def variabili(self):
        self.var=self.v.variabili()
        return self.var

    def tipo_var(self):
        self.tipo_variabili=self.v.tipo_var()
        return self.tipo_variabili

    def grado(self):

        for deg in self.v.grado():
            self.grado_variabili.append([deg[0], deg[1]*self.b])
        return self.grado_variabili

    def relazioni_alle_variabili(self):
        self.v.relazione.extend(self.relazione)

    def inversa (self, res):

        return radice(res,self.b)

class radice:
    def __init__(self,var, indice):
        self.v=var
        self.b=indice
        self.nome='radice_'+ str(self.b) +'('+ self.v.nome + ')'
        self.valore=np.power(self.v.valore, 1/self.b)
        self.l=[self]
        self.r=variabile()
        self.var=[]
        self.grado_variabili=[]
        self.tipo_variabili = []
        self.relazione=[]

        self.tipo=self.v.tipo

    def risultato(self):
        self.r.nome = self.nome
        self.r.valore=self.valore
        return self.r

    def variabili(self):
        self.var = self.v.variabili()
        return self.var

    def tipo_var(self):
        self.tipo_variabili=self.v.tipo_var()
        return self.tipo_variabili

    def grado(self):
        for deg in self.v.grado():
            self.grado_variabili.append([deg[0], deg[1] / self.b])
        return self.grado_variabili

    def relazioni_alle_variabili(self):
        self.v.relazione.extend(self.relazione)

    def inversa (self, res):

        return potenza(res, self.b)


class equazione:
    def __init__(self, membro1, membro2):
        self.nome='equazione'
        self.m1=membro1
        self.m2=membro2

        self.var=[]

        self.sol=operazione()
        self.soluzioni=[]

        '''
        self.tipo=self.m1.tipo
        for t in self.m2.tipo:
            if not t in self.tipo:
                self.tipo.append(t)
        '''

    def grado(self, v):
        d1=0
        d2=0
        if v in self.m1.variabili():
            for deg in self.m1.grado():
                if v.nome == deg[0]:
                    d1=deg[1]
        if v in self.m2.variabili():
            for deg in self.m2.grado():
                if v.nome == deg[0]:
                    d1=deg[1]

        return np.max([d1,d2])

    def tipo(self,v):
        tipo=[]
        if v in self.m1.variabili():
            for tv in self.m1.tipo_var():
                if tv[0] == v.nome:
                    for t1 in tv[1]:
                        if not t1 in tipo:
                            tipo.append(t1)
        if v in self.m2.variabili():
            for tv in self.m2.tipo_var():
                if tv[0] == v.nome:
                    for t1 in tv[1]:
                        if not t1 in tipo:
                            tipo.append(t1)
        return tipo

    def variabili(self):
        self.m1.variabili()
        for v in self.m1.var:
            if not v in self.var:
                self.var.append(v)
        self.m2.variabili()
        for v in self.m2.var:
            if not v in self.var:
                self.var.append(v)

        return self.var

    '''def variabili_old(self):
        if not isinstance(self.m1, variabile):
            for o in self.m1.l:
                if isinstance(o.v1, variabile):
                    if not o.v1 in self.var:
                        self.var.append(o.v1)
                else:
                    for e in o.v1.l:
                        if isinstance(e.v1, variabile):
                            if not e.v1 in self.var:
                                self.var.append(e.v1)
                        if isinstance(e.v2, variabile):
                            if not e.v2 in self.var:
                                self.var.append(e.v2)
                if isinstance(o.v2, variabile):
                    if not o.v2 in self.var:
                        self.var.append(o.v2)
                else:
                    for e in o.v2.l:
                        if isinstance(e.v1, variabile):
                            if not e.v1 in self.var:
                                self.var.append(e.v1)
                        if isinstance(e.v2, variabile):
                            if not e.v2 in self.var:
                                self.var.append(e.v2)
        else:
            self.var.append(self.m1)
        if not isinstance(self.m2, variabile):
            for o in self.m2.l:
                if isinstance(o.v1, variabile):
                    if not o.v1 in self.var:
                        self.var.append(o.v1)
                else:
                    for e in o.v1.l:
                        if isinstance(e.v1, variabile):
                            if not e.v1 in self.var:
                                self.var.append(e.v1)
                        if isinstance(e.v2, variabile):
                            if not e.v2 in self.var:
                                self.var.append(e.v2)
                if isinstance(o.v2, variabile):
                    if not o.v2 in self.var:
                        self.var.append(o.v2)
                else:
                    for e in o.v2.l:
                        if isinstance(e.v1, variabile):
                            if not e.v1 in self.var:
                                self.var.append(e.v1)
                        if isinstance(e.v2, variabile):
                            if not e.v2 in self.var:
                                self.var.append(e.v2)
        else:
            self.var.append(self.m2)'''

    def relazioni(self):
        self.m1.relazione.append(self)
        self.m2.relazione.append(self)
        if not isinstance(self.m1, variabile):
            self.m1.relazioni_alle_variabili()
        if not isinstance(self.m2, variabile):
            self.m2.relazioni_alle_variabili()

    '''
    def riduzione_old(self, v, res=None):

        n = len(self.m1.l)
        i = 0

        if res is None:
            R = self.m2
        else:
            R = res

        for i in range(n-1):

            if isinstance(self.m1.l[n - 1 - i].v2, variabile) :
                if v == self.m1.l[n - 1-i].v2:

                    #print(v.nome, self.m1.l[n - 1 -i].v2.nome)
                    self.sol.l.append(self.m1.l[n - 1 -i].inversa(R, self.m1.l[n - 1 -i].v2))
                    return self.sol
                else:
                    self.sol.l.append(self.m1.l[n - 1 -i].inversa(R, self.m1.l[n - 2 - i]))
                    self.sol.risultato()
                    R=self.sol
                    #print(self.sol.l[-1].nome)

            elif  v in self.m1.l[n - 1-i].v2.var :
                self.sol.l.append(self.m1.l[n - 1-i].inversa(R, self.m1.l[n - 1-i].v2))
                #print(self.sol.l[-1].nome)

                m1=self.m1.l[n - 1-i].v2
                m2=self.sol

                m1.risultato()
                m2.risultato()
                E1=equazione(m1,m2)
                E1.soluzione(v)
                self.sol.l.extend(E1.sol.l)
                #print(self.sol.l[-1].nome)
                return self.sol

            else:
                self.sol.l.append(self.m1.l[n - 1 -i].inversa(R, self.m1.l[n - 2 - i]))
                self.sol.risultato()
                R = self.sol
                #print(self.sol.l[-1].nome)

        if isinstance(self.m1.l[0].v1, variabile):
            if v == self.m1.l[0].v1:
                #print(v.nome, self.m1.l[0].v1.nome)
                self.sol.l.append(self.m1.l[0].inversa(R, self.m1.l[0].v1))
                return self.sol

            else:
                #print('variabile non trovata')
                return operazione()

        elif v in self.m1.l[0].v1.var:

            self.sol.l.append(self.m1.l[0].inversa(R, self.m1.l[0].v1))
            #print(self.sol.l[-1].nome)

            m1 = self.m1.l[0].v1
            m2 = self.sol
            #m2.append(self.m1.l[0].inversa(R, self.m1.l[0].v1))
            m2.risultato()
            E1 = equazione(m1, m2)
            E1.soluzione(v)
            self.sol.l.extend(E1.sol.l)
            #print(self.sol.l[-1].nome)
            return self.sol
        if isinstance(self.m1.l[0].v2, variabile):
            if v == self.m1.l[0].v2:
                #print(v.nome, self.m1.l[0].v2.nome)
                self.sol.l.append(self.m1.l[0].inversa(R, self.m1.l[0].v2))
                return self.sol

            else:
                print('variabile non trovata')
                return operazione()

        elif v in self.m1.l[0].v2.var:

            self.sol.l.append(self.m1.l[0].inversa(R, self.m1.l[0].v2))
            #print(self.sol.l[-1].nome)

            m1 = self.m1.l[0].v2
            m2 = self.sol
            #m2.append(self.m1.l[0].inversa(R, self.m1.l[0].v1))
            m2.risultato()
            E1 = equazione(m1, m2)
            E1.soluzione(v)
            self.sol.l.extend(E1.sol.l)
            #print(self.sol.l[-1].nome)
            return self.sol
        else:
            print('variabile non trovata')
            return operazione()
    
    def soluzione_primo_membro_old(self, v, res=None):

        #print('un membro',self.sol.l[-1].nome)
        n = len(self.m1.l)
        i = 0


        if res is None:
            R = self.m2
        else:
            R = res
        #print(n)

        if isinstance(self.m1, operazione):
            if n>1:
                if v.nome == self.m1.l[n - 1].v2.nome:
                    #print(n,'yes',v.nome, self.m1.l[n - 1].v2.nome)
                    self.sol.l.append(self.m1.l[n - 1].inversa(R, self.m1.l[n - 1].v2))
                    return self.sol
                else:
                    self.sol.l.append(self.m1.l[n - 1].inversa(R, self.m1.l[n - 2]))
                    R=self.sol

            for i in range(n - 2):

                if v.nome == self.m1.l[n - 2 - i].v2.nome:
                    #print(v.nome, self.m1.l[n - 2 - i].v2.nome)
                    self.sol.l.append(self.m1.l[n - 2 - i].inversa(R.l[-1], self.m1.l[n - 2 - i].v2))
                    return self.sol
                else:
                    self.sol.l.append(self.m1.l[n - 2 - i].inversa(R.l[-1], self.m1.l[n - 3 - i]))
                    R=self.sol

            if v.nome == self.m1.l[0].v1.nome or v.nome == self.m1.l[0].v2.nome:
                #print(v.nome, self.m1.l[0].v2.nome)
                self.sol.l.append(self.m1.l[0].inversa(R, v))
                return self.sol
            else:
                #print(v.nome, self.m1.l[0].v1.nome, self.m1.l[0].v2.nome, self.sol.nome)
                print('variabile non trovata')
                return operazione()
            return self.sol
        else:
            self.sol.append(self.m1.inversa(self.m2))
            E1=equazione(self.m1.v, self.sol[-1])
            self.sol.extend(E1.soluzione_primo_membro(v))
            return self.sol


    def soluzione_old(self, v):


        if isinstance(self.m1, variabile):
            if v == self.m1:
                self.sol.l.append(self.m2)
                return self.sol
            else:
                if isinstance(self.m2, variabile):
                    print('i membri sono variabii')
                    if v == self.m2:
                        self.sol.l.append(self.m1)
                        return self.sol
                    else:
                        print('variabile non trovata')
                        return operazione()
                else:
                    if v in self.m2.var:
                        E1 = equazione(self.m2, self.m1)
                        self.sol = E1.soluzione(v)
                        return self.sol
                    else:
                        print('variabile non trovata')
                        return operazione()

        else:
            n = len(self.m1.l)
            c = 0
            for i in range(n):
                if not isinstance(self.m1.l[n - 1 - i].v2, variabile):
                    c = 1
            if not isinstance(self.m1.l[0].v1, variabile):
                c = 1

            if isinstance(self.m2, variabile):
                if v == self.m2:
                    self.sol.l.append(self.m1)
                    return self.sol
                else:  #m1 operazione m2 variabile
                    if v in self.m1.var:
                        if c==1:
                            self.sol.l.extend( self.riduzione(v).l)
                            return self.sol
                        else:
                            self.sol.l.extend(self.soluzione_primo_membro(v).l)
                            return self.sol

            else: #ne m1 ne m2 sono variabili
                if v in self.m1.var:
                    if c==1:
                        self.sol = self.riduzione(v)
                        return self.sol
                    else:
                        #print(self.sol.l[-1].nome)
                        self.sol.l.extend(self.soluzione_primo_membro(v).l)
                        return self.sol
                elif v in self.m2.var:
                    E1=equazione(self.m2, self.m1)
                    self.sol = E1.soluzione(v)
                    return self.sol
                else:
                    print('variabile non trovata')
                    return operazione()

        if not self.sol.l:
            E1 = equazione(self.m2, self.m1)
            self.sol = E1.soluzione(v)

        if not self.sol.l:
            print('variabile non trovata')

        return self.sol
    
    '''
    def soluzione(self,v):
        if not self.tipo(v) and self.grado(v) == 2:
            self.soluzione2(v)
            return self.soluzioni
        else:
            if len(self.tipo(v)) < 2 and self.grado(v) < 3:
                self.soluzione1(v)
                self.soluzioni.append(self.sol)
                return self.sol


    def soluzione2(self,v):
        #if not self.tipo(v) and self.grado(v)==2:
        a1 = self.m1.coefficiente(potenza(v, 2))
        a2 = self.m2.coefficiente(potenza(v, 2))
        if not a1.valore==0:

            if not a2.valore == 0:

                a = meno(a1, a2)
            else:
                a=a1
        else:
            if not a2 == 0:
                a = a2
            else:
                print('coeffficiente ' + v.nome + '^2 uguale a zero')
                return []

        b1 = self.m1.coefficiente(v)
        b2 = self.m2.coefficiente(v)
        if not b1.valore == 0:

            if not b2.valore == 0:

                b = meno(b1, b2)
            else:
                b = b1
        else:
            if not b2.valore == 0:
                b = b2
            else:
                print('coeffficiente ' + v.nome + ' uguale a zero')
                b=variabile()
                b.nome='0'

        c1 = meno(self.m1, piu(per(a1, potenza(v, 2)), per(b1, v)))
        c2 = meno(self.m2, piu(per(a2, potenza(v, 2)), per(b2, v)))
        if not c1.valore == 0:

            if not c2.valore == 0:

                c = meno(c1, c2)
            else:
                c = c1
        else:
            if not c2.valore == 0:
                c = c2
            else:
                print('termine noto uguale a zero')
                c=variabile()
                c.nome='0'


        self.soluzioni=self.sol_eq_grado_2(a,b,c)
        return self.soluzioni

    def sol_eq_grado_2(self,a,b,c):
        s=[]
        quattro=variabile()
        quattro.nome='4'
        quattro.valore=4
        due=variabile()
        due.nome='2'
        due.valore=2

        menob=variabile()
        menob.nome='-' + b.nome
        menob.valore = - b.valore

        delta=meno(potenza(b,2), per(quattro,per(a,c)))
        if delta.valore < 0 :
            print('delta negativo, nessuna soluzione')
            return s
        if delta.valore == 0 :
            print('delta uguale a zero, una sola soluzione')
            sol=diviso(menob,per(due,a))
            s.append(sol)
            return s
        if delta.valore > 0 :
            print('delta maggiore di zero, due soluzioni')
            sol1 = diviso(meno(menob,radice(delta,2)), per(due, a))
            sol2 = diviso(piu(menob, radice(delta, 2)), per(due, a))
            s.extend([sol1,sol2])
            return s

    def soluzione1(self, v):

        self.variabili()
        if v in self.m2.var:
            E1 = equazione(self.m2, self.m1)
            self.sol = E1.soluzione(v)
            return self.sol
        else:
            R = self.m2
            if v in self.m1.var:
                if isinstance(self.m1, operazione):
                    n = len(self.m1.l)
                    for i in range(n):
                        j = 0
                        # print(self.m1.l[n - 1 - i].nome)
                        for oe in operazioni_elementari:
                            if isinstance(self.m1.l[n - 1 - i], oe):
                                j = 1
                                self.m1.l[n - 1 - i].v2.variabili()
                                if v in self.m1.l[n - 1 - i].v2.var:

                                    self.sol.l.append(self.m1.l[n - 1 - i].inversa(R, self.m1.l[n - 1 - i].v2))
                                    self.sol.risultato()
                                    R = self.sol

                                    if isinstance(self.m1.l[n - 1 - i].v2, variabile):
                                        return self.sol

                                    else:
                                        m1 = self.m1.l[n - 1 - i].v2
                                        m2 = self.sol

                                        m1.risultato()
                                        m2.risultato()
                                        E1 = equazione(m1, m2)
                                        E1.soluzione(v)
                                        self.sol.l.extend(E1.sol.l)
                                        # print(self.sol.l[-1].nome)
                                        return self.sol
                                break
                        if j==0:
                            self.m1.l[n - 1 - i].v.variabili()
                            if v in self.m1.l[n - 1 - i].v.var:

                                self.sol.l.append(self.m1.l[n - 1 - i].inversa(R, self.m1.l[n - 1 - i].v))
                                self.sol.risultato()
                                R = self.sol

                                if isinstance(self.m1.l[n - 1 - i].v, variabile):
                                    return self.sol

                                else:
                                    m1 = self.m1.l[n - 1 - i].v
                                    m2 = self.sol

                                    m1.risultato()
                                    m2.risultato()
                                    E1 = equazione(m1, m2)
                                    E1.soluzione(v)
                                    self.sol.l.extend(E1.sol.l)
                                    # print(self.sol.l[-1].nome)
                                    return self.sol
                    if n == 0:
                        for oe in operazioni_elementari:
                            if isinstance(self.m1.l[0], oe):
                                j = 1
                                if v in self.m1.l[0].v2.var:
                                    self.sol.append(self.m1.l[0].inversa(R, self.m1.l[0].v2))
                                    self.sol.risultato()
                                    R = self.sol

                                    if isinstance(self.m1.l[0].v2, variabile):
                                        return self.sol

                                    else:
                                        m1 = self.m1.l[0].v2
                                        m2 = self.sol

                                        m1.risultato()
                                        m2.risultato()
                                        E1 = equazione(m1, m2)
                                        E1.soluzione(v)
                                        self.sol.l.extend(E1.sol.l)
                                        # print(self.sol.l[-1].nome)
                                        return self.sol

                                if v in self.m1.l[0].v1.var:
                                    self.sol.append(self.m1.l[0].inversa(R, self.m1.l[0].v1))
                                    self.sol.risultato()
                                    R = self.sol

                                    if isinstance(self.m1.l[0].v1, variabile):
                                        return self.sol

                                    else:
                                        m1 = self.m1.l[0].v1
                                        m2 = self.sol

                                        m1.risultato()
                                        m2.risultato()
                                        E1 = equazione(m1, m2)
                                        E1.soluzione(v)
                                        self.sol.l.extend(E1.sol.l)
                                        # print(self.sol.l[-1].nome)
                                        return self.sol


                        if j==0:
                            self.m1.l[0].v.variabili()
                            if v in self.m1.l[0].v.var:

                                self.sol.l.append(self.m1.l[n - 1 - i].inversa(R, self.m1.l[n - 1 - i].v))
                                self.sol.risultato()
                                R = self.sol

                                if isinstance(self.m1.l[n - 1 - i].v, variabile):
                                    return self.sol

                                else:
                                    m1 = self.m1.l[n - 1 - i].v
                                    m2 = self.sol

                                    m1.risultato()
                                    m2.risultato()
                                    E1 = equazione(m1, m2)
                                    E1.soluzione(v)
                                    self.sol.l.extend(E1.sol.l)
                                    # print(self.sol.l[-1].nome)
                                    return self.sol



                elif isinstance(self.m1, variabile):
                    self.sol = self.m2
                    return self.sol
                else:  # se m1 non è variabile ne operazione
                    m1 = self.m1.v
                    m2 = self.m1.inversa(self.m2)
                    print(self.m2.nome)
                    # self.sol.l.append(m2)
                    E1 = equazione(m1, m2)
                    self.sol.l.extend(E1.soluzione(v).l)
                    return self.sol

            else:
                print('soluzione non trovata')
                return operazione()

    def soluzione1_old(self, v):


        self.variabili()
        if v in self.m2.var:
            E1=equazione(self.m2,self.m1)
            self.sol=E1.soluzione(v)
            return self.sol
        else:
            R=self.m2
            if v in self.m1.var:
                if isinstance(self.m1, operazione):
                    n=len(self.m1.l)
                    for i in range(n):
                        #print(self.m1.l[n - 1 - i].nome)
                        self.m1.l[n - 1 - i].v2.variabili()
                        if v in self.m1.l[n-1-i].v2.var:

                            self.sol.l.append(self.m1.l[n - 1 - i].inversa(R, self.m1.l[n - 1 - i].v2))
                            self.sol.risultato()
                            R=self.sol

                            if isinstance(self.m1.l[n - 1 - i].v2, variabile):
                                return self.sol

                            else:
                                m1 = self.m1.l[n - 1 - i].v2
                                m2 = self.sol

                                m1.risultato()
                                m2.risultato()
                                E1 = equazione(m1, m2)
                                E1.soluzione(v)
                                self.sol.l.extend(E1.sol.l)
                                # print(self.sol.l[-1].nome)
                                return self.sol
                    if n==0:
                        if v in self.m1.l[0].v2.var:
                            self.sol.append(self.m1.l[0].inversa(R, self.m1.l[0].v2))
                            self.sol.risultato()
                            R = self.sol

                            if isinstance(self.m1.l[0].v2, variabile):
                                return self.sol

                            else:
                                m1 = self.m1.l[0].v2
                                m2 = self.sol

                                m1.risultato()
                                m2.risultato()
                                E1 = equazione(m1, m2)
                                E1.soluzione(v)
                                self.sol.l.extend(E1.sol.l)
                                # print(self.sol.l[-1].nome)
                                return self.sol

                    if v in self.m1.l[0].v1.var:
                        self.sol.append(self.m1.l[0].inversa(R, self.m1.l[0].v1))
                        self.sol.risultato()
                        R = self.sol

                        if isinstance(self.m1.l[0].v1, variabile):
                            return self.sol

                        else:
                            m1 = self.m1.l[0].v1
                            m2 = self.sol

                            m1.risultato()
                            m2.risultato()
                            E1 = equazione(m1, m2)
                            E1.soluzione(v)
                            self.sol.l.extend(E1.sol.l)
                            # print(self.sol.l[-1].nome)
                            return self.sol
                elif isinstance(self.m1, variabile):
                    self.sol=self.m2
                    return self.sol
                else: #se m1 non è variabile ne operazione
                    m1=self.m1.v
                    m2=self.m1.inversa(self.m2)
                    print(self.m2.nome)
                    #self.sol.l.append(m2)
                    E1=equazione(m1, m2)
                    self.sol.l.extend(E1.soluzione(v).l)
                    return self.sol

            else:
                print('soluzione non trovata')
                return operazione()

'''
    def riduzione(self, v, res=None):

        n = len(self.m1.l)
        i = 0

        if res is None:
            R = self.m2
        else:
            R = res

        for i in range(n):

            if isinstance(self.m1.l[n - 1 - i].v2, variabile) :
                if v == self.m1.l[n - 1-i].v2:

                    print(v.nome, self.m1.l[n - 1 -i].v2.nome)
                    self.sol.l.append(self.m1.l[n - 1 -i].inversa(R, self.m1.l[n - 1 -i].v2))
                    return self.sol
                else:
                    self.sol.l.append(self.sol.l.append(self.m1.l[n - 1 -i].inversa(R, self.m1.l[n - 2 - i])))
            elif  v in self.m1.l[n - 1-i].v2.var :
                self.sol.l.append(self.m1.l[n - 1-i].inversa(R, self.m1.l[n - 1-i].v2))
                m1=self.m1.l[n - 1-i].v2
                m2=self.sol

                m2.risultato()
                E1=equazione(m1,m2)
                E1.soluzione(v)
                self.sol.l.extend(E1.sol.l)
                return self.sol

            else:
                self.sol.l.append(self.m1.l[n - 1 -i].inversa(R, self.m1.l[n - 2 - i]))

        if isinstance(self.m1.l[0].v1, variabile):
            if v == self.m1.l[0].v1:
                print(v.nome, self.m1.l[0].v1.nome)
                self.sol.l.append(self.m1.l[0].inversa(R, self.m1.l[0].v1))
                return self.sol

            else:
                print('variabile non trovata')
                return operazione()

        elif v in self.m1.l[0].v1.var:

            self.sol.l.append(self.m1.l[0].inversa(R, self.m1.l[0].v1))
            m1 = self.m1.l[0].v1
            m2 = self.sol
            #m2.append(self.m1.l[0].inversa(R, self.m1.l[0].v1))
            m2.risultato()
            E1 = equazione(m1, m2)
            E1.soluzione(v)
            self.sol.l.extend(E1.sol.l)
            return self.sol

        else:
            print('variabile non trovata')
            return operazione()



    def soluzione(self, v):

        if isinstance(self.m1, variabile):
            if v == self.m1:
                self.sol.l.append(self.m2)
                return self.sol
            else:
                E1 = equazione(self.m2, self.m1)
                self.sol = E1.soluzione(v)  # manca il caso in cui i membri sono entrambi variabili e diversi da quella cercata!!loop infinito
                return self.sol
        else:
            if isinstance(self.m2, variabile):
                if v == self.m2:
                    self.sol.l.append(self.m1)
                    return self.sol
                else:
                    self.sol = self.riduzione( v, self.m2)
            else:

                self.sol = self.riduzione(v, self.m2)

        if not self.sol.l:
            E1 = equazione(self.m2, self.m1)
            self.sol = E1.soluzione(v)

        if not self.sol.l:
            print('variabile non trovata')

        return self.sol




def solve_all(l, vf, res=None):
    n = len(l)
    if res is None:
        R=l[n-1].risultato()
    else:
        R=res
    sol = []
    sol.append(l[n - 1].inversa(R, l[n - 2].risultato()))

    for i in range(n - 2):
        sol.append(l[n - 2 - i].inversa(sol[i].risultato(), l[n - 3 - i].risultato()))
    sol.append(l[0].inversa(sol[n - 2].risultato(), vf))
    return sol


def soluzione_primo_membro(o, v, res=None):

    n = len(o.l)
    i=0
    sol = operazione()

    if res is None:
        R = o.l[n - 1].risultato()
    else:
        R = res

    if v.nome == o.l[n - 1].v2.nome:
        print(v.nome, o.l[n-1].v2.nome)
        sol.l.append(o.l[n - 1].inversa(R, o.l[n - 1].v2 ))
        return sol
    else:
        sol.l.append(o.l[n - 1].inversa(R, o.l[n - 2].risultato()))

    for i in range(n - 2):

        if v.nome == o.l[n-2-i].v2.nome:
            print(v.nome, o.l[n-2-i].v2.nome)
            sol.l.append(o.l[n-2-i].inversa( sol.l[i].risultato() , o.l[n-2-i].v2))
            return sol
        else:
            sol.l.append(o.l[n - 2 - i].inversa(sol.l[i].risultato(), o.l[n - 3 - i].risultato()))
            i+=1
    if v.nome == o.l[0].v1.nome or v.nome == o.l[0].v2.nome :
        print(v.nome, o.l[0].v2.nome)
        sol.l.append(o.l[0].inversa(sol.l[n - 2].risultato(), v))
    else:
        return []
    return sol

def soluzione_equazione(E, v):
    sol=operazione()


    if isinstance(self.m1,variabile):
        if v==self.m1:
            sol.l.append(E.m2)
            return sol
        else:
            E1=equazione(E.m2,E.m1)
            sol=soluzione_equazione(E1,v)#manca il caso in cui i membri sono entrambi variabili e diversi da quella cercata!!loop infinito
            return sol
    else:
        sol=soluzione_primo_membro(E.m1, v, E.m2.r)

    if not sol:
        E1 = equazione(E.m2, E.m1)
        sol=soluzione_equazione(E1, v)

    if not sol:
        print('variabile non trovata')

    return sol

'''





#PROVA

e=variabile()
e.valore=np.e
e.nome='e'

x=variabile()
y=variabile()
x.nome='x'
x.valore= 7
y.valore= 5
y.nome='y'
z=variabile()
z.nome='z'
z.valore= 10

d=variabile()
d.nome='d'
d.valore= 4

R=variabile()
R.nome='R'
R.valore=11

t=variabile()
t.nome='t'
t.valore=5

w=potenza(x,2)
v=potenza(d,2)

l=operazione()
l.l.append(piu(w, per(d,x)))
l.l.append(piu(l.l[0], d))
l.l.append(logaritmo(l.l[1],2))
l.risultato()
l.variabili()
l.grado()
l.tipo_operazione()

#l=meno(x, y)

#print(v.nome, v.valore)
'''
print(l.coefficiente(potenza(x,2)).nome)

E=equazione(l,t)
sol=E.prova_soluzione(x)

print(len(sol))
for s in sol:
    print(s.nome, s.valore)

#for v in l.var:
#    print(v.nome)
#for deg in l.grado_variabili:
#    print(deg[0],deg[1])
#print(len(l.tipo), l.tipo[0], l.tipo[1])

vt=l.tipo_var()
for v in vt:
    print(v[0])
    for t in v[1]:
        print( t)

'''
g=operazione()
g.l.append(piu(R,t))
g.risultato()
g.variabili()

E=equazione(l,g)
E.soluzione(x)
soluzioni=E.soluzioni
sol=E.sol
sol.risultato()
#print(sol.l[0].nome,sol.l[0].valore)
print(len(sol.l),sol.nome,sol.valore)
print(len(soluzioni))
#print(2**int(sol.l[0].valore))
#for s in sol:
#    print(s.nome, s.valore)





'''
print(piu(l,g).nome, piu(l,g).valore)
print(piu(l,R).nome, piu(l,R).valore)

print(l.r.nome,l.r.valore)
print(g.r.nome,g.r.valore)
sol=operazione()


U=equazione(l,g)
U.soluzione(t)
sol=U.sol
sol.risultato()

print(len(sol.l),sol.nome, sol.valore)
print(l.l[0].v1.nome, l.l[0].v1.relazione[0].m1.nome)
print(x.relazione[0].m1.nome)


'''