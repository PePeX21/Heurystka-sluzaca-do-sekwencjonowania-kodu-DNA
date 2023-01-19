# Heurystka-sluzaca-do-sekwencjonowania-kodu-DNA
## Wstęp teoretyczny
Do podstawy sekwencjonowania wykorzystujemy algorytm Pevznera, który polega na
przekształceniu ścieżki Hamiltona złożonej z oligonukleotydów do ścieżki Eulera w celu pracy
algorytmu w czasie wielomianowym. Algorytm dzieli oligonukleotydy znajdujące się w danych na
wejściu na dwa (jeden bez pierwszego nukleotydu , drugi bez ostatniego) - wierzchołki w grafie,
tak, aby łuki skierowane przechodzące pomiędzy dwoma wierzchołkami reprezentowały jeden
oligonukleotyd potrzebny do sekwencjonowania.

Np. oligonukleotyd CGAT przerobiony na łuk : CGA -> GAT
Aby wykryć sekwencję DNA wystarczy wtedy znaleźć ścieżkę przechodzącą przez wszystkie
łuki, zaczynając od wierzchołka o większej liczbie wychodzących łuków a kończąc na
wierzchołku o większej liczbie łuków wchodzących. W przypadku gdy nie jest to możliwe, mamy
do czynienia z błędami pozytywnymi lub negatywnymi.

Problem oryginalnej metody pojawia się przy pojawieniu się błędów pozytywnych i
negatywnych. Oryginalna heurystyka zaproponowana przez P.A. Pevznera pozwala w pewnym
stopniu na wykrycie brakujących oligonukleotydów w przypadku błędów negatywnych.
Wykrywamy wtedy wierzchołki, w których liczba wchodzących i wychodzących łuków nie jest
sobie równa. Z tych wierzchołków, tworzymy graf przepływu tak aby dodać brakujące
oligonukleotydy - tworzymy nowe łuki. Wierzchołki z większą liczbą łuków wchodzących zostają
w ten sposób pierwszą warstwą grafu przepływu, a wierzchołki z większą liczbą łuków
wychodzących zostają drugą warstwą przepływu. Koszt utworzenia oligonukleotydu
przedstawiony jest w łuku pomiędzy tymi dwoma warstwami jako offset, który definiuje w którym
miejscu dwa wierzchołki na siebie nachodzą.

Np. dla łańcucha CGATGC dla dwóch wierzchołków CGA - > GAT koszt łuku wynosi 1, gdyż aby
utworzyć oligonukleotyd wystarczy przesunąć nukleotyd w CGA o jeden, aby GA mogło na
siebie nachodzić.
Dla łańcucha CGA - > ATG koszt wynosi 2,
Natomiast dla łańcucha CGA - > TGC koszt wynosi 3.
Heurystyka w ten sposób poszukuje przepływów o minimalnych kosztach, tak aby umożliwić
wykrycie ścieżki przechodzącej po każdym łuku.

Problemy do rozwiązania przy obecnej heurystyce:
- Gdy uzupełniony graf okaże się nie być spójny - np. Wystąpią dwie ścieżki Eulera w
podzielonym grafie, ale brakuje połączenia pomiędzy nimi.
- Pojawienie się cyklu w grafie już na samym początku - brak wierzchołków, które
rozpoczynałyby i zakończyłyby ścieżkę Eulera w grafie.
- Graf nie jest w stanie dodać wystarczającej ilości krawędzi - przepływ o minimalnym
koszcie będzie miał inny koszt niż liczba brakujących oligonukleotydów

## Modyfikacja i opis metody:
Tworzymy macierz sąsiedztwa w której której pola zawierają informacje czy to do danego
wierzchołka wchodzi czy wychodzi krawędź. Dla przykładowego grafu pokazanego na zdjęciu:
![image](https://user-images.githubusercontent.com/67105405/213503203-3233e275-fd76-44f2-b8a0-9a68d240addf.png)

Dane w macierzy prezentują się następująco:
![image](https://user-images.githubusercontent.com/67105405/213503568-59287948-becb-4c79-b43a-def70da66c97.png)

Nawigacja po macierzy odbywa się za pomocą słownika. Odpowiada on również za
zapamiętywanie ilości wierzchołków wchodzących i wychodzących z każdego wierzchołka
![image](https://user-images.githubusercontent.com/67105405/213503712-3d99f40a-e5e6-4d16-9456-e8b2b67e01c5.png)

Następnie wyznaczamy stopień wierzchołków
( Stopień większy od 0 - więcej wierzchołków wychodzących od wchodzących,
Stopień mniejszy od 0 - więcej wierzchołków wchodzących od wychodzących )
Następnie tworzone są trzy tablice: dla wierzchołków o pozytywnych, negatywnych i zerowych
stopniach.

Jeżeli tablice pozytywne i negatywne są jednoelementowe a ilość istniejących krawędzi
odpowiada ilości potrzebnych oligonukleotydów do utworzenia sekwencji o zadanej długości n
poszukiwana jest ścieżka eulera z użyciem algorytmu Hierholzera. Niestety taka korzystna
sytuacja prawie nigdy się nie zdarza przy występowaniu błędów.

W celu pozbycia się błędów sprawdzamy czy graf wierzchołków jest rozłączny. Podobnie
wyznaczamy stopnie wierzchołków tworząc trzy tablice dla ścieżek które nie znajdują się w
głównej szukanej ścieżce. W przypadku grafu rozłącznego do grafu próbujemy dodać nowe
wierzchołki zaczynając od wierzchołków o największych różnicach stopni, a kończąc na
najmniejszych różnicach stopni o przeciwnych znakach, tak aby zmniejszyć ich różnicę.
Przykładowo zaczynając od wierzchołków o stopniach 5 i -5, a kończąc na 1 i -1 .
Przy wykonywaniu, algorytm ogranicza się do pewnej maksymalnej wartości przesunięcia
pomiędzy nimi, zwiększając stopniowo offset w pętli. Gdy nie ma już możliwości dodania
nowych krawędzi na dany obecnie offset, algorytm próbuje usunąć krawędzie pomiędzy
stopniem 1 a 0, lub -1 a 0.

Następny etap wygląda podobnie, z tą różnicą, że tym razem następuje najpierw próba
usunięcia krawędzi pomiędzy wierzchołkami o największych różnicach stopni, a później
dodawanie krawędzi pomiędzy stopniami 1 a 0, lub -1 a 0.

Opisane operacje umożliwiają utworzenie ścieżki eulera o odpowiedniej wymaganej długości.

## Możliwe ulepszenia
dy znajdziemy sekwencję potencjalnie powtarzających się oligonukleotydów w
oryginalnej sekwencji np. wykryjemy AGCGCT, to możemy uzupełnić parzystą liczbę
nukleotydów np. Dodając drugi raz CGC i GCG - uzyskując AGCGCGCT, podobnie, gdy
sekwencja jest zbyt długa możemy usunąć powtarzające się oligonukleotydy.

Przy usuwaniu i dodawaniu wybieramy te wierzchołki, które mają najmniej potencjalnych
połączeń z innymi, natomiast przy dodawaniu pomiędzy 1 a 0 i -1 a 0 wybieramy te,
które mają ich najwięcej.

W sytuacji gdy znaleziona sekwencja jest za krótka można ją rozciągnąć o krawędzie
usunięte przy operacji między 1 i 0, jeśli takie zostały usunięte z pierwszego i ostatniego
wierzchołka ciągu eulera.

## Stopień wykorzystania oryginalnych oligonukleotydów z poszczególnych instancji testowych przez algorytm

![image](https://user-images.githubusercontent.com/67105405/213505492-d6f69fee-792a-41df-bbd3-147cf2fbe6b6.png)
![image](https://user-images.githubusercontent.com/67105405/213505550-28281e3a-d7c5-4e6f-bfa7-eef4bd0677b1.png)

