"Yang Xinyue CSMI M1"

import numpy as np
import matplotlib.pyplot as plt

def dp_H(q,p):

    return p

def dq_H(q,p):

    return 10*q/np.linalg.norm(q)**3

def euler_hamiltonian_solve(p0,q0,temps):
    N=len(temps)
    q = np.zeros((N,2))
    p = np.zeros((N,2))
    q[0] = q0
    p[0] = p0

    for i in range(N-1):
        dtn = temps[i + 1] - temps[i]
        p[i+1] = p[i] - dtn * dq_H(q[i], p[i])
        q[i+1] = q[i] + dtn * dp_H(q[i], p[i])

    return p,q


def rk4_hamiltonian_solve(p0,q0,temps):
    N = len(temps)
    q = np.zeros((N, 2))
    p = np.zeros((N, 2))
    q[0] = q0
    p[0] = p0

    for i in range(N - 1):
        dtn = temps[i + 1] - temps[i]

        [ kq0 , kp0 ] = [ dp_H(q[i],p[i]) , -dq_H(q[i],p[i]) ]
        [ kq1 , kp1 ] = [ dp_H(q[i]+(dtn/2)*kq0, p[i]+(dtn/2)*kp0) , -dq_H(q[i]+(dtn/2)*kq0, p[i]+(dtn/2)*kp0)]
        [ kq2 , kp2 ] = [ dp_H(q[i]+(dtn/2)*kq1, p[i]+(dtn/2)*kp1) , -dq_H(q[i]+(dtn/2)*kq1, p[i]+(dtn/2)*kp1)]
        [ kq3 , kp3 ] = [dp_H(q[i]+dtn*kq2, p[i]+dtn*kp2), -dq_H(q[i]+dtn*kq2, p[i]+dtn*kp2)]

        p[i + 1] = p[i] + dtn * (kp0+2*kp1+2*kp2+kp3)/6
        q[i + 1] = q[i] + dtn * (kq0+2*kq1+2*kq2+kq3)/6

    return p, q


def dp_H_sep(p):

    return p

def dq_H_sep(q):

    return 10*q/np.linalg.norm(q)**3

def euler_symplect_hamiltonian_separable_solve(p0,q0,temps):
    N = len(temps)
    q = np.zeros((N, 2))
    p = np.zeros((N, 2))
    q[0] = q0
    p[0] = p0

    for i in range(N-1):
        dtn = temps[i + 1] - temps[i]
        q[i + 1] = q[i] + dtn * dp_H_sep(p[i])
        p[i + 1] = p[i] - dtn * dq_H_sep(q[i+1])
    return p,q

def verlet_hamiltonian_separable_solve(p0,q0,temps):
    N = len(temps)
    q = np.zeros((N, 2))
    p = np.zeros((N, 2))
    q[0] = q0
    p[0] = p0
    for i in range(N-1):
        dtn = temps[i + 1] - temps[i]

        demiq = q[i] + (dtn / 2) * dp_H_sep(p[i])

        p[i + 1] = p[i] - (dtn / 2) * (dq_H_sep(demiq)+dq_H_sep(demiq))

        q[i + 1] = demiq + (dtn / 2) * p[i+1]

    return p,q


def energy(q,p):
    v = np.empty(len(q[:,0]))
    for i in range(len(q[:,0])):
        v[i]=1/2*np.linalg.norm(p[i])**2 - 10./np.linalg.norm(q[i])
    return v


p0 = [1,0]
q0 = [0,3]
test=1

if test == 1:
    N = 4000
    Tmax = 4

if test == 2:
    N = 40000
    Tmax = 4

if test == 3:
    N = 400000
    Tmax = 4

if test == 4:
    N = 4000
    Tmax = 8

if test == 5:
    N = 4000
    Tmax = 10

if test == 6:
    N = 4000
    Tmax = 20

temps = np.linspace(0,Tmax,N)
p1, q1 = euler_hamiltonian_solve(p0, q0, temps)
Y=energy(q1,p1)



p2, q2 = rk4_hamiltonian_solve(p0, q0, temps)
p3, q3 = euler_symplect_hamiltonian_separable_solve(p0,q0,temps)
p4, q4 = verlet_hamiltonian_separable_solve(p0,q0,temps)


plt.subplot(2, 1, 1)
plt.plot(q1[:, 0], q1[:, 1], label='$euler hamiltonian solve$ ', color='red', linewidth=1)
plt.plot(q2[:, 0], q2[:, 1], label='$rk4 hamiltonian solve$ ', color='blue', linewidth=1)
plt.plot(q3[:, 0], q3[:, 1], label='$euler symplect hamiltonian$ ', color='yellow', linewidth=1)
plt.plot(q4[:, 0], q4[:, 1], label='$verlet_hamiltonian_separable$ ', color='green', linewidth=1)
plt.subplot(2, 1, 2)
plt.plot(energy(q1,p1), label='$euler hamiltonian solve$ ', color='red', linewidth=1)
plt.plot(energy(q2,p2), label='$rk4 hamiltonian solve$ ', color='blue', linewidth=1)
plt.plot(energy(q3,p3), label='$euler symplect hamiltonian$ ', color='yellow', linewidth=1)
plt.plot(energy(q4,p4), label='$verlet_hamiltonian_separable$ ', color='green', linewidth=1)
plt.legend()
plt.show()

q2[:, 0] - q3[:, 0]
q2[:, 1] - q3[:, 1]

energy(q2,p2) == energy(q3,p3)

"conclusion"
"1 d'abord on faire le test==1, on peut voir que la courbe rouge est un peu differente avec les autre." \
"  Et les troisiemes courbes suvant sont meme" \
"2 pour les test 2,3, on change la valeur de N. Quand la valeur de N assez grand , les quatres" \
"  courbes sont meme" \
"3 pour les test 4,5,6 ,on varier le temps final (Tmax = 4,8,10,20),on peut voir que la courbe rouge " \
"  change, il a plusieurs cycle. pour les autre , il n'y a pas de change evidente ."



