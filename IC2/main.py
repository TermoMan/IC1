import pandas as pd
import math


class Node(object):
    def __init__(self):
        self.data = ""
        self.children = []
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def add_child(self, obj):
        self.children.append(obj)

    def add_data(self, data):
        self.data = data

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + self.data)
        if self.children:
            for child in self.children:
                child.print_tree()


def infor(p, n):
    if (p == 0) or (n == 0):
        return 0
    return -p * math.log(p, 2) - n * math.log(n, 2)


def merito(lista_ejemplos, atrib):
    n = lista_ejemplos.Jugar.count()
    sum = 0
    for act in lista_ejemplos[atrib].unique():
        p_act = lista_ejemplos[atrib][(lista_ejemplos[atrib] == act) & (lista_ejemplos["Jugar"] == "si")].count() / \
                lista_ejemplos[atrib][lista_ejemplos[atrib] == act].count()
        n_act = lista_ejemplos[atrib][(lista_ejemplos[atrib] == act) & (lista_ejemplos["Jugar"] == "no")].count() / \
                lista_ejemplos[atrib][lista_ejemplos[atrib] == act].count()
        sum += (lista_ejemplos[atrib][lista_ejemplos[atrib] == act].count() / n) * infor(p_act, n_act)

    return sum


def mejorElem(lista_ejemplos, lista_atributos):
    mejorAct = ""
    meritoActual = 100
    for atr in lista_atributos:
        a = merito(lista_ejemplos, atr)
        if a < meritoActual:
            meritoActual = a
            mejorAct = atr

    return mejorAct


def id3(arbol, lista_ejemplos, lista_atributos):
    if lista_ejemplos.empty:
        arbol.add_data("empty")
        return "empty"
    elif lista_ejemplos['Jugar'].eq("no").all():
        arbol.add_data("-")
        return "-"
    elif lista_ejemplos['Jugar'].eq("si").all():
        arbol.add_data("+")
        return "+"
    elif not lista_atributos:
        print("error")
        return "error"
    else:
        
        best = mejorElem(lista_ejemplos, lista_atributos)
        arbol.add_data(best)
        lista_atributos.remove(best)
        for act in lista_ejemplos[best].unique():
            chld = Node()
            chld.set_parent(arbol)
            arbol.add_child(chld)
            ejemplos_restantes = lista_ejemplos.drop(lista_ejemplos[lista_ejemplos[best] != act].index)
            id3(chld, ejemplos_restantes, lista_atributos)



def main():
    lista_ejemplos = pd.read_csv('Juego.txt', sep=",", header=None)
    lista_atributos = []
    with open('AtributosJuego.txt', encoding="utf8") as fp:
        for line in fp:
            lista_atributos = [x.strip() for x in line.split(',')]

    lista_ejemplos.columns = lista_atributos
    lista_atributos.remove("Jugar")
    arbol = Node()

    id3(arbol, lista_ejemplos, lista_atributos)
    arbol.print_tree()


main()
