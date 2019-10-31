# Găsirea minimului a 4 funcții de optimizare folosind algoritmi tip traiectorie

-- Andrei Căutișanu, 2E2
-- Tema T1

---

### Despre experiment
În probleme cu un grad mare de dificultate, îndeplinirea unui obiectiv poate să nu fie de ajuns. Sistemul trebuie, spre exemplu, să ajungă la soluția optimă într-un anumit timp sau să ajungă cât mai aproape de soluția optimă într-un timp definit. În calcularea minimului global al unei funcții, intervin factori care fac problema să fie irezolvabilă într-un mod determinist în timp rezonabil, precum un număr mare de dimensiuni, un domeniu de definiție foarte mare, sau determinarea valorii funcției într-un anumit punct necesitând calcule foarte complexe. De aceea, este necesară folosirea unor metode de optimizare probabiliste, care vor încerca să aproximeze cât mai precis minimul global al funcțiilor.

Prin acest experiment vom testa performanța tehnicilor de optimizare Best Improvement Hill Climbing, First Improvement Hill Climbing și Simulated Annealing căutând minimul funcțiilor de optimizare Rastrigin, Ackley, Dixon-Price și Rosenbrock, observând timpul de execuție și acuratețea soluțiilor găsite în funcție de numărul de parametri folosiți pentru fiecare dintre funcții.

---

## Algoritmii utilizați

#### HILL CLIMBING

Tehnica de optimizare **hill climbing** realizează o căutare locală, începând cu o soluție aleatorie, apoi făcând o schimbare incrementală soluției pentru a o îmbunătăți. Algoritmul continuă să realizeze schimbări incrementale până când nu mai poate îmbunătăți soluția.

În cazul nostru, algoritmul generează un set de parametri aleatoriu ca prima soluție, apoi caută în vecinătatea acesteia (descrisă în secțiunea "Implementare") o soluție mai bună. Dacă aceasta este găsită, va fi considerată noua soluție, acest procedeu continuând până când nu se poate găsi o soluție mai bună în vecinătatea celei curente. 

- **First Improvement Hill Climbing** va evalua soluțiile din vecinătate până când o găsește pe prima care îmbunătățește rezultatul, selectând-o și oprind evaluarea vecinătății
- **Best Improvement (Steepest Ascent) Hill Climbing** va evalua toate soluțiile din vecinătate și o va selecta pe cea care se apropie cel mai mult de rezultatul dorit (în cazul nostru, setul de parametri care rezultă în cea mai mică valoare a funcției)

În cazul particular al acestui experiment, când în vecinătatea soluției curente nu se găsește una mai bună, algoritmul a ajuns într-un minim local din care nu mai poate ieși. De aceea, vom folosi varianta iterată a Hill Climbing, cu care vom restarta procedeul de fiecare dată când ajungem într-un minim local, astfel găsind mai multe minime locale și parcurgând un spațiu mai mare în funcție.

### SIMULATED ANNEALING
Simulated Annealing este o metodă de aproximare a optimului global care permite ieșirea din optimul local prin acceptarea unor soluții de calitate mai slabă. Probabilitatea acceptării unei soluții de calitate mai slabă este mai mare la începutul executării și scade pe măsură ce programul selectează mai multe soluții.

La începutul programului se inițializează coeficientul de "temperatură" care va scădea pe parcursul rulării (în cazul experimentului de față, am folosit temperatura inițială 100 care scade cu o rată de 5%). În fiecare pas, algoritmul va selecta aleatoriu un vecin al soluției curente. Dacă calitatea acesteia este mai bună (în cazul nostru, valoarea funcției în vecin este mai mică), funcția o va accepta ca o nouă soluție. În caz contrar, algoritmul va accepta noua soluție cu o probabilitate P sau va rămâne în soluția curentă cu o probabilitate 1-P, unde P este definit ca:

P = exp(--(calitatea soluției vecine -- calitatea soluției curente) / Temperatura)

Astfel, probabilitatea selectării unei soluții mai slabe este direct proporțională cu calitatea relativă față de soluția curentă și cu temperatura curentă a algoritmului. Pe măsură ce sunt selectate mai multe soluții, va scădea probabilitatea de a trece într-o soluție mai slabă. În timp ce Hill Climbing va rămâne mereu blocat într-un punct de optim local, Simulated Annealing va avea o șansă de a ieși din acel punct pentru a căuta mai multe soluții și având șanse mai mari de a găsi optimul global.

---

## Implementare

Vom genera soluțiile ca șiruri de biți pe care le vom mapa în intervalul corespunzător domeniului funcției. Pentru a genera un număr într-un interval [a,b] cu precizie de Z zecimale vom avea nevoie de un număr de biți egal cu partea întreagă superioară a numărului log2(10^Z^ * (b-a)). Algoritmul nostru lucrează cu generare cu o precizie de 4 zecimale, deci pentru domeniul de definiție al funcției Ackley  [-32.768, 32.768] va genera un șir de lungime L = 20 de biți pentru a reprezenta un parametru.

Deci, pentru a genera un anumit număr *d* de parametri, trebuie doar să generăm un șir de biți aleatorii de lungime *L* \* *d*.

**Vecinătatea** soluției curente va fi alcătuită din toate șirurile de biți care au distanța Hamming față de aceasta egală cu 1. Spre exemplu, vecinătatea soluției [101101] va fi mulțimea {[001101], [111101], [100101], [101001], [101111], [101100]}

În acest experiment vom itera ambele variante de Hill Climbing de 100 de ori pe fiecare funcție pentru 2 și 5 parametri, respectiv de 25 de ori pentru 30 de parametri și vom extrage soluția cea mai apropiată de rezultatul optim. Acest procedeu se va repeta de 30 de ori pentru a analiza performanța medie și deviația rezultatelor. Simulated Annealing va fi rulat pe fiecare funcție de 10 000 de ori pe 2, 5, și 30 de parametri și vom analiza din nou media soluțiilor, deviația, minimul și maximul.

---

## Rezultatele experimentului

- ### FUNCȚIA RASTRIGIN

    ![](https://www.sfu.ca/~ssurjano/rastr2.png)

    Minimul global al funcției este 0, când toți parametrii au valoarea 0.
    
    x~i~ ∈ [-5.12, 5.12], pentru i = 1, ..., d

    Graficul funcției cu 2 parametri:
    
    ![](https://www.sfu.ca/~ssurjano/rastr.png)
    
---
    
    
- **RASTRIGIN 2 PARAMETRI**
    
 | Metoda | Nr. iteratii | Solutia minima | Solutia maxima | Media solutiilor | Deviatia standard | Timp rulare |
|:----------------------------------:|:------------:|:--------------:|:--------------:|:----------------:|:-----------------:|:---:|
| HILL CLIMBING  (best improvement) x30 | 100 | 3.027e-06 | 3.027e-06 | 3.027e-06 | 0 | 21s
| HILL CLIMBING  (first improvement) x30 | 100 | 6.054538e-07 | 2.240179e-05 | 4.076722e-06 | 4.572274e-06 | 18s
| SIMULATED ANNEALING | 10000 | 6.054538e-07 | 15.92933 | 4.579159 | 3.202226 | 2m 10s

![](https://i.imgur.com/myTFWiB.png)
![](https://i.imgur.com/Ao1xkbi.png)
---
- **RASTRIGIN 5 PARAMETRI**

| Metoda | Nr. iteratii | Solutia minima | Solutia maxima | Media solutiilor | Deviatia standard | Timp rulare
|:--------------------------------------:|:------------:|:--------------:|:--------------:|:----------------:|:-----------------:|:--:|
| HILL CLIMBING  (best improvement) x30 | 100 | 3.93545e-06 | 4.985067 | 2.245943 | 1.070562 | 1m 30s
| HILL CLIMBING  (first improvement) x30 | 100 | 3.057541e-05 | 2.990033 | 2.01848 | 0.5777003 | 3m 15s
| SIMULATED ANNEALING | 10000 | 1.320564 | 41.92923 | 14.3618 | 6.579299 | 4m 50s

![](https://i.imgur.com/eWQxDzS.png)
![](https://i.imgur.com/12mlU2N.png)
![](https://i.imgur.com/8Rkgu1G.png)

---

- **RASTRIGIN 30 PARAMETRI**

| Metoda | Nr. iteratii | Solutia minima | Solutia maxima | Media solutiilor | Deviatia standard | Timp rulare
|:--------------------------------------:|:------------:|:--------------:|:--------------:|:----------------:|:-----------------:|:--:|
| HILL CLIMBING  (best improvement) x30 | 25 | 210 | 234 | 226.5667 | 5.110391 | 4m
| HILL CLIMBING  (first improvement) x30 | 25 | 38.862 | 61.904 | 48.97647 | 5.711071 | 2h 30m
| SIMULATED ANNEALING | 10000 | 137.9132 | 384.1236 | 244.4421 | 38.18492 | 25m 6s

![](https://i.imgur.com/n3r0TJg.png)
![](https://i.imgur.com/2f6iQB1.png)
![](https://i.imgur.com/UDsbvjD.png)

---

- ### FUNCȚIA ACKLEY

    ![](https://www.sfu.ca/~ssurjano/ackley2.png)

    Valorile folosite sunt a=20, b=0.2, c=2π
    
    Minimul global al funcției este 0, când toți parametrii au valoarea 0
    
    x~i~ ∈ [-32.768, 32.768], pentru i = 1, ..., d

    Graficul funcției cu 2 parametri:
    
    ![](https://www.sfu.ca/~ssurjano/ackley.png)

---

-- **ACKLEY 2 PARAMETRI**

| Metoda | Nr. iteratii | Solutia minima | Solutia maxima | Media solutiilor | Deviatia standard | Timp rulare |
|:--------------------------------------:|:------------:|:--------------:|:--------------:|:----------------:|:-----------------:|:---:|
| HILL CLIMBING  (best improvement) x30 | 100 | 0.0002797688 | 2.231794 | 1.176493 | 1.050142 | 18s
| HILL CLIMBING  (first improvement) x30 | 100 | 0.0001250521 | 0.0001250521 | 0.0001250521 | 0 | 30s
| SIMULATED ANNEALING | 10000 | 0.0001250521 | 19.96677 | 2.14002 | 3.184884 | 2m 15s

![](https://i.imgur.com/RGv4EVo.png)
![](https://i.imgur.com/s1k1oPF.png)

---

-- **ACKLEY 5 PARAMETRI**

| Metoda | Nr. iteratii | Solutia minima | Solutia maxima | Media solutiilor | Deviatia standard | Timp rulare
|:--------------------------------------:|:------------:|:--------------:|:--------------:|:----------------:|:-----------------:|:--:|
| HILL CLIMBING  (best improvement) x30 | 100 | 2.139435 | 2.348296 | 2.291392 | 0.04494098 | 38s
| HILL CLIMBING  (first improvement) x30 | 100 | 0.0001250521 | 0.0001250521 | 0.0001250521 | 0 | 5m 49s
| SIMULATED ANNEALING | 10000 | 0.3015777 | 19.99341 | 9.365155 | 5.24811 | 5m 20s

![](https://i.imgur.com/0B6E94E.png)
![](https://i.imgur.com/yFrI9TM.png)

---

-- **ACKLEY 30 PARAMETRI**

| Metoda | Nr. iteratii | Solutia minima | Solutia maxima | Media solutiilor | Deviatia standard | Timp rulare |
|:--------------------------------------:|:------------:|:--------------:|:--------------:|:----------------:|:-----------------:|:--:|
| HILL CLIMBING  (best improvement) x30 | 25 | 2.467152 | 2.545542 | 2.508916 | 0.02301308 | 5m 8s
| HILL CLIMBING  (first improvement) x30 | 25 | 2.411027 | 2.888043 | 2.664627 | 0.1182601 | 5h 26m
| SIMULATED ANNEALING | 10000 | 17.86243 | 20.8811 | 20.0109 | 0.4369461 | 27m 20s

![](https://i.imgur.com/rSVQSCO.png)
![](https://i.imgur.com/w1GJDzo.png)
![](https://i.imgur.com/GeUug5E.png)

---

- ### FUNCȚIA DIXON-PRICE

    ![](https://www.sfu.ca/~ssurjano/dixonpr2.png)
    
    Minimul global al funcției: 
    
    ![](https://www.sfu.ca/~ssurjano/dixonpr3.png)
    
    x~i~ ∈ [-10, 10], pentru i = 1, ..., d

    Graficul funcției cu 2 parametri:
    
    ![](https://www.sfu.ca/~ssurjano/dixonpr.png)

---

-- **DIXON-PRICE 2 PARAMETRI**

| Metoda | Nr. iteratii | Solutia minima | Solutia maxima | Media solutiilor | Deviatia standard | Timp rulare
|:--------------------------------------:|:------------:|:--------------:|:--------------:|:----------------:|:-----------------:|:---:|
| HILL CLIMBING  (best improvement) x30 | 100 | 1.074008e-06 | 2.478457e-04 | 6.786213e-05 | 8.879594e-05 | 8s
| HILL CLIMBING  (first improvement) x30 | 100 | 1.570382e-05 | 3.924927e-03 | 6.222384e-04 | 1.174641e-03 | 23s
| SIMULATED ANNEALING | 10000 | 1.556196e-05 | 100.7616 | 18.07076 | 32.58397 | 2m 37s

![](https://i.imgur.com/pAKTxm2.png)
![](https://i.imgur.com/9bAhesC.png)
![](https://i.imgur.com/IJg4UwH.png)

---

-- **DIXON-PRICE 5 PARAMETRI**

| Metoda | Nr. iteratii | Solutia minima | Solutia maxima | Media solutiilor | Deviatia standard | Timp rulare
|:--------------------------------------:|:------------:|:--------------:|:--------------:|:----------------:|:-----------------:|:--:|
| HILL CLIMBING  (best improvement) x30 | 100 | 0.009301946 | 0.6668074 | 0.3788513 | 0.2433799 | 1m 56s
| HILL CLIMBING  (first improvement) x30 | 100 | 0.009809773 | 0.666683 | 0.3328484 | 0.2815964 | 6m 44s
| SIMULATED ANNEALING | 10000 | 0.04541871 | 10107.59 | 127.9927 | 642.3514 | 5m 2s

![](https://i.imgur.com/YjJDzt5.png)
![](https://i.imgur.com/A31mtyP.png)
![](https://i.imgur.com/Ko8DfNC.png)

---

-- **DIXON-PRICE 30 PARAMETRI**
| Metoda | Nr. iteratii | Solutia minima | Solutia maxima | Media solutiilor | Deviatia standard | Timp rulare |
|:--------------------------------------:|:------------:|:--------------:|:--------------:|:----------------:|:-----------------:|:--:|
| HILL CLIMBING  (best improvement) x30 | 25 | 187368 | 203152 | 198067.1 | 3758.145 | 5m
| HILL CLIMBING  (first improvement) x30 | 25 | 0.6666814 | 1.000093 | 0.7615168 | 0.1409038 | 9h 2m
| SIMULATED ANNEALING | 10000 | 26992.11 | 2439185 | 667836.3 | 386494.2 | 27m 2s

![](https://i.imgur.com/5wQcaX1.png)
![](https://i.imgur.com/dXez2K2.png)
![](https://i.imgur.com/n4pehNs.png)

---

-- ### FUNCȚIA ROSENBROCK

![](https://www.sfu.ca/~ssurjano/rosen2.png)
    
Minimul global al funcției este 0, când toți parametrii au valoarea 1

x~i~ ∈ [-2.048, 2.048], pentru i = 1, ..., d

Graficul funcției cu 2 parametri:

![](https://www.sfu.ca/~ssurjano/rosen.png)

---

-- **ROSENBROCK 2 PARAMETRI**

| Metoda | Nr. iteratii | Solutia minima | Solutia maxima | Media solutiilor | Deviatia standard | Timp Rulare |
|:--------------------------------------:|:------------:|:--------------:|:--------------:|:----------------:|:-----------------:|:-----------:|
| HILL CLIMBING  (best improvement) x30 | 100 | 5.906802e-07 | 4.807277e-04 | 9.555073e-05 | 1.1438e-04 | 20.4s |
| HILL CLIMBING  (first improvement) x30 | 100 | 1.49353e-06 | 2.43923e-04 | 7.555383e-05 | 6.176454e-05 | 19.5s |
| SIMULATED ANNEALING | 10000 | 6.163575e-07 | 16.13256 | 1.688637 | 2.540816 | 2m 16s |

![](https://i.imgur.com/kxmAR2H.png)
![](https://i.imgur.com/cxft6n5.png)
![](https://i.imgur.com/5Yrz37M.png)

---

-- **ROSENBROCK 5 PARAMETRI**

| Metoda | Nr. iteratii | Solutia minima | Solutia maxima | Media solutiilor | Deviatia standard | Timp Rulare |
|:--------------------------------------:|:------------:|:--------------:|:--------------:|:----------------:|:-----------------:|:-----------:|
| HILL CLIMBING  (best improvement) x30 | 100 | 0.0001203503 | 0.1057066 | 0.02281183 | 0.03130177 | 5m 30s |
| HILL CLIMBING  (first improvement) x30 | 100 | 0.002943086 | 0.07490109 | 0.024371 | 0.01992932 | 5m 59s |
| SIMULATED ANNEALING | 10000 | 0.05296301 | 174.4472 | 23.3788 | 31.64389 | 6m 10s |

![](https://i.imgur.com/vZor5vP.png)
![](https://i.imgur.com/vrnXSgt.png)
![](https://i.imgur.com/UWc5yL1.png)

---

-- **ROSENBROCK 30 PARAMETRI**
| Metoda | Nr. iteratii | Solutia minima | Solutia maxima | Media solutiilor | Deviatia standard | Timp Rulare |
|:--------------------------------------:|:------------:|:--------------:|:--------------:|:----------------:|:-----------------:|:-----------:|
| HILL CLIMBING  (best improvement) x30 | 25 | 22.91891 | 60.45753 | 30.05953 | 6.700672 | 5h 21m |
| HILL CLIMBING  (first improvement) x30 | 25 | 23.07029 | 29.23516 | 26.95261 | 1.593219 | 7h 9m |
| SIMULATED ANNEALING | 10000 | 438.6709 | 7025.985 | 2294.329 | 1011.439 | 29m 31s |

![](https://i.imgur.com/tbZb20D.png)
![](https://i.imgur.com/3wrOpcl.png)
![](https://i.imgur.com/gkoA8SH.png)



---


## Analiza rezultatelor și concluzii

| Algoritm | Gasit valoarea cea mai apropiata de minim |
|:-:|:-:|
| Best Improvement Hill Climb | 6 |
| First Improvement Hill Climb | 6 |
| Simulated Annealing | 2 |

(la variantele de 2 parametri ale functiilor Rastrigin și Ackley, First Improvement Hill Climb și Simulated Annealing au ajuns la același rezultat) 

După cum se observă, Simulated Annealing calilbrat cu datele din experimentul curent (T=100, T *= 0.95 la fiecare pas), deși se apropie de minim la un număr mic de parametri, precizia algoritmului scade pe măsură ce creștem numărul de dimensiuni, nefiind deloc aproape de rezultatul corect la nicio funcție pe 30 de dimensiuni. De asemenea, variația Simulated Annealing este semnificativ mai mare decât la variantele de Hill Climbing, după cum se poate observa pe graficele de dispersie a rezultatelor.

Între cele două variante de Hill Climbing, analiza duce la niște rezultate interesante. În majoritatea cazurilor, Best Improvement ajunge mult mai rapid într-un punct de minim local, astfel timpul de execuție al acestei variante este mai mic în ciuda faptului că analizează toți vecinii. Însă, dacă analizăm rezultatele, BI și FI au găsit valoarea cea mai apropiată de un număr egal de ori, iar First Improvement a avut rezultate mai bune pe un număr mare de parametri. Singura funcție pe care Best Improvement a găsit un rezultat mai bun decât First Improvement în 30 de dimensiuni este Rosenbrock, însă la o diferență de doar 0.16, FI având chiar o medie a rezultatelor mai mică decât BI. O anomalie semnificativă se poate observa la funcția Dixon Price cu 30 de parametri, unde First Improvement a găsit un minim mai mic decât 1 în 9 ore, în timp ce Best Improvement s-a blocat foarte rapid în minimi locali, terminând în 5 minute, însă având rezultate de ordinul sutelor de mii. Putem observa astfel că varianta First Improvement face pași mai mici spre minim și nu rămâne blocată în puncte de minim local foarte devreme, găsind rezultate mai bune pe 30 de dimensiuni, însă într-un timp semnificativ mai mare.

Putem conclude astfel, că performanța celor 3 algoritmi variază în funcție de numărul de dimeniuni, funcția folosită, numărul de rulări și timpul în care sunt lăsați să funcționeze. Calibrarea temperaturii folosită la Simulated Annealing a dat rezultate medii spre bune la un număr mic de dimensiuni, însă nu a dat rezultate deloc bune comparativ cu Hill Climbing pe 30 de dimensiuni. Best Improvement și First Improvement au fiecare avantajele lor în ce privește timpul de execuție și acuratețea rezultatelor, BI dând rezultate mai bune pe un număr mici de dimensiuni, iar FI având rezultate mai bune într-un timp mai mare pe un număr ridicat.

Putem spune, asftel, că rezultatele acestui experiment nu sunt îndeajuns de concludente pentru a putea trage o linie și a ajunge la o concluzie clară în ce privește performanța universală a acestor 3 algoritmi comparativ unul cu altul.



