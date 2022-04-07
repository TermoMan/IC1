import pandas as pd
import math



def k_medios(X, v, toleranciaKM, pesoExponencialKM):
    ready = False
    while not ready:
        ready = centCalc(X, v, toleranciaKM, pesoExponencialKM)
    for i in range(len(v)):
        print(str(v[i]))


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
            ds.append(math.pow(1/d, 1/(pesoExponencialKM-1)))
            acum += math.pow(1/d, 1/(pesoExponencialKM-1));
        for r in range(len(v)):
            u[r][mNum] = ds[r]/acum
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
            w = w/acumB
            acumC += abs(w - v[i][k])
            values[k] = w
        v[i] = values
        if acumC > toleranciaKM:
            ready = False
    return ready

def clasificacionKM(muestra, v, dic):
    acumulados = []
    acumD = 0.0
    for i in range(len(v)):
        acumA = 0.0
        for k in range(len(muestra)):
            acumA += math.pow(muestra[k] - v[i][k], 2)
        acumD += 1/acumA
        acumulados.append(1/acumA)
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
        print("Predecimos que la muestra pertenece a la clase: " + str(dic[indMax])+"("+str(indMax)+")\t\tLa clase a la que debería pertenecer es: " +muestra[4][0])



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

    v = [[4.6, 3.0, 4.0, 0.0],
         [6.8, 3.4, 4.6, 0.7]]

    toleranciaKM = 0.01
    pesoExponencialKM = 2

    toleranciaL = math.pow(10,-10)
    iteracionesMaxL = 10
    razonAprendizajeL = 0.1

    toleranciaSOM = math.pow(10, -6)
    iteracionesMaxSOM = 1000
    razonAprendizajeSOM = 0.1
    alfaIni = 0.1
    alfaFin = 0.01
    ## Consideramos que un centro se actualiza cuando K T α ( ) k > , siendo T = 10^-5
    T = math.pow(10, -5)

    k_medios(X, v, toleranciaKM, pesoExponencialKM)
    clasificacionKM(y1, v, dic)
    clasificacionKM(y2, v, dic)
    clasificacionKM(y3, v, dic)


main()