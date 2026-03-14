# Raport 1: OctoSpawn

## Opis gry
Hexspawn to determinstyczna gra dwuosobowa przypominająca szachy, która odbywa się na planszy 3x3. Wszystkie pionki poruszają się jak piony w szachach i wygrywa gracz, który albo dotrze do rzędu przeciwnika jednym ze swoich pionów, albo pozostawi go bez możliwych ruchów do wykonania. Octospawn to wersja tej gry, w której plansza ma wymiary 4x4. Obie te gry są grami rozwiązanymi, i w hexspawn gracz biały zawsze przegra po 3 turach przy optymalnej rozgrywce.


## Przeprowadzone Eksperymenty

## 1. Cel eksperymentów
Celem testów było porównanie wydajności i skuteczności trzech wariantów algorytmów przeszukiwania drzewa gry, zorientowanych na podejmowanie optymalnych decyzji w grach dwuosobowych o sumie zerowej:

*   **Negamax** – wersja podstawowa algorytmu Minimax, oparta na założeniu, że max(a, b) = min(-a, -b). Pozwala to na uproszczenie implementacji poprzez stosowanie tej samej logiki dla obu graczy (każdy dąży do maksymalizacji własnego wyniku, który jest negacją wyniku przeciwnika). Służy on jako punkt odniesienia (baseline) dla pozostałych metod.
*   **Negamax z odcięciem Alfa-Beta (AB)** – matematyczna optymalizacja, która eliminuje konieczność sprawdzania gałęzi drzewa niebędących w stanie wpłynąć na ostateczną decyzję. Dzięki utrzymywaniu granic dopuszczalnych wartości (alfa i beta), algorytm "odcina" ścieżki, o których już wiadomo, że prowadzą do wyników gorszych niż te wcześniej znalezione. Jest to optymalizacja bezstratna – zwraca identyczny wynik jak pełny Negamax, ale w znacznie krótszym czasie.
*   **Expectiminimax** – zaawansowane rozszerzenie dedykowane dla gier probabilistycznych, czyli takich, w których występuje element losowy (np. rzut kostką, rozdanie kart). Wprowadza on dodatkowe "węzły szansy" (chance nodes), w których nie wybieramy najlepszego ruchu, lecz obliczamy wartość oczekiwaną (średnią ważoną) wszystkich możliwych wyników losowych. Pozwala to algorytmowi ocenić ryzyko i wybierać ruchy statystycznie najkorzystniejsze w warunkach niepewności.


Eksperymenty można wykonać uruchamiając plik: **experiments.py**

---

## 2. Wyniki: Negamax vs Negamax Alfa-Beta (Zadanie 6 pkt)

### Środowisko Deterministyczne (20 gier)
| Algorytm A | Algorytm B | Wynik (A:B) | Śr. czas A | Śr. czas B |
| :--- | :--- | :---: | :---: | :---: |
| Negamax-5-AB | Negamax-10-AB | 10 : 10 | **5.34 ms** | 64.27 ms |
| Negamax-5-AB | Negamax-5 | 10 : 10 | **4.92 ms** | 38.81 ms |

**Wnioski:**
1.  **Potęga Alfa-Beta:** Zastosowanie odcięć skróciło czas obliczeń blisko **8-krotnie** (z ~39ms do ~5ms) przy zachowaniu identycznej jakości ruchów.
2.  **Sufit strategiczny:** Wynik 10:10 między głębokością 5 a 10 sugeruje, że gra przy głębokości 5 jest już "rozwiązana" – dalsze przeszukiwanie nie zmienia decyzji, a jedynie wydłuża czas.
3.  **Determinizm:** Idealnie równy podział wygranych wynika z braku losowości i naprzemiennego rozpoczynania partii.

### Środowisko Probabilistyczne (20 gier)
| Algorytm A | Algorytm B | Wynik (A:B) | Śr. czas A | Śr. czas B |
| :--- | :--- | :---: | :---: | :---: |
| Negamax-5-AB | Negamax-5 | 9 : 11 | 5.43 ms | 41.75 ms |
| Negamax-10-AB | Negamax-5 | 11 : 9 | 66.82 ms | 38.48 ms |

**Wnioski:**
1. **Wariacja:** Widać, że liczba wygranych nie jest równa co oznacza, że nie ma gwarancji wygranej znając kilka ruchów do przodu.

---

## 3. Wyniki: Expectiminimax (Zadanie 8 pkt)

### Środowisko Deterministyczne (Expectimax działa jak Negamax)
| Algorytm A | Algorytm B | Wynik (A:B) | Śr. czas A | Śr. czas B |
| :--- | :--- | :---: | :---: | :---: |
| Negamax-6-AB | Expectimax-6-AB | 8 : 7 | **8.01 ms** | 14.39 ms |

*Expectimax w grach deterministycznych wykazuje niewielki narzut czasowy (overhead) wynikający z dodatkowego sprawdzania warunków probabilistycznych, ale gra na tym samym poziomie co Negamax.*

### Środowisko Probabilistyczne (Kluczowy test)
| Algorytm A | Algorytm B | Wynik (A:B) | Śr. czas A | Śr. czas B |
| :--- | :--- | :---: | :---: | :---: |
| Negamax-6-AB | **Expectimax-6-AB** | 6 : **9** | **8.58 ms** | 488.05 ms |
| Negamax-6-AB | Expectimax-5 | 8 : 7 | **8.93 ms** | 1030.56 ms |

**Wnioski:**
1.  **Przewaga jakościowa:** Expectimax osiągnął lepszy bilans wygranych (**9:6**) przeciwko Negamaxowi. Udowadnia to, że uwzględnianie wartości oczekiwanej w węzłach losowych pozwala na podejmowanie lepszych decyzji w warunkach niepewności.
2.  **Eksplozja czasowa:** Czas ruchu w Expectimax wzrósł blisko **50-krotnie** w porównaniu do Negamaxa (z 8.5ms do 488ms). Wynika to z konieczności przeliczenia wszystkich możliwych wyników losowych w każdym węźle.
3.  **Efektywność optymalizacji:** Expectimax-6-AB (z odcięciami) jest **dwukrotnie szybszy** niż Expectimax-5 (bez odcięć), mimo że przeszukuje drzewo o jeden poziom głębiej. Pokazuje to, że odcięcia Alfa-Beta są kluczowe nawet w algorytmach probabilistycznych.

---

## 4. Podsumowanie
*   **Optymalizacja Alfa-Beta** drastycznie zwiększa zasięg czasowy algorytmu bez wpływu na jego logikę.
*   **Expectiminimax** jest niezbędny w grach z elementem losowym, aby grać skuteczniej niż standardowy Minimax, jednak kosztem bardzo dużego zapotrzebowania na moc obliczeniową.
*   W małych grach deterministycznych wyższa głębokość nie zawsze gwarantuje zwycięstwo, jeśli algorytm o mniejszej głębokości już gra optymalnie.


