import pandas
import pandas as pd
import math
import numpy as np

def k_medios(X, v, toleranciaKM, pesoExponencialKM):
    ready = False
    while not ready:
        ready = centCalc(X, v, toleranciaKM, pesoExponencialKM)


def centCalc(X, v, toleranciaKM, pesoExponencialKM):
    ready = True
    u = [[0 for x in range(len(X))] for y in range(len(v))]
    mNum = 0
    for index, m in X.iterrows():
        ds = []
        acum = 0.0
        for r in range(len(v)):
            c = v[r]
            d = 0.0
            for i in range(len(c)):
                d += math.pow(c[i] - m[i], 2);
            ds.append(math.pow(1 / d, 1 / (pesoExponencialKM - 1)))
            acum += math.pow(1 / d, 1 / (pesoExponencialKM - 1));
        for r in range(len(v)):
            u[r][mNum] = ds[r] / acum
        mNum += 1

    for i in range(len(v)):
        values = []
        for r in range(len(v[i])):
            values.append(0);
        acumB = 0.0
        for j in range(len(X)):
            m = X.iloc[[j]]
            acumB += math.pow(u[i][j], pesoExponencialKM)
            for k in range(len(values)):
                w = values[k]
                w += float(m[k]) * math.pow(u[i][j], pesoExponencialKM)
                values[k] = w
        acumC = 0.0
        for k in range(len(values)):
            w = values[k]
            w = w / acumB
            acumC += abs(w - v[i][k])
            values[k] = w
        v[i] = values
        if acumC > toleranciaKM:
            ready = False
    return ready


def lloyd(X, v, toleranciaL, iteracionesMaxL, razonAprendizajeL):
    ready = False
    iter = 0
    while not ready:
        iter = iter + 1
        centrosPrevios = v.copy()

        for index, m in X.iterrows():
            ganador = competicion(m, v)
            actualizaCentro(ganador, index, X, v, razonAprendizajeL)

        ready = calcTolerancia(v, centrosPrevios, toleranciaL)
        if iter == iteracionesMaxL:
            ready = True


def competicion(punto, v):
    indiceMejor = 0
    menorDist = distancia(punto, v[0])
    for j in range(len(v)):
        dist = distancia(punto, v[j])
        if dist < menorDist:
            menorDist = dist
            indiceMejor = j
    return indiceMejor


def distancia(punto, centro):
    distancia = 0
    for i in range(len(punto)):
        distancia += math.pow(punto[i] - centro[i], 2)
    return math.sqrt(distancia)


def actualizaCentro(iCentro, iPunto, X, v, razonAprendizajeL):
    for j in range(len(v[iCentro])):
        v[iCentro][j] = v[iCentro][j] + razonAprendizajeL * (X[j][iPunto] - v[iCentro][j])


def calcTolerancia(v, centrosPrevios, toleranciaL):
    for i in range(len(v)):
        if distancia(v[i], centrosPrevios[i]) >= toleranciaL:
            return False
    return True


def clasificacion(muestra, v, dic):
    acumulados = []
    acumD = 0.0
    for i in range(len(v)):
        acumA = 0.0
        for k in range(len(muestra)):
            acumA += math.pow(muestra[k] - v[i][k], 2)
        acumD += 1 / acumA
        acumulados.append(1 / acumA)
    max = 0.0
    indMax = -1
    for i in range(len(acumulados)):
        d = acumulados[i]
        d = d / acumD
        acumulados[i] = d
        if d > max:
            max = d
            indMax = i
    if indMax != -1:
        print("Predecimos que la muestra pertenece a la clase: " + str(dic[indMax]) + "(" + str(
            indMax) + ")\t\tLa clase a la que deber??a pertenecer es: " + muestra[4][0])


def bayes(X, y):
    x1 = X[y == 'Iris-setosa']
    x2 = X[y == 'Iris-versicolor']
    m1 = x1.mean()
    C1 = x1.cov()
    m2 = x2.mean()
    C2 = x2.cov()
    return m1, C1, m2, C2


def bayesClasificador(punto, w):
    m1, C1, m2, C2 = w
    p1 = probBayes(punto, m1, C1)
    p2 = probBayes(punto, m2, C2)
    if (p1 > p2):
        print("Predecimos que la muestra pertenece a la clase: Iris-setosa. La clase a la que deberia pertenecer es " +
              punto[4][0])
    else:
        print(
            "Predecimos que la muestra pertenece a la clase: Iris-versicolor. La clase a la que deberia pertenecer es " +
            punto[4][0])


def probBayes(punto, m, c):
    aux = punto.loc[0][:4] - m
    fraccion = 1 / (math.pow(2 * math.pi, 2) * math.pow(np.linalg.det(c.to_numpy()), 1 / 2))
    exponente = math.exp((-1 / 2) * np.matmul(np.matmul(aux.transpose(), np.linalg.inv(c.to_numpy())), aux))
    return fraccion * exponente

def main():
    Xy = pd.read_csv('Iris2Clases.txt', sep=",", header=None)
    y = Xy[4]
    a0 = "Iris-setosa"
    a1 = "Iris-versicolor"
    dic = {0: a0, 1: a1}

    X = Xy.drop(Xy.columns[4], axis=1)

    y1 = pd.read_csv('TestIris01.txt', sep=",", header=None)
    y2 = pd.read_csv('TestIris02.txt', sep=",", header=None)
    y3 = pd.read_csv('TestIris03.txt', sep=",", header=None)

    vOriginales = [[4.6, 3.0, 4.0, 0.0],
                   [6.8, 3.4, 4.6, 0.7]]

    toleranciaKM = 0.01
    pesoExponencialKM = 2

    toleranciaL = math.pow(10, -10)
    iteracionesMaxL = 10
    razonAprendizajeL = 0.1

    toleranciaSOM = math.pow(10, -6)
    iteracionesMaxSOM = 1000
    razonAprendizajeSOM = 0.1
    alfaIni = 0.1
    alfaFin = 0.01
    ## Consideramos que un centro se actualiza cuando K T ?? ( ) k > , siendo T = 10^-5
    T = math.pow(10, -5)

    print("\nKMeans:")
    vKm = vOriginales.copy()
    k_medios(X, vKm, toleranciaKM, pesoExponencialKM)
    clasificacion(y1, vKm, dic)
    clasificacion(y2, vKm, dic)
    clasificacion(y3, vKm, dic)

    print("\nBayes:")
    w = bayes(X, y)
    bayesClasificador(y1, w)
    bayesClasificador(y2, w)
    bayesClasificador(y3, w)

    print("\nLloyd:")
    vL = vOriginales.copy()
    lloyd(X, vL, toleranciaL, iteracionesMaxL, razonAprendizajeL)
    clasificacion(y1, vL, dic)
    clasificacion(y2, vL, dic)
    clasificacion(y3, vL, dic)


main()
