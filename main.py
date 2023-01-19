import io
import os
import random
from recordtype import recordtype
# ------------------------------------------------------------------------------------------------------

### ZMIENNE GLOBALNE ###
sequence = "" # sekwencja orginalna
var = [] # tablica oligonukleotydow
lenOfDNA = 0 # dlugosc lancucha wyjsciowego
lenOfSample = 0 # dlugosc oligonukleoty

numEdges = 0 # ilosc krawedzi
numVertices = 0 # ilosc wierzcholkow

graph = [] # macierz sasiectwa
structInGraph = recordtype("struct", "inside outside offset") # dane wewnatrz grafu
oligo = {} # slownik oligonukleotydow do nawigacji po grafie
oligoUpSideDown = {} # slownik oligonukleotydow do nawigacji po grafie od tylu
structInOligo = recordtype("struct", "inside outside position") # dane wewnatrz slownika oligo

visitedVertex = [] # odwiedzone wierzchoki przy sprawdzaniu czy graf jest laczny
startingPoint = "Hello World!"
resolved = [] # rozwiazanie
#sequence, var, lenOfDNA, lenOfSample, numEdges, numVertices
#graph, structInGraph, oligo, oligoUpSideDown, structInOligo

# czyszczenie brudnych zmiennych
def clearVariables():
    global sequence, var, lenOfDNA, lenOfSample, numEdges, numVertices, graph, structInGraph
    global oligo, oligoUpSideDown, structInOligo, visitedVertex, startingPoint, resolved
    sequence = "" # sekwencja orginalna
    var = [] # tablica oligonukleotydow
    lenOfDNA = 0 # dlugosc lancucha wyjsciowego
    lenOfSample = 0 # dlugosc oligonukleoty

    numEdges = 0 # ilosc krawedzi
    numVertices = 0 # ilosc wierzcholkow

    graph = [] # macierz sasiectwa
    structInGraph = recordtype("struct", "inside outside offset") # dane wewnatrz grafu
    oligo = {} # slownik oligonukleotydow do nawigacji po grafie
    oligoUpSideDown = {} # slownik oligonukleotydow do nawigacji po grafie od tylu
    structInOligo = recordtype("struct", "inside outside position") # dane wewnatrz slownika oligo

    visitedVertex = [] # odwiedzone wierzchoki przy sprawdzaniu czy graf jest laczny
    startingPoint = "Hello World!"
    resolved = [] # rozwiazanie
# -----------------------------------------------------------------------------------------------------

### PRZYGOTOWANIE DANYCH ###
def dateFrom_File():
    global sequence, var, lenOfDNA, lenOfSample, numEdges, numVertices

    # pobieranie danych z pliku
    dateFromFile = []
    f = open("nset.txt", "r")
    for x in f:
        dateFromFile.append(x.split("\n")[0])

    sequence, var = dateFromFile[0], dateFromFile[1:]
    lenOfDNA = len(sequence)
    lenOfSample = len(var[0])

    print("Szukana sekwencja:", sequence)
    print("Oligonukleotydy:", var)
    print()

def testDate(filename):
    global sequence, var, lenOfDNA, lenOfSample, numEdges, numVertices

    # pobieranie danych z pliku
    dateFromFile = []
    f = open(filename, "r")
    for x in f:
        dateFromFile.append(x.split("\n")[0])
    var = dateFromFile
    lenOfSample = len(var[0])
    sequence = "unknown"

    print("Nazwa pliku: " + filename)
    choose = input("podaj dlugosc sekwencji wyjsciowej\n")
    lenOfDNA = int(choose)

def dateFrom_Generator():
    global sequence, var, lenOfDNA, lenOfSample, numEdges, numVertices

    # tworzenie danych
    print("podaj 2 liczby rozdzielone spacja: n (dlugosc DNA) i l (dlugosc probki)\nwieksza rozbieznosc miedzy n a l spowoduje ze bedzie wiecej bledow wynikajacych z powtorek\npolecam unikac jezeli nie chesz akurat tego sprawdzac\n PS. jezeli chcesz poogladac wredne przypadki wpisz 10 3 na cykle i doeulerowanie i 50 3 na problem przy dodaniu wystarczajacej ilosci krawedzi\n a pozniej nie musisz nawet dodawac nowych rodzacjow bledow jesli wypadly jakies powtorzenia\n przyjazne dane bez powtorzen to np 10 4 i 100 7")
    tmp = input().split()
    print(tmp[0])
    lenOfDNA = int(tmp[0])
    lenOfSample = int(tmp[1])

    sequence = ""
    for i in range(lenOfDNA):
        rand = random.randint(0, 3)
        if (rand == 0):
            sequence = "A" + sequence
        elif (rand == 1):
            sequence = "C" + sequence
        elif (rand == 2):
            sequence = "G" + sequence
        elif (rand == 3):
            sequence = "T" + sequence
        # z niewiadmoych mi przyczyn match case mi nie dziala ...

    var = []
    for it in range(lenOfSample, lenOfDNA + 1):
        var.append(sequence[it - lenOfSample:it])

    print("Szukana sekwencja:", sequence)
    print("Oligonukleotydy z powtorzeniami:", var)

    ### WRZUCIC DO IFa
    dublicates = len(var) - len(list(set(var)))
    var = list(set(var))
    print("Oligonukleotydy bez powtorzen:", var)
    print("wypadlo: ", dublicates, "oligonukleotydow")
    print()
    ###

    print("podaj 2 liczby rozdzielone spacja: dodanie bledow 1 (pozytywnych) , 2 (negatywnych), 3 (oba) , 4 (bez zmian) i ilosc bledow")
    choose = input()
    choose = choose.split(" ")
    if (int(choose[0]) < 4):  # dodane by nie bylo trzbe podawac ilosci bledow jezeli sie chce pozostawic dane bez mian
        choose[1] = int(choose[1])

    if (choose[0] == "1"):  # pozytywne
        print("pozytywne, trzeba dodac jakies krawedzie i stworzyc algoryt")
        exit(0)
    elif (choose[0] == "2"):  # negatywne
        while (choose[1] != 0):
            var.pop(random.randrange(1, len(var) - 1))  # Nie wywala ostatniego i pierwszego, to na pozniej
            choose[1] -= 1
        print("Oligonukleotydy po odjeciu: ", var)
        print()
    elif (choose[0] == "3"):  # oba
        print("oba, trzeba dodac oba rodzaje bledow i stworzyc algorytm")
        exit(0)

    print("Szukana sekwencja:", sequence)
    print("Oligonukleotydy:", var)
    print()
# -----------------------------------------------------------------------------------------------------

### TWORZENIE GRAFU ###
#macierz sasiectwa "z potrojna warstwa danych 'in i out i offset' nawigacja slownikem zapamietujacy ilosc wchodzacych i wychodzacych lukow
def create_Graph():
    global sequence, var, lenOfDNA, lenOfSample, numEdges, numVertices
    global graph, structInGraph, oligo, oligoUpSideDown, structInOligo

    # inicjacja tablicy sasiectwa
    divs = []
    for it in var:
        divs.append(it[1:])
        divs.append(it[:-1])
    oligo = dict.fromkeys(divs)

    for it in oligo:
        oligo[it] = structInOligo(0, 0, numVertices)
        oligoUpSideDown[numVertices] = it
        numVertices += 1

    numEdges = lenOfDNA - lenOfSample + 1 # bo pracujemy na grafie na krawedziowym
    print(oligo)

    graph = [[None for y in range(numVertices)] for x in range(numVertices)]
    for i in range(numVertices):
        for j in range(numVertices):
            graph[i][j] = structInGraph(0, 0, 0)

    # wypelnianie macierzy sasiectwa jak u pevznera wtedy tez offset trzeba na jeden mniej
    #for i in range(len(var)):
    #    graph[oligo[var[i][:-1]].position][oligo[var[i][1:]].position].outside += 1
    #    oligo[var[i][:-1]].outside += 1
    #    graph[oligo[var[i][1:]].position][oligo[var[i][:-1]].position].inside += 1
    #    oligo[var[i][1:]].inside += 1

    # wypelnianie macierzy sasiectwa z wszystkimi krawedziami
    numEdges=0
    for i in oligo:
        for j in oligo:
            if(i == j):
                continue
            if(i[1:] == j[:-1]):
                numEdges+=1
                graph[oligo[i].position][oligo[j].position].outside += 1
                oligo[i].outside += 1
                graph[oligo[j].position][oligo[i].position].inside += 1
                oligo[j].inside += 1
def show_Graph():
    global sequence, var, lenOfDNA, lenOfSample, numEdges, numVertices
    global graph, structInGraph, oligo, oligoUpSideDown, structInOligo

    # wyswietlanie macierzy sasiectwa
    for it in oligo:
        #print("\t\t", it, end="\t")
        print("\t", it, end="\t")
    print()
    for it in oligo:
        print(it, end="\t\t")
        for it2 in range(numVertices):
            print(graph[oligo[it].position][it2].outside, graph[oligo[it].position][it2].inside, sep="\t",
                  end="\t\t")
        print()
    print("in/out", end="\t")
    for it in oligo:
        print(oligo[it].inside, oligo[it].outside, sep="\t", end="\t\t")
    print()

    print(
        "Ogladajac w poziomie: 1 na pierwszym polu oznacza luk skierowany z elementu kolumny do elementu wiersza")
    print("ogladajac w pionie: mozna dla kazdego oligonukleotydu odczytac ilosc lokow wchodzacych i wychodzacych")
    print()
# -----------------------------------------------------------------------------------------------------

### PRZYGOTYWOWANIE GRAFU DO DFS ###
def preparing_Graph():
    global sequence, var, lenOfDNA, lenOfSample, numEdges, numVertices
    global graph, structInGraph, oligo, oligoUpSideDown, structInOligo
    global visitedVertex

    #zadbanie o lacznosc grafu
    while(True):
        visitedVertex = []
        if_connected_Graph(oligoUpSideDown[0])
        tmp = []
        for element in oligo:
            if element not in visitedVertex:
                tmp.append(element)
        print("preparing_Graph: VisitedVertex- ", visitedVertex)
        print("preparing_Graph: tmp- ", tmp, "\n")
        if numVertices-2 <= len(visitedVertex): # dwa samotne wierzcholki nie przeszkadzaja
            break
        fixing_bettwen_Graphs(tmp)
    # zadbanie o doeulerowanie grafu
    eulering_Graph()
# checking if graph is connected #
def if_connected_Graph(nextVertex):
    global sequence, var, lenOfDNA, lenOfSample, numEdges, numVertices
    global graph, structInGraph, oligo, oligoUpSideDown, structInOligo
    global visitedVertex
    #print("hi", nextVertex)
    visitedVertex.append(nextVertex)
    for it in range(numVertices):
        if ((graph[oligo[nextVertex].position][it].outside >= 1 or graph[oligo[nextVertex].position][it].inside >= 1) and oligoUpSideDown[it] not in visitedVertex):
            if_connected_Graph(oligoUpSideDown[it])
# adding connection if graph is unconnected
def fixing_bettwen_Graphs(tmp):
    global sequence, var, lenOfDNA, lenOfSample, numEdges, numVertices
    global graph, structInGraph, oligo, oligoUpSideDown, structInOligo
    global visitedVertex

    visitedVertex_minus = []
    visitedVertex_plus = []
    visitedVertex_zero = []
    for it in visitedVertex:
        if oligo[it].outside - oligo[it].inside > 0:
            visitedVertex_plus.append({"it":it, "num":oligo[it].outside - oligo[it].inside})
        elif oligo[it].outside - oligo[it].inside < 0:
            visitedVertex_minus.append({"it": it, "num":oligo[it].outside - oligo[it].inside})
        else:
            visitedVertex_zero.append({"it": it, "num": 0})
    tmp_minus = []
    tmp_plus = []
    tmp_zero = []
    for it in tmp:
        if oligo[it].outside - oligo[it].inside > 0:
            tmp_plus.append({"it": it, "num":oligo[it].outside - oligo[it].inside})
        elif oligo[it].outside - oligo[it].inside < 0:
            tmp_minus.append({"it": it, "num": oligo[it].outside - oligo[it].inside})
        else:
            tmp_zero.append({"it": it, "num": 0})

    visitedVertex_plus.sort(reverse=True, key=lambda x: x.get('num'))
    tmp_plus.sort(reverse=True, key=lambda x: x.get('num'))
    visitedVertex_minus.sort(key=lambda x: x.get('num'))
    tmp_minus.sort(key=lambda x: x.get('num'))
    higest = max(max(abs(visitedVertex_minus[0]["num"]), abs(tmp_minus[0]["num"])), max(visitedVertex_plus[0]["num"], tmp_plus[0]["num"]))
    print("fixing_bettwen_Graphs: visitedVertex_plus-", visitedVertex_plus, " visitedVertex_minus- ", visitedVertex_minus)
    print("fixing_bettwen_Graphs: tmp_plus- ", tmp_plus, " tmp_minus-  ", tmp_minus)
    print("fixing_bettwen_Graphs: higest- ", higest)

    new_connection = []
    offset = 2
    exit = 0
    #while(offset != 6 and exit == 0):
    while (exit == 0):

        print("fixing_bettwen_Graphs: offset- ", offset)
        it_visitedVertex_plus = 0
        it_visitedVertex_minus = 0
        it_tmp_plus = 0
        it_tmp_minus = 0

        print("fixing_bettwen_Graphs: NR 1 poszukujemy pomiedzy tmp_minus i visitedVertex_plus")
        while (it_visitedVertex_plus != len(visitedVertex_plus) and it_tmp_minus != len(tmp_minus) and exit == 0):
            if (abs(visitedVertex_plus[it_visitedVertex_plus]["num"]) > abs(
                    tmp_minus[it_tmp_minus]["num"])):
                for it in range(it_tmp_minus, len(tmp_minus)):
                    #print("jeden ", visitedVertex_plus[it_visitedVertex_plus]["num"], "i dwa", tmp_minus[it]["num"])
                    if visitedVertex_plus[it_visitedVertex_plus]["it"][:-offset] == tmp_minus[it]["it"][offset:]:
                        print("fixing_bettwen_Graphs: bingo + ", tmp_minus[it]["it"], visitedVertex_plus[it_visitedVertex_plus]["it"])
                        if_connected_Graph(tmp_minus[it]["it"])
                        if(len(visitedVertex) < 5):
                            continue
                        new_connection.append(tmp_minus[it])
                        new_connection.append(visitedVertex_plus[it_visitedVertex_plus])
                        exit = 1
                        break
                it_visitedVertex_plus += 1
            else:
                for it in range(it_visitedVertex_plus, len(visitedVertex_plus)):
                    #print("dwa", tmp_minus[it_tmp_minus]["num"], "i jeden", visitedVertex_plus[it]["num"])
                    if visitedVertex_plus[it]["it"][:-offset] == tmp_minus[it_tmp_minus]["it"][offset:]:
                        print("fixing_bettwen_Graphs: bingo - ! ", tmp_minus[it_tmp_minus]["it"], visitedVertex_plus[it]["it"])
                        if_connected_Graph(tmp_minus[it_tmp_minus]["it"])
                        if (len(visitedVertex) < 5):
                            continue
                        new_connection.append(tmp_minus[it_tmp_minus])
                        new_connection.append(visitedVertex_plus[it])
                        exit = 1
                        break
                it_tmp_minus += 1

        print("fixing_bettwen_Graphs: NR 2 poszukujemy pomiedzy visitedVertex_minus i tmp_plus")
        while (it_visitedVertex_minus != len(visitedVertex_minus) and it_tmp_plus != len(tmp_plus) and exit <= 1):
            if (abs(visitedVertex_minus[it_visitedVertex_minus]["num"]) > abs(tmp_plus[it_tmp_plus]["num"])):
                for it in range(it_tmp_plus, len(tmp_plus)):
                    #print("dwa ", visitedVertex_minus[it_visitedVertex_minus]["num"], "i jeden", tmp_plus[it]["num"])
                    if visitedVertex_minus[it_visitedVertex_minus]["it"][offset:] == tmp_plus[it]["it"][:-offset]:
                        print("fixing_bettwen_Graphs: - ! ", visitedVertex_minus[it_visitedVertex_minus]["it"], tmp_plus[it]["it"])
                        if_connected_Graph(tmp_plus[it]["it"])
                        if (len(visitedVertex) < 5):
                            continue
                        if (exit == 0):
                            print("fixing_bettwen_Graphs: dodajemy z NR 2")
                            new_connection.append(visitedVertex_minus[it_visitedVertex_minus])
                            new_connection.append(tmp_plus[it])
                        elif (max(new_connection[0]["num"], new_connection[1]["num"]) < max(
                                visitedVertex_minus[it_visitedVertex_minus]["num"], tmp_plus[it]["num"])):
                            print("fixing_bettwen_Graphs: dodajemy z NR 2")
                            new_connection = []
                            new_connection.append(visitedVertex_minus[it_visitedVertex_minus])
                            new_connection.append(tmp_plus[it])
                        else:
                            print("fixing_bettwen_Graphs: dodajemy z NR 1")
                        exit = 2
                        break
                it_visitedVertex_minus += 1
            else:
                for it in range(it_visitedVertex_minus, len(visitedVertex_minus)):
                    #print("jeden", tmp_plus[it_tmp_plus]["num"], "i dwa", visitedVertex_minus[it]["num"])
                    if visitedVertex_minus[it]["it"][offset:] == tmp_plus[it_tmp_plus]["it"][:-offset]:
                        print("fixing_bettwen_Graphs: bingo + ! ", visitedVertex_minus[it]["it"], tmp_plus[it_tmp_plus]["it"])
                        if_connected_Graph(tmp_plus[it_tmp_plus]["it"])
                        if (len(visitedVertex) < 5):
                            continue
                        if (exit == 0):
                            print("fixing_bettwen_Graphs: dodajemy z NR 2")
                            new_connection.append(visitedVertex_minus[it])
                            new_connection.append(tmp_plus[it_tmp_plus])
                        elif (max(new_connection[0]["num"], new_connection[1]["num"]) < max(
                                visitedVertex_minus[it]["num"], tmp_plus[it_tmp_plus]["num"])):
                            print("fixing_bettwen_Graphs: dodajemy z NR 2")
                            new_connection = []
                            new_connection.append(visitedVertex_minus[it])
                            new_connection.append(tmp_plus[it_tmp_plus])
                        else:
                            print("fixing_bettwen_Graphs: dodajemy z NR 1")
                        exit = 2
                        break
                it_tmp_plus += 1


        offset -= 1 # teraz mniejszy dla 1 0
        if(exit == 0): # zaczynamy poszukiwania miedzy: najwiekszym a 0

            print("fixing_bettwen_Graphs: NR 3 poszukujemy pomiedzy 0 i wierzcholkiem roznym od 0")
            for minus in visitedVertex_minus:
                if (abs(minus["num"]) == higest):
                    for zero in tmp_zero:
                        if(zero["it"][:-offset] == minus["it"][offset:]):
                            print("fixing_bettwen_Graphs: bingo - 0 ! ", minus["it"], zero["it"])
                            if_connected_Graph(zero["it"])
                            if (len(visitedVertex) < 5):
                                continue
                            new_connection.append(minus)
                            new_connection.append(zero)
                            exit = 1
                            break
                            # przeszukujemy zero z wszystkimi w poszukiwaniu outa
                else:
                    break
                if(exit != 0):
                    break
            if (exit != 0):
                print("fixing_bettwen_Graphs: dodajemy z NR 3")
                break

            for plus in visitedVertex_plus:
                if (plus["num"] == higest):
                    for zero in tmp_zero:
                        if (plus["it"][:-offset] == zero["it"][offset:]):
                            print("fixing_bettwen_Graphs: bingo 0 + ! ", zero["it"], plus["it"])
                            if_connected_Graph(zero["it"])
                            if (len(visitedVertex) < 5):
                                continue
                            new_connection.append(zero)
                            new_connection.append(plus)
                            exit = 1
                            break
                else:
                    break
                if (exit != 0):
                    break
            if (exit != 0):
                print("fixing_bettwen_Graphs: dodajemy z NR 3")
                break

            for minus in tmp_minus:
                if (abs(minus["num"]) == higest):
                    for zero in visitedVertex_zero:
                        if (zero["it"][:-offset] == minus["it"][offset:]):
                            print("fixing_bettwen_Graphs: bingo - 0 ! ", minus["it"], zero["it"])
                            if_connected_Graph(minus["it"])
                            if (len(visitedVertex) < 5):
                                continue
                            new_connection.append(minus)
                            new_connection.append(zero)
                            exit = 1
                            break
                else:
                    break
                if (exit != 0):
                    break
            if (exit != 0):
                print("fixing_bettwen_Graphs: dodajemy z NR 3")
                break

            for plus in tmp_plus:
                if (plus["num"] == higest):
                    for zero in visitedVertex_zero:
                        if (plus["it"][:-offset] == zero["it"][offset:]):
                            print("fixing_bettwen_Graphs: bingo 0 + ! ", zero["it"], plus["it"])
                            if_connected_Graph(plus["it"])
                            if (len(visitedVertex) < 5):
                                continue
                            new_connection.append(zero)
                            new_connection.append(plus)
                            exit = 1
                            break
                else:
                    break
                if (exit != 0):
                    break
            if (exit != 0):
                print("fixing_bettwen_Graphs: dodajemy z NR 3")
                break

            offset += 2

    print("fixing_bettwen_Graphs New Connection :D ", new_connection,  "\n")
    if(exit == 0):
        print("ojojoj no nie ma NIC nie MA :< --- to trzeba bd zmienic")
    graph[oligo[new_connection[0]["it"]].position][oligo[new_connection[1]["it"]].position].outside += 1
    oligo[new_connection[0]["it"]].outside += 1
    graph[oligo[new_connection[1]["it"]].position][oligo[new_connection[0]["it"]].position].inside += 1
    oligo[new_connection[1]["it"]].inside += 1
# doeulerowywanie grafu
def eulering_Graph():
    global sequence, var, lenOfDNA, lenOfSample, numEdges, numVertices
    global graph, structInGraph, oligo, oligoUpSideDown, structInOligo
    global visitedVertex, startingPoint

    vertexNot_0 = 0
    for it in oligo:
        vertexNot_0 += abs(oligo[it].inside - oligo[it].outside)

    visitedVertex_minus = []
    visitedVertex_plus = []
    visitedVertex_zero = []
    for it in visitedVertex:
        if oligo[it].outside - oligo[it].inside > 0:
             visitedVertex_plus.append({"it": it, "num": oligo[it].outside - oligo[it].inside})
        elif oligo[it].outside - oligo[it].inside < 0:
            visitedVertex_minus.append({"it": it, "num": oligo[it].outside - oligo[it].inside})
        else:
            visitedVertex_zero.append({"it": it, "num": 0})

    visitedVertex_plus.sort(reverse=True, key=lambda x: x.get('num'))
    visitedVertex_minus.sort(key=lambda x: x.get('num'))

    if(vertexNot_0 == 2):
        print("\neulering_Graph: graf doeulerowany")
        print("eulering_Graph: expected edges and existings ", lenOfDNA - lenOfSample + 1, numEdges,
              "- not add ones added in function fixing_beetwen_Graph !!")
        startingPoint = visitedVertex_plus[0]["it"]
    elif(vertexNot_0 == 0):
        print("\neulering_Graph: graf jako jeden wielki cykl")
        print("eulering_Graph: expected edges and existings ", lenOfDNA - lenOfSample + 1, numEdges, "- not add ones added in function fixing_beetwen_Graph !!")
        startingPoint = oligoUpSideDown[0]
    else:
        print("\neulering_Graph: trzeba eulerowac")
        print("eulering_Graph: expected edges and existings ", lenOfDNA - lenOfSample + 1, numEdges,
              "- not add ones added in function fixing_beetwen_Graph !!")
        print("eulering_Graph: visitedVertex_plus- ", visitedVertex_plus)
        print("eulering_Graph: visitedVertex_minus- ", visitedVertex_minus)
        new_connection = []
        offset = 2

        # wyrzucenie hopelessow ######################################################################################
        while(vertexNot_0 != 2):
            print("eulering_Graph: vertexNot_0-  ", vertexNot_0)
            print("eulering_Graph: offset-  ", offset)
            higest = max(abs(visitedVertex_minus[0]["num"]), abs(visitedVertex_plus[0]["num"]))
            exit = 0

            # kicking out edge
            it_visitedVertex_plus = 0
            it_visitedVertex_minus = 0
            while (exit == 0 and it_visitedVertex_plus != len(visitedVertex_plus) and it_visitedVertex_minus != len(visitedVertex_minus) and offset == 2):
                if (abs(visitedVertex_minus[it_visitedVertex_minus]["num"]) >= abs(visitedVertex_plus[it_visitedVertex_plus]["num"]) and abs(visitedVertex_minus[it_visitedVertex_minus]["num"]) == higest):
                    for it in range(it_visitedVertex_plus, len(visitedVertex_plus)):
                        #print("dwa ", visitedVertex_minus[it_visitedVertex_minus]["num"], "i jeden", visitedVertex_plus[it]["num"], visitedVertex_minus[it_visitedVertex_minus]["it"], visitedVertex_plus[it]["it"])
                        if graph[oligo[visitedVertex_plus[it]["it"]].position][oligo[visitedVertex_minus[it_visitedVertex_minus]["it"]].position].outside == 1:
                            print("eulering_Graph: kick out - ! ", visitedVertex_minus[it_visitedVertex_minus]["it"], visitedVertex_plus[it]["it"], "na odwrot")
                            new_connection.append(visitedVertex_plus[it])
                            new_connection.append(visitedVertex_minus[it_visitedVertex_minus])

                            graph[oligo[new_connection[0]["it"]].position][
                                oligo[new_connection[1]["it"]].position].outside -= 1
                            oligo[new_connection[0]["it"]].outside -= 1
                            graph[oligo[new_connection[1]["it"]].position][
                                oligo[new_connection[0]["it"]].position].inside -= 1
                            oligo[new_connection[1]["it"]].inside -= 1
                            # jak nizej i jest git :D

                            new_connection[0]["num"] -= 1
                            new_connection[1]["num"] += 1
                            visitedVertex_plus = [x for x in visitedVertex_plus if
                                                  x.get("it") != new_connection[0]["it"]]
                            visitedVertex_minus = [x for x in visitedVertex_minus if
                                                   x.get("it") != new_connection[1]["it"]]
                            if(new_connection[0]["num"] == 0):
                                visitedVertex_zero.append(new_connection[0])
                            else:
                                visitedVertex_plus.append(new_connection[0])
                            if(new_connection[1]["num"] == 0):
                                visitedVertex_zero.append(new_connection[1])
                            else:
                                visitedVertex_minus.append(new_connection[1])

                            '''
                            if (new_connection[0]["num"] == 1):
                                visitedVertex_plus = [x for x in visitedVertex_plus if
                                                      x.get("it") != new_connection[0]["it"]]
                                visitedVertex_zero.append(new_connection[0]["num"])
                            if (new_connection[1]["num"] == 1):
                                visitedVertex_minus = [x for x in visitedVertex_minus if
                                                       x.get("it") != new_connection[1]["it"]]
                                visitedVertex_zero.append(new_connection[1]["num"])
                            print(visitedVertex_plus)
                            '''

                            # checking
                            # decysion
                            new_connection = []
                            offset = 2
                            vertexNot_0 -= 2
                            exit = 1
                            break
                    it_visitedVertex_minus += 1
                elif(abs(visitedVertex_plus[it_visitedVertex_plus]["num"]) > abs(visitedVertex_minus[it_visitedVertex_minus]["num"]) and abs(visitedVertex_plus[it_visitedVertex_plus]["num"]) == higest):
                    for it in range(it_visitedVertex_minus, len(visitedVertex_minus)):
                        # print("jeden", tmp_plus[it_tmp_plus]["num"], "i dwa", visitedVertex_minus[it]["num"])
                        if graph[oligo[visitedVertex_plus[it_visitedVertex_plus]["it"]].position][oligo[visitedVertex_minus[it]["it"]].position].outside == 1:
                            print("eulering_Graph: kick out + ! ", visitedVertex_minus[it]["it"], visitedVertex_plus[it_visitedVertex_plus]["it"], "na odwrot")

                            new_connection.append(visitedVertex_plus[it_visitedVertex_plus])
                            new_connection.append(visitedVertex_minus[it])

                            graph[oligo[new_connection[0]["it"]].position][
                                oligo[new_connection[1]["it"]].position].outside -= 1
                            oligo[new_connection[0]["it"]].outside -= 1
                            graph[oligo[new_connection[1]["it"]].position][
                                oligo[new_connection[0]["it"]].position].inside -= 1
                            oligo[new_connection[1]["it"]].inside -= 1

                            new_connection[0]["num"] -= 1
                            new_connection[1]["num"] += 1
                            visitedVertex_plus = [x for x in visitedVertex_plus if
                                                  x.get("it") != new_connection[0]["it"]]
                            visitedVertex_minus = [x for x in visitedVertex_minus if
                                                   x.get("it") != new_connection[1]["it"]]
                            if (new_connection[0]["num"] == 0):
                                visitedVertex_zero.append(new_connection[0])
                            else:
                                visitedVertex_plus.append(new_connection[0])
                            if (new_connection[1]["num"] == 0):
                                visitedVertex_zero.append(new_connection[1])
                            else:
                                visitedVertex_minus.append(new_connection[1])
                            '''
                            if (new_connection[0]["num"] == 1):
                                visitedVertex_plus = [x for x in visitedVertex_plus if
                                                      x.get("it") != new_connection[0]["it"]]
                                visitedVertex_zero.append(new_connection[0]["num"])
                            if (new_connection[1]["num"] == 1):
                                visitedVertex_minus = [x for x in visitedVertex_minus if
                                                       x.get("it") != new_connection[1]["it"]]
                                visitedVertex_zero.append(new_connection[1]["num"])
                            '''
                            # checking
                            # decysion
                            new_connection = []
                            offset = 2
                            vertexNot_0 -= 2
                            exit = 1
                            break
                    it_visitedVertex_plus += 1
                else:
                    break
            if (exit != 0):
                continue

            # addning the edge beetwen
            it_visitedVertex_plus = 0
            it_visitedVertex_minus = 0
            while (exit == 0 and it_visitedVertex_plus != len(visitedVertex_plus) and it_visitedVertex_minus != len(visitedVertex_minus)):
                if (abs(visitedVertex_minus[it_visitedVertex_minus]["num"]) >= abs(visitedVertex_plus[it_visitedVertex_plus]["num"]) and abs(visitedVertex_minus[it_visitedVertex_minus]["num"]) == higest):
                    for it in range(it_visitedVertex_plus, len(visitedVertex_plus)):
                        # print("dwa ", visitedVertex_minus[it_visitedVertex_minus]["num"], "i jeden", tmp_plus[it]["num"])
                        if visitedVertex_minus[it_visitedVertex_minus]["it"][offset:] == visitedVertex_plus[it]["it"][:-offset]:
                            print("eulering_Graph: bingo dla - ! ", visitedVertex_minus[it_visitedVertex_minus]["it"], visitedVertex_plus[it]["it"])
                            new_connection.append(visitedVertex_minus[it_visitedVertex_minus])
                            new_connection.append(visitedVertex_plus[it])

                            graph[oligo[new_connection[0]["it"]].position][oligo[new_connection[1]["it"]].position].outside += 1
                            oligo[new_connection[0]["it"]].outside += 1
                            graph[oligo[new_connection[1]["it"]].position][oligo[new_connection[0]["it"]].position].inside += 1
                            oligo[new_connection[1]["it"]].inside += 1

                            new_connection[0]["num"] += 1
                            new_connection[1]["num"] -= 1
                            visitedVertex_plus = [x for x in visitedVertex_plus if
                                                  x.get("it") != new_connection[1]["it"]]
                            visitedVertex_minus = [x for x in visitedVertex_minus if
                                                   x.get("it") != new_connection[0]["it"]]
                            if (new_connection[1]["num"] == 0):
                                visitedVertex_zero.append(new_connection[1])
                            else:
                                visitedVertex_plus.append(new_connection[1])
                            if (new_connection[0]["num"] == 0):
                                visitedVertex_zero.append(new_connection[0])
                            else:
                                visitedVertex_minus.append(new_connection[0])
                            '''
                            if(new_connection[0]["num"] == 1):
                                visitedVertex_zero.append(new_connection[0]["num"])
                                visitedVertex_minus = [x for x in visitedVertex_minus if
                                                       x.get("it") != new_connection[0]["it"]]
                            if(new_connection[1]["num"] == 1):
                                visitedVertex_zero.append(new_connection[1]["num"])
                                visitedVertex_plus = [x for x in visitedVertex_plus if
                                                      x.get("it") != new_connection[1]["it"]]
                            '''

                            new_connection = []
                            offset = 2
                            vertexNot_0 -= 2
                            exit = 1

                            break
                    it_visitedVertex_minus += 1
                elif(abs(visitedVertex_plus[it_visitedVertex_plus]["num"]) > abs(visitedVertex_minus[it_visitedVertex_minus]["num"]) and abs(visitedVertex_plus[it_visitedVertex_plus]["num"]) == higest):
                    for it in range(it_visitedVertex_minus, len(visitedVertex_minus)):
                        # print("jeden", tmp_plus[it_tmp_plus]["num"], "i dwa", visitedVertex_minus[it]["num"])
                        if visitedVertex_minus[it]["it"][offset:] == visitedVertex_plus[it_visitedVertex_plus]["it"][:-offset]:
                            print("eulering_Graph: bingo dla + ! ", visitedVertex_minus[it]["it"], visitedVertex_plus[it_visitedVertex_plus]["it"])
                            new_connection.append(visitedVertex_minus[it])
                            new_connection.append(visitedVertex_plus[it_visitedVertex_plus])

                            graph[oligo[new_connection[0]["it"]].position][oligo[new_connection[1]["it"]].position].outside += 1
                            oligo[new_connection[0]["it"]].outside += 1
                            graph[oligo[new_connection[1]["it"]].position][oligo[new_connection[0]["it"]].position].inside += 1
                            oligo[new_connection[1]["it"]].inside += 1

                            new_connection[0]["num"] += 1
                            new_connection[1]["num"] -= 1
                            visitedVertex_plus = [x for x in visitedVertex_plus if
                                                  x.get("it") != new_connection[1]["it"]]
                            visitedVertex_minus = [x for x in visitedVertex_minus if
                                                   x.get("it") != new_connection[0]["it"]]
                            if (new_connection[1]["num"] == 0):
                                visitedVertex_zero.append(new_connection[1])
                            else:
                                visitedVertex_plus.append(new_connection[1])
                            if (new_connection[0]["num"] == 0):
                                visitedVertex_zero.append(new_connection[0])
                            else:
                                visitedVertex_minus.append(new_connection[0])

                            '''
                            if (new_connection[0]["num"] == 1):
                                visitedVertex_zero.append(new_connection[0]["num"])
                                visitedVertex_minus = [x for x in visitedVertex_minus if
                                                       x.get("it") != new_connection[0]["it"]]
                            if (new_connection[1]["num"] == 1):
                                visitedVertex_zero.append(new_connection[1]["num"])
                                visitedVertex_plus = [x for x in visitedVertex_plus if
                                                      x.get("it") != new_connection[1]["it"]]
                            '''

                            new_connection = []
                            offset = 2
                            vertexNot_0 -= 2
                            exit = 1

                            break
                    it_visitedVertex_plus += 1
                else:
                    break
            if(exit != 0):
                continue

            offset += 1


        '''
                #adding beetwen smth and 0
                #offset -= 1  # teraz mniejszy dla 1 0 # tu jest zle
            print("PIERDOLONY OFFSET WYNOSI: ", offset)
            for minus in visitedVertex_minus:
                if (abs(minus["num"]) == higest):
                    for zero in visitedVertex_zero:
                        if (zero["it"][:-(offset-1)] == minus["it"][(offset-1):]):
                            print("mamy polaczenie z 0", minus["it"], zero["it"])
                            new_connection.append(minus)
                            new_connection.append(zero)
                            new_connection = []
                            exit = 1
                            break
                            # przeszukujemy zero z wszystkimi w poszukiwaniu outa
                else:
                    break
                if (exit != 0):
                    break
            if (exit != 0):
                continue

            for plus in visitedVertex_plus:
                if (plus["num"] == higest):
                    for zero in visitedVertex_zero:
                        if (plus["it"][:-(offset-1)] == zero["it"][(offset-1):]):
                            print("mamy polaczenie z 0", zero["it"], plus["it"])
                            new_connection.append(zero)
                            new_connection.append(plus)
                            new_connection = []
                            exit = 1
                            break
                else:
                    break
                if (exit != 0):
                    break
            if (exit != 0):
                continue

            # kicking out beetwen smth 0
            for minus in visitedVertex_minus:
                if (abs(minus["num"]) == higest):
                    for zero in visitedVertex_zero:
                        if (graph[oligo[zero["it"]].position][oligo[minus["it"]].position] == 1):
                            print("wywalamy polaczenie z 0 i - ", zero["it"], minus["it"])
                            new_connection.append(minus)
                            new_connection.append(zero)
                            new_connection = []
                            exit = 1
                            break
                            # przeszukujemy zero z wszystkimi w poszukiwaniu outa
                else:
                    break
                if (exit != 0):
                    break
            if (exit != 0):
                continue

            for plus in visitedVertex_plus:
                if (plus["num"] == higest):
                    for zero in visitedVertex_zero:
                        if (graph[oligo[plus["it"]].position][oligo[zero["it"]].position]):
                            print("wywalay polaczenie z + i 0", plus["it"], zero["it"])
                            new_connection.append(zero)
                            new_connection.append(plus)
                            new_connection = []
                            exit = 1
                            break
                else:
                    break
                if (exit != 0):
                    break
            if (exit != 0):
                continue
            '''

            #print('kutwesddsas')
            #offset +=1



        #print("\ndoeulerowujemy ", vertexNot_0, "mamy krawedzi ", numEdges, " a chcemy w zasadzie", lenOfDNA - lenOfSample + 1)
        print("\ndoeulerowany graf, wartosc bezwzgledna z wagi wierzcholkow = ", vertexNot_0)
        if(visitedVertex_plus == []):
            startingPoint = oligoUpSideDown[0]
        else:
            startingPoint = visitedVertex_plus[0]["it"]

# ------------------------------------------------------------------------------------------------------

### DFS ### znajdowanie sciezki Elera, Algorytm Hierholzera https://www.youtube.com/watch?v=8MpoO2zA2l4
def DFS(nextVertex):
    global oligo,oligoUpSideDown, graph, numVertices, resolved
    while(oligo[nextVertex].outside != 0):
        for it in range(numVertices):
            if(graph[oligo[nextVertex].position][it].outside >= 1): ## mysle ze moze byc tu == 1
                oligo[nextVertex].outside -= 1
                graph[oligo[nextVertex].position][it].outside -= 1
                print("wierzcholek: ", nextVertex, " kolejny: ", oligoUpSideDown[it], "licznik out: ", oligo[nextVertex].outside)
                DFS(oligoUpSideDown[it])
    resolved.append(nextVertex)
#-------------------------------------------------------------------------------------------------------

### MAIN ###
choose = input("1(dane z plików), 2(dane testowe) , 3(dane z generatora)\n")
fileList = []
currentFile = "instances/9.200-80"

# plik z wynikami
savedFile = open("wyniki.txt", "w")

if choose == "1":
    fileList = os.listdir("instances/")

# czemu python nie ma do while?
while True:
    clearVariables()

    #wczytujemy plik z listy plikow instances
    if (choose == "1"):
        currentFile = "instances/" + fileList.pop()
        testDate(currentFile)
    elif choose == "2":
        testDate(currentFile)
    else:
        dateFrom_Generator()

    create_Graph()
    #show_Graph()
    preparing_Graph()
    # --- extra by zobaczyc czy nie rozlaczylismy macierzy
    visitedVertex = []
    if_connected_Graph(oligoUpSideDown[0])
    tmp = []
    for element in oligo:
        if element not in visitedVertex:
            tmp.append(element)
    print(" VisitedVertex- ", visitedVertex)
    print(" tmp- ", tmp, "\n")
    # ----

    print("to jest start: ",startingPoint)
    DFS(startingPoint)
    resolved = resolved[::-1]
    outcome = resolved[0]
    for it in range(len(resolved)-1):
        for it2 in range(1, lenOfSample):
            if (resolved[it][it2:] == resolved[it+1][:-it2]):
                #print(resolved[it], resolved[it+1])
                #print("dodajemy ", resolved[it+1][(lenOfSample-1)-it2:])
                outcome += resolved[it+1][(lenOfSample-1)-it2:]
                break

    #print("dlugosc", lenOfDNA, sequence)
    print("sequance", lenOfDNA)
    #print("co mamy", len(outcome), outcome[:lenOfDNA])
    print(resolved)
    print(var)

    # sprawdzanie ile
    lista = []
    if(len(outcome ) > lenOfDNA):
        outcome = outcome[0:lenOfDNA]

    print("co mamy", outcome, "\ndługość: ", len(outcome))

    for i in range(len(outcome) - 10):
        lista.append(outcome[i:i+10])
    print(lista)

    it = 0
    # nowa lista zeby nie modyfikowac oryginalu
    remainingOligos = list(var)
    for i in lista:
        for j in remainingOligos:
            if(i == j):
                it += 1
                remainingOligos.remove(j)
                break

    accuracy = it / len(var)
    print("skutecznosc: ", (it / len(var)))

    savedFile.write(currentFile + " - " + str(accuracy) + '\n')
    if (choose != "1" or len(fileList) == 0):
        break
        savedFile.close()
#------------------------------------------------------------------------------------------------------


# SMIETNICZEK KODOW
'''
print("\n\nabrakadarba:::")
visitedVertex_minus = []
visitedVertex_plus = []
visitedVertex_plus.append({"it": "AAA", "num": 4})
visitedVertex_plus.append({"it": "AAA", "num": 1})
visitedVertex_plus.append({"it": "ATC", "num": 4})
visitedVertex_plus.append({"it": "AAA", "num": 5})
visitedVertex_plus.append({"it": "AAA", "num": 3})
visitedVertex_plus.append({"it": "AAA", "num": 5})
visitedVertex_plus.append({"it": "AAA", "num": 1})

visitedVertex_minus.append({"it": "CTC", "num": -3})
visitedVertex_minus.append({"it": "BBB", "num": -5})
visitedVertex_minus.append({"it": "BBB", "num": -2})

visitedVertex_plus.sort(reverse=True, key=lambda x: x.get('num'))
visitedVertex_minus.sort(key=lambda x: x.get('num'))
print(visitedVertex_plus, " i jebaniec na minus ", visitedVertex_minus)

it_visitedVertex_plus = 0
it_visitedVertex_minus = 0

visitedVertex_minus = [x for x in visitedVertex_minus if x.get("it") != "CTC"]
print("kurwa", visitedVertex_minus)



while(it_visitedVertex_plus != len(visitedVertex_plus) and it_visitedVertex_minus != len(visitedVertex_minus)):
    print("jeb sie")
    if (abs(visitedVertex_plus[it_visitedVertex_plus]["num"]) > abs(visitedVertex_minus[it_visitedVertex_minus]["num"])):
        for it in range(it_visitedVertex_minus, len(visitedVertex_minus)):
            print("jeden ", visitedVertex_plus[it_visitedVertex_plus]["num"], "i dwa", visitedVertex_minus[it]["num"])
            if visitedVertex_plus[it_visitedVertex_plus]["it"][2:] == visitedVertex_minus[it]["it"][:-2]:
                print("bingo dla + ! ", visitedVertex_plus[it_visitedVertex_plus]["it"], visitedVertex_minus[it]["it"])
                #zapamietujemy i wychodzimy
                break
                
                ### hierarchia nie potrzebna jak sie zdecyduje na krawedziowy pelny
                #vertex_plus = visitedVertex_plus[it_visitedVertex_plus]["it"]
                #vertex_minus = visitedVertex_minus[it]["it"]
                #for num in range(numVertices):
                #    print(oligoUpSideDown[num], vertex_plus)
                #    if (oligoUpSideDown[num] == vertex_plus or oligoUpSideDown[num] == vertex_minus):
                #        print(num, "a to vertexy@@@@: ", vertex_plus, vertex_minus )
                #        continue

                    #if (graph[oligo[nextVertex].position][num].outside >= 1)
                #for
                #nowa tablica slownikowe pamietanie z do i numerek 1 ucieczka 2 oba maja ucieczke 0 zaden <- taki chcemy wybrac

        it_visitedVertex_plus += 1
    else:
        for it in range(it_visitedVertex_plus, len(visitedVertex_plus)):
            print("dwa", visitedVertex_minus[it_visitedVertex_minus]["num"], "i jeden", visitedVertex_plus[it]["num"])
            if visitedVertex_plus[it]["it"][2:] == visitedVertex_minus[it_visitedVertex_minus]["it"][:-2]:
                print("bingo dla - ! ", visitedVertex_plus[it]["it"], visitedVertex_minus[it_visitedVertex_minus]["it"])
        it_visitedVertex_minus +=1
    print("itjeden ", it_visitedVertex_plus, "itdewa ", it_visitedVertex_minus)
'''

'''
# to samo bez slownikowego zamieszania
jeden = [5,5,4,4,3,1,1]
dwa = [-5,-3,-2]
it_jeden = 0
it_dwa = 0
if(len(jeden) == 0 or len(dwa) == 0): # juz nie potrzebne
    print("GOWNo treba isc dalej")
    # tutaj jakas wartosc na x zeby nie porownywac


while(it_jeden != len(jeden) and it_dwa != len(dwa)):
    print("jeb sie")
    if(abs(jeden[it_jeden]) > abs(dwa[it_dwa])):
        for it in range(it_dwa, len(dwa)):
            print("jeden ", jeden[it_jeden], "i dwa", dwa[it])
        it_jeden += 1
    else:
        for it in range(it_jeden, len(jeden)):
            print("dwa", dwa[it_dwa], "i jeden", jeden[it])
        it_dwa +=1
    print("itjeden ", it_jeden, "itdewa ", it_dwa)
'''''