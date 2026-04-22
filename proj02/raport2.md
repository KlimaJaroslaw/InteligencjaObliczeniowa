# Raport 2: STRIPS EasyAI

## Autorzy

**Paweł Knot**

**Jarosław Klima**


## Cel i zakres

Projekt implementuje algorytmy planowania w oparciu o reprezentację STRIPS (Stanford Research Institute Problem Solver). Celem jest demonstracja rozwiązywania problemów planowania na trzech poziomach zaawansowania:

- **Zadanie 1 (4 pkt)**: Podstawowe problemy planowania (Robot, BlockWorld, Monkey) z bezpośrednim planowaniem w przód (Forward Planning) oraz porównanie efektywności z heurystyką dla problemu Gripper
- **Zadanie 2 (6 pkt)**: Decomposition na podcele - rozbicie problemów na mniejsze, sekwencyjne zadania cząstkowe dla 3 domen (Gripper, BlockWorld, Monkey)
- **Zadanie 3 (8 pkt)**: Rozszerzone problemy planowania (3 warianty problemu Gripper z 8, 10 i 12 piłkami) z wieloma podcelami, każdy wymagający minimum 20 akcji

Raport dokumentuje wyniki planowania, wpływ funkcji heurystycznej na efektywność wyszukiwania oraz porównanie czasów wykonania z i bez heurystyk.


## Użyte domeny i problemy

### 1. Robot Delivery Domain
Domena opisu transportu paczek w budynku z wieloma pokojami. Parametry:
- **Lokalizacje**: cs (CompSci), off (office), lab (laboratory), mr (mail room)  
- **Cechy**: Robot Location (RLoc), Robot Has Coffee (RHC), Software in Compacts (SWC), Mail for Widget (MW), Robot Has Mail (RHM)
- **Akcje**: Poruszanie się między pokojami (8 akcji), podnoszenie/odkładanie przedmiotów (4 akcje)
- **Problem testowy**: Zanieś oprogramowanie do CompSci (cel: RLoc=off, SWC=False)

### 2. BlockWorld (4 bloki: a, b, c, d)
Klasyczny problem układanki z klockami. Parametry:
- **Obiekty**: 4 klocki + stół jako miejsce docelowe
- **Cechy**: on_X (gdzie jest klocek X), clear_X (czy klocek X jest czysty/pusty z góry)
- **Akcje**: Przeniesienie klocka z jednego miejsca na drugie (24 akcje dla 4 klocków)
- **Problem testowy**: Ułożenie wieży (d→c→b→a), stan początkowy: wieża d-c-b na stole, a oddzielnie

### 3. Gripper Domain
Problem transportu piłek między dwoma pokojami (roomA, roomB) za pomocą dwupalczastego chwytu. Parametry:
- **Obiekty**: Ball1-Ball4 (wersja bazowa), Ball1-Ball8 (8 piłek), Ball1-Ball10 (10 piłek), Ball1-Ball12 (12 piłek)
- **Cechy**: at_ballX (lokalizacja piłki: roomA, roomB, left, right), rob_at (położenie robota), free_left, free_right (stan chwytaków)
- **Akcje**: Ruch robota między pokojami, podniesienie piłki, upuszczenie piłki (liczba akcji rośnie z liczbą piłek)
- **Problemy testowe**: 
  - Bazowy (4 piłki, wszystkie z roomA do roomB)
  - Podcele (2 podcele po 2 piłki dla wersji bazowej)
  - Rozszerzone A/B/C (8/10/12 piłek z 2-3 podcelami, minimum 20+ akcji łącznie)

**Heurystyka dla Gripper**: Szacuje koszt pozostałych akcji na podstawie liczby piłek do transportu + koszty przejazdu robota.

### 4. Monkey Domain
Problem osiągnięcia i zdobycia owoców (banany) przez małpę z użyciem pudła jako podnóżka. Parametry:
- **Lokalizacje**: l1, l2, l3 (3 lokalizacje)
- **Cechy**: monkey_loc (położenie małpy), box_loc (położenie pudła), bananas_loc (położenie bananów), on_box (czy małpa na pudłe), has_bananas (czy ma banany)
- **Akcje**: Chodzenie do lokalizacji, pchanie pudła, wspinanie się na pudło, zrywanie bananów (7 akcji)
- **Problem testowy**: Małpa w l1, pudło w l2, banany w l3 → przenies pudło, wejdź, zerwij banany

---

## Zadanie 1 (4 pkt) - Podstawowe problemy planowania

**Wymagania**: 
- Minimum 3 problemy testowe
- Pomiarów czasu wykonania
- Porównanie efektywności z heurystyką

**Zaimplementowane testy**:

| Problem | Znalezione rozwiązanie | Koszt planu | Rozwinięte ścieżki | Czas [s] |
|---------|----------------------|-------------|-------------------|----------|
| Robot Delivery | ✓ | 5 | 17 | 0.001 |
| BlockWorld (4 bloki) | ✓ | 4 | 42 | 0.004 |
| Monkey (3 lokalizacje) | ✓ | 4 | 13 | 0.001 |
| Gripper bez heurystyki | ✓ | 11 | 255 | 0.025 |
| Gripper z heurystyką | ✓ | 11 | 117 | 0.012 |

**Obserwacje**:
- Wszystkie 3 podstawowe problemy rozwiązane w pełni
- Problem Gripper demonstruje wpływ heurystyki: redukcja z 255 do 117 ekspansji (~54% zmniejszenie)
- Czas wykonania poprawiony 2× dzięki heurystyce (0.025s → 0.012s)
- Plan optimality zachowana (koszt 11 zarówno z heurystyką jak i bez)

---

## Zadanie 2 (6 pkt) - Podcele i heurystyki

**Wymagania**:
- Minimum 3 domeny z podcelami (2+ podcele na domenę)
- Porównanie czasów/ścieżek z heurystyką dla co najmniej jednej domeny

**Zaimplementowane podcele**:

### Gripper - Subgoal porównanie (z/bez heurystyki)

| Problem | Bez heurystyki (ścieżki) | Z heurystyką (ścieżki) | Przyspieszenie | Koszt |
|---------|--------------------------|------------------------|-----------------|-------|
| Subgoal 1 | 103 | 6 | **17.2×** | 5 |
| Subgoal 2 | 73 | 6 | **12.2×** | 5 |

**Efekt heurystyki**: Dramatyczne zmniejszenie przestrzeni przeszukiwania bez wpływu na optimalność planu.

### BlockWorld - Subcele

| Problem | Koszt | Rozwinięte ścieżki | Czas [s] | Status |
|---------|-------|-------------------|----------|--------|
| Subgoal 1 (d→c, c→b) | 4 | 33 | 0.003 | ✓ |
| Subgoal 2 (dodaj b→a) | 1 | 3 | 0.000 | ✓ |
| **Razem** | **5** | — | **0.003** | ✓ |

### Monkey - Subcele

| Problem | Koszt | Rozwinięte ścieżki | Czas [s] | Status |
|---------|-------|-------------------|----------|--------|
| Subgoal 1 (przenieś pudło) | 1 | 3 | 0.000 | ✓ |
| Subgoal 2 (zerwij banany) | 3 | 13 | 0.001 | ✓ |
| **Razem** | **4** | — | **0.001** | ✓ |

**Wnioski z Zadania 2**:
- Decomposition na podcele redukuje koszt całkowity (4→5 dla kumul., ale rozszerza możliwości)
- Heurystyka gripper_heuristic zapewnia spersonalizowaną optymalizację dla domeny
- BlockWorld i Monkey mają mniejszą przestrzeń poszukiwań, heurystyka byłaby mniej istotna

---

## Zadanie 3 (8 pkt) - Problemy rozszerzone (20+ akcji)

**Wymagania**:
- Minimum 3 dodatkowe problemy
- Każdy musi mieć 20+ akcji łącznie
- Mogą wykorzystywać podcele

### Problem A: 8 piłek (2 podcele, min. 20 akcji)

| Subgoal | Koszt | Rozwinięte | Czas [s] | Cele |
|---------|-------|-----------|----------|------|
| A.1: Ball 1-4 A→B | 11 | 201 | 0.033 | ✓ |
| A.2: Ball 5-8 A→B | 11 | 107 | 0.019 | ✓ |
| **Razem** | **22** | 308 | **0.052** | **✓ (>20)** |

### Problem B: 10 piłek (3 podcele, min. 25 akcji)

| Subgoal | Koszt | Rozwinięte | Czas [s] | Cele |
|---------|-------|-----------|----------|------|
| B.1: Ball 1-4 A→B | 11 | 233 | 0.054 | ✓ |
| B.2: Ball 5-8 A→B | 11 | 141 | 0.032 | ✓ |
| B.3: Ball 9-10 A→B | 5 | 6 | 0.001 | ✓ |
| **Razem** | **27** | 380 | **0.087** | **✓ (>25)** |

### Problem C: 12 piłek (3 podcele, min. 30 akcji)

| Subgoal | Koszt | Rozwinięte | Czas [s] | Cele |
|---------|-------|-----------|----------|------|
| C.1: Ball 1-4 A→B | 11 | 291 | 0.081 | ✓ |
| C.2: Ball 5-8 A→B | 11 | 183 | 0.051 | ✓ |
| C.3: Ball 9-12 A→B | 11 | 107 | 0.027 | ✓ |
| **Razem** | **33** | 581 | **0.159** | **✓ (>30)** |

**Weryfikacja wymagań**:
- Problem A: 22 akcji (przekracza minimum 20)
- Problem B: 27 akcji (przekracza minimum 25)
- Problem C: 33 akcji (przekracza minimum 30)
- Wszystkie podcele zaimplementowane z heurystyką
- Rozwiązania znalezione dla każdego wariantu

---

## Analiza heurystyki gripper_heuristic

**Funkcja h(state, goal)**:
```python
h(state) = liczba(piłek do transportu) 
         + lokalizacjapiłek (dodatkowe koszty)
         + pozycja robota
```

**Efekt**: Zmniejszenie liczby rozwijanych węzłów w przeszukiwaniu

| Problem | Bez heurystyki (węzły) | Z heurystyką (węzły) | Przyspieszenie |
|---------|----------------------|----------------------|-----------------|
| Gripper 4 piłki | 255 | 117 | **2.18×** |
| Subgoal 1 (2 piłki) | 103 | 6 | **17.2×** |
| Subgoal 2 (2 piłki) | 73 | 6 | **12.2×** |

**Obserwacje**:
- Heurystyka zapewnia przyrost efektywności rosnący wraz z zmniejszeniem problemu
- Dla dużych problemów (4 piłki): 2.18× przyspieszenie
- Dla małych podcelów (2 piłki): 12-17× przyspieszenie
- Brak wzrostu kosztu planu → optymalna heurystyka (admissible)

---

## Wyniki i obserwacje

### Podsumowanie wyników wszystkich zadań

| Zadanie | Problemy | Status | Uwagi |
|---------|----------|--------|-------|
| 1 (4 pkt) | 3 domeny + Gripper | **OK** | Timing zmierzony, heurystyka porównana |
| 2 (6 pkt) | 6 podcelów, 3 domeny | **OK** | Heurystyka wykazuje dramatyczną poprawę |
| 3 (8 pkt) | 3 problemy, 22/27/33 akcji | **OK** | Wszystkie wymagania przekroczone |

---

## Wnioski

1. **Forward Planning + Heurystyka**: Kombinacja Forward_STRIPS z heurystyką gripper_heuristic wykazuje praktyczną efektywność, szczególnie dla problemów o większej złożoności.

2. **Decomposition Effectiveness**: Rozbicie na podcele umożliwia:
   - Szybsze wyszukiwanie dla podproblemów
   - Logiczne grupowanie akcji
   - Redukcję szumu wyszukiwania na poziomie całego problemu

3. **Heurystyka Domain-Specific**: Opracowana heurystyka dla domeny Gripper jest znacznie bardziej efektywna niż blind search (17× dla małych instancji), wskazując na wartość ekspertyz.

4. **Skalowanie**: Algorytm skaluje się do co najmniej 12 piłek (33 akcji), utrzymując czasy poniżej 0.17s.