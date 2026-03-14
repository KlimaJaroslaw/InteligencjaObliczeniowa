# Raport 1: OctoSpawn

## Opis gry
Hexspawn to determinstyczna gra dwuosobowa przypominająca szachy, która odbywa się na planszy 3x3. Wszystkie pionki poruszają się jak piony w szachach i wygrywa gracz, który albo dotrze do rzędu przeciwnika jednym ze swoich pionów, albo pozostawi go bez możliwych ruchów do wykonania. Octospawn to wersja tej gry, w której plansza ma wymiary 4x4. Obie te gry są grami rozwiązanymi, i w hexspawn gracz biały zawsze przegra po 3 turach przy optymalnej rozgrywce.


## Przeprowadzone Eksperymenty

## 1. Cel eksperymentów
Celem testów było porównanie wydajności i skuteczności trzech wariantów algorytmów:
*   **Negamax** – wersja podstawowa (brute-force).
*   **Negamax z odcięciem Alfa-Beta (AB)** – optymalizacja ograniczająca liczbę odwiedzanych węzłów.
*   **Expectiminimax** – algorytm dedykowany dla gier probabilistycznych, uwzględniający węzły losowe (chance nodes).

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


