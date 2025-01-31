import numpy as np

import operatori as o


class moto_rett_unif:

    def __init__(self):

        self.x = o.variabile()
        self.x.nome = 'posizione'
        self.x0 = o.variabile()
        self.x0.nome = 'posizione iniziale'
        self.v0 = o.variabile()
        self.v0.nome = 'velocità iniziale'
        self.t = o.variabile()
        self.t.nome = 'tempo'
        self.var = [self.x, self.x0, self.v0, self.t]

    def legge_oraria(self):
        m1 = self.x
        m2=o.operazione()
        m2.l.append(o.per(self.v0, self.t))
        m2.l.append(o.piu(m2.l[0], self.x0))
        m2.risultato()
        self.l_o = o.equazione(m1,m2)
        self.l_o.nome = 'Legge oraria moto uniforme'
        self.l_o.relazioni()
        self.l_o.variabili()


class moto_unif_acc:

    def __init__(self):

        self.x = o.variabile()
        self.x.nome = 'posizione'
        self.x0 = o.variabile()
        self.x0.nome = 'posizione iniziale'
        self.v0 = o.variabile()
        self.v0.nome = 'velocità iniziale'
        self.v = o.variabile()
        self.v.nome = 'velocità'
        self.t = o.variabile()
        self.t.nome = 'tempo'
        self.a = o.variabile()
        self.a.nome = 'accelerazione'
        self.var = [self.x, self.x0, self.v0, self.t, self.a, self.v]

    def legge_oraria(self):

        self.cost = o.variabile()
        self.cost.nome = 'costante'
        self.cost.valore=0.5
        m1 = self.x
        m2 = o.operazione()

        l1 = o.operazione()

        l1.l.append(o.potenza(self.t, 2))
        l1.l.append(o.per(l1.l[0], self.a))
        l1.l.append(o.per(l1.l[1], self.cost))
        l1.risultato()
        l1.variabili()
        #print(l1.var)

        l2 = o.operazione()
        l2.l.append(o.per(self.v0, self.t))
        l2.risultato()
        l2.variabili()

        m2.l.append(o.piu(l1, l2))
        m2.l.append(o.piu(m2.l[0], self.x0))
        m2.risultato()
        m2.variabili()

        self.l_o = o.equazione(m1, m2)
        self.l_o.nome = 'Legge oraria moto uniformemente accelerato'
        self.l_o.relazioni()
        self.l_o.variabili()

    def legge_velocita(self):

        m2 = o.operazione()
        m2.l.append(o.per(self.a, self.t))
        m2.l.append(o.piu(m2.l[0], self.v0))
        m2.risultato()

        self.l_v = o.equazione(self.v, m2)
        self.l_v.nome = 'Legge della velocità'
        self.l_v.relazioni()
        self.l_v.variabili()

    def legge_velocita_spazio(self):

        c = o.variabile()
        c.nome = 'costante'
        c.valore = 2
        m1 = o.operazione()
        m1.l.append(o.meno(o.potenza(self.v, 2), o.potenza(self.v0, 2)))
        m1.risultato()
        m2 = o.operazione()
        m2.l.append(o.per(o.per(c, o.meno(self.x, self.x0)), self.a))
        m2.risultato
        self.l_v_x=o.equazione(m1,  m2)
        self.l_v_x.nome = 'Legge della velocità in funzione dello spazio'
        self.l_v_x.relazioni()
        self.l_v_x.variabili()


class dinamica:

    def __init__(self):

        #self.x = o.variabile()
        #self.x.nome = 'posizione'
        self.F = o.variabile()
        self.F.nome = 'forza'
        self.m = o.variabile()
        self.m.nome = 'massa'
        self.a = o.variabile()
        self.a.nome = 'accelerazione'

        self.g = o.variabile()
        self.g.nome='costante'
        self.g.valore=9.81

        self.var = [ self.F, self.m, self.a, self.g] #self.x,

    def legge_Newton(self):

        m2 = o.operazione()
        m2.l.append(o.per(self.m, self.a))
        m2.risultato()
        m2.variabili()

        self.l_N = o.equazione(self.F, m2)
        self.l_N.nome = 'Legge di Newton'
        self.l_N.relazioni()
        self.l_N.variabili()


class molla(dinamica):

    def __init__(self):

        super().__init__()
        self.x = o.variabile()
        self.x.nome = 'posizione'
        self.k = o.variabile()
        self.k.nome = 'costante elastica'

        self.var.extend([self.x, self.k])

    def legge_Hooke(self):

        m2 = o.operazione()
        m2.l.append(o.per(self.k, self.x.opposto))
        m2.risultato()

        self.l_H = o.equazione(self.F, m2)
        self.l_H.nome = 'Legge di Hooke'
        self.l_H.relazioni()
        self.l_H.variabili()


class piano_inclinato(dinamica): #bisogna introdurre gli operatori goniometrici

    def __init__(self):

        super().__init__()

        self.l = o.variabile()
        self.l.nome = 'lunghezza'
        self.h = o.variabile()
        self.h.nome = 'altezza'
        self.angolo = o.variabile()
        self.angolo.nome = 'angolo inclinazione'

        self.T = o.variabile()
        self.T.nome = 'reazione vincolare'

        self.var.extend([self.l, self.h, self.angolo, self.T])

    def componente_x(self):

        m2=o.operazione()
        m2.l.append(o.per(self.g, o.seno(self.angolo)))
        m2.risultato()
        self.c_x = o.equazione(self.a, m2)
        self.c_x.nome = 'componente x'
        self.c_x.relazioni()
        self.c_x.variabili()

    def componente_y(self):

        m2=o.operazione()
        m2.l.append(o.per(self.m, self.g))
        m2.l.append(o.per(m2.l[0], o.coseno(self.angolo) ))
        m2.risultato()

        self.c_y = o.equazione(self.T, m2)
        self.c_y.nome = 'componente y'
        self.c_y.relazioni()
        self.c_y.variabili()


class elettrostatica(dinamica):

    def __init__(self):

        super().__init__()
        self.q = o.variabile()
        self.q.nome = 'carica'

        self.q1 = o.variabile()
        self.q1.nome = 'carica 1'

        self.E = o.variabile()
        self.E.nome = 'campo elettrico'

        self.k = o.operazione()
        self.k.nome = 'costante dielettrica'

        self.epsilon0=o.variabile()
        self.epsilon0='costante dielettrica assoluta'
        self.epsilon0.valore=8,85418762*(10**(-12))

        self.epsilonr = o.variabile()
        self.epsilonr = 'costante dielettrica relativa'
        self.epsilonr.valore = 1

        quattro=o.variabile()
        quattro.nome='costante'
        quattro.valore=4

        pi=o.variabile()
        pi.nome='costante'
        pi.valore=np.pi

        self.k.l.append(per(per(quattro,pi),per(self.epsilon0,self.epsilon)))
        self.k.risultato()
        self.k.nome = 'costante dielettrica'

        self.var.extend([self.q, self.q1, self.E, self.epsilon0, self.epsilonr])

    def forza_campo_elettrico(self):

        m2=o.operazione()
        m2.l.append(per(self.q, self.E))
        m2.risultato()

        self.F_q_E=o.equazione(F, m2)
        self.F_q_E.relazioni()
        self.F_q_E.variabili()

    def legge_Coulomb(self):

        self.d = o.variabile()
        self.d.nome = 'distanza'

        self.var.appen(self.d)

        m2=o.operazione()
        m2.l.append(diviso(per(self.q, self.q1), o.potenza(self.d, 2)))
        m2.l.append(diviso(m2.l[0], self.k))
        m2.risultato()

        self.l_C = o.equazione(self.F, m2)
        self.l_C.relazioni()
        self.l_C.variabili()


class piano_infinito(elettrostatica):

    def __init__(self):

        super().__init__()
        self.S = o.variabile()
        self.S.nome = 'superficie del piano'

        self.Q = o.variabile()
        self.Q.nome = 'carica contenuta nel piano'

        self.sigma = o.variabile()
        self.sigma.nome = 'densità superficiale di carica'

        self.var.extend([self.Q, self.S, self.sigma])

    def campo_elettrico(self):

        m = o.operazione()
        m.l.append(o.diviso(self.Q, self.S))
        m.risultato()
        self.densita_carica_superficiale = o.equazione(self.sigma, m)
        self.densita_carica_superficiale.relazioni()
        self.densita_carica_superficiale.variabili()

        due = o.variabile()
        due.nome = 'costante'
        due.valore = 2

        m2 = o.operazione()
        m2.l.append(o.diviso(self.sigma), per(due,per(self.epsilon0, self.epsilonr)))

        self.c_e = o.equazione(self.E, m2)
        self.c_e.relazioni()
        self.c_e.variabili()


class filo_infinito(elettrostatica):

    def __init__(self):

        super().__init__()
        self.Q = o.variabile()
        self.Q.nome = 'carica contenuta nel filo'
        self.L = o.variabile()
        self.L.nome = 'lunghezza del filo'
        self.d_lin = o.variabile()
        self.d_lin.nome = 'densità lineare di carica'
        self.d = o.variabile()
        self.d.nome = 'distanza'

        self.var.extend([self.Q, self.L, self.d_lin, self.d])

    def campo_elettrico(self):

        m = o.operazione()
        m.l.append(o.diviso(self.Q, self.L))
        m.risultato()
        self.densita_carica_lineare = o.equazione(self.d_lin, m)
        self.densita_carica_lineare.relazioni()
        self.densita_carica_lineare.variabili()

        due = o.variabile()
        due.nome = 'costante'
        due.valore = 2

        pi = o.variabile()
        pi.nome = 'pi'
        pi.valore = np.pi

        m2 = o.operazione()
        m2.l.append(o.diviso(self.d_lin, self.d))
        m2.l.append(o.diviso(m2.l[0], o.per(due, o.per(pi, o.per(self.epsilon0, self.epsilonr)))))
        m2.risultato()

        self.c_e = o.equazione(self.E, m2)
        self.c_e.relazioni()
        self.c_e.variabili()



#PROVA
'''
P=piano_inclinato()
for v in P.var:
    print(v.nome)


sol=o.operazione()
M=moto_unif_acc()
M.x0.valore=2
M.x.valore=10
#M.a.valore=4
M.t.valore=20
M.v0.valore=6
M.legge_oraria()

sol=M.l_o.soluzione(M.a)
#sol=M.l_o.sol
M.a.valore=sol.risultato().valore

M.legge_velocita()
sol1=o.operazione()
sol1=M.legge_velocita.soluzione(M.v)
sol1.risultato()


sol2=o.operazione()
D=dinamica()
D.F.valore=-30
#D.m.valore=3
D.a=M.a
D.legge_newton()
sol2=D.l_N.soluzione(D.m)
sol2.risultato()


print(len(sol.l),sol.l[-1].nome, sol.l[-1].valore)

print(len(sol1.l),sol1.l[-1].nome, sol1.l[-1].valore)

print(len(sol2.l),sol2.l[-1].nome, sol2.l[-1].valore)

M.legge_velocita.variabili()
print(len(M.l_v.var))
for v in M.l_v.var:
    print(v.nome)

'''