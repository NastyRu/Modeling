import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from math import *

tableI = [0.5, 1, 5, 10, 50, 200, 400, 800, 1200]
tableT0 = [6700, 6790, 7150, 7270, 8010, 9185, 10010, 11140, 12010]
tableM = [0.5, 0.55, 1.7, 3.0, 11.0, 32.0, 40.0, 41.0, 39.0]

tableT = [4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000]
tableSigma = [0.031, 0.27, 2.05, 6.06, 12.0, 19.9, 29.6, 41.1, 54.1, 67.7, 81.5]

tw = 2000
grp = 0
gt0 = 0

Igraph = []
Ugraph = []
Tgraph = []
RPgraph = []
T0graph = []

def graf():
    gridsize = (3, 2)
    fig = plt.figure(figsize=(12, 8))
    ax1 = plt.subplot2grid(gridsize, (0, 0))
    ax1.set_xlabel('$t$')
    ax1.set_ylabel('$I$')

    ax2 = plt.subplot2grid(gridsize, (0, 1))
    ax2.set_xlabel('$t$')
    ax2.set_ylabel('$U$')

    ax3 = plt.subplot2grid(gridsize, (1, 0))
    ax3.set_xlabel('$t$')
    ax3.set_ylabel('$Rp$')

    ax4 = plt.subplot2grid(gridsize, (1, 1))
    ax4.set_xlabel('$t$')
    ax4.set_ylabel('$To$')

    ax5 = plt.subplot2grid(gridsize, (2, 0))
    ax5.set_xlabel('$t$')
    ax5.set_ylabel('$I*Rp$')

    ax1.plot(Tgraph, Igraph)
    ax2.plot(Tgraph, Ugraph)
    ax3.plot(Tgraph, RPgraph)
    ax4.plot(Tgraph, T0graph)

    IRPgraph = [x * y for x, y in zip(Igraph, RPgraph)]
    ax5.plot(Tgraph, IRPgraph)

    plt.show()

def interpolation(Y, tableY, table):
    imax = 0
    imin = 0
    for i in range(len(tableY)):
        if (Y > tableY[i]):
            imax = i
        else:
            imax = i
            break
    if (0 == imax):
        imax = 1
    imin = imax - 1

    return table[imin] + (table[imax] - table[imin]) / (tableY[imax] - tableY[imin]) * (Y - tableY[imin])

def Fint(I, z):
    t0 = interpolation(I, tableI, tableT0)
    global gt0
    gt0 = t0
    m = interpolation(I, tableI, tableM)
    t = t0 + (tw - t0) * (z ** m)
    sigma = interpolation(t, tableT, tableSigma)

    return sigma * z

def iint(I):
    a = 0
    b = 1
    n = 100
    h = (b - a) / n
    s = (Fint(I, a) + Fint(I, b)) / 2
    x = 0

    for i in range(n - 1):
        x = x + h
        s = s + Fint(I, x)
    s = s * h

    return s

def Rp(le, R, I):
    return le / (2 * pi * R * R * iint(I))

def f(I, U, le, R, Lk, Rk):
    global grp
    grp = Rp(le, R, fabs(I))
    return (U - (Rk + grp) * I) / Lk

def Inext(I, U, le, R, Lk, hn, Rk, Ck):
    k1 = f(I, U, le, R, Lk, Rk)
    q1 = g(I, Ck)
    k2 = f(I + hn * k1 / 2, U + hn * q1 / 2, le, R, Lk, Rk)
    q2 = g(I + hn * k1 / 2, Ck)
    k3 = f(I + hn * k2 / 2, U + hn * q2 / 2, le, R, Lk, Rk)
    q3 = g(I + hn * k2 / 2, Ck)
    k4 = f(I + hn * k3, U + hn * q3, le, R, Lk, Rk)
    q4 = g(I + hn * k3, Ck)
    return I + hn * (k1 + 2 * k2 + 2 * k3 + k4) / 6

def g(I, Ck):
    return -I / Ck

def Unext(I, U, le, R, Lk, hn, Rk, Ck):
    k1 = f(I, U, le, R, Lk, Rk)
    q1 = g(I, Ck)
    k2 = f(I + hn * k1 / 2, U + hn * q1 / 2, le, R, Lk, Rk)
    q2 = g(I + hn * k1 / 2, Ck)
    k3 = f(I + hn * k2 / 2, U + hn * q2 / 2, le, R, Lk, Rk)
    q3 = g(I + hn * k2 / 2, Ck)
    k4 = f(I + hn * k3, U + hn * q3, le, R, Lk, Rk)
    q4 = g(I + hn * k3, Ck)
    return U + hn * (q1 + 2 * q2 + 2 * q3 + q4) / 6

def main():
    R = 0.35
    le = 12
    Lk = 0.000187
    Ck = 0.000268
    Rk = 0.25
    Uc = 1400
    I = 0
    hn = 0.000001
    t = 0

    for i in range(1200):
        I = Inext(I, Uc, le, R, Lk, hn, Rk, Ck)
        Uc = Unext(I, Uc, le, R, Lk, hn, Rk, Ck)
        t += hn

        Igraph.append(I)
        Ugraph.append(Uc)
        Tgraph.append(t)
        RPgraph.append(grp)
        T0graph.append(gt0)

    graf()

if __name__ == "__main__":
    main()
