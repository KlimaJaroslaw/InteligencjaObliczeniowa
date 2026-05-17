# Sprawozdanie: Uczenie ze Wzmocnieniem w środowisku CarRacing

## 1. Autorzy
- Paweł Knot
- Jarosław Klima

---

# Na 4 pkt

## 2. Środowisko: CarRacing

### 2.1. Opis środowiska
- Nazwa środowiska: CarRacing-v3
- Typ przestrzeni akcji:
  - ciągła (continuous=True)
  - dyskretna (continuous=False)
- Obserwacje:
  - obraz RGB o stałym rozmiarze zwracany jako klatki w czasie
  - testowo: grayscale (nie poprawił wyników)
  - frame stacking (n_stack=4) dla uchwycenia dynamiki ruchu pojazdu

### 2.2. Cel agenta
- Maksymalizacja średniej nagrody epizodu
- Stabilna jazda po torze bez utknięcia
- Utrzymanie auta na asfalcie i płynne pokonywanie zakrętów

### 2.3. Miary oceny
- eval/mean_reward
- rollout/ep_rew_mean
- eval/mean_ep_length
- rollout/ep_len_mean
- Dodatkowo jakościowo: obserwacja przejazdu modelu w trybie renderowania

---

## 3. Rozwiązanie problemu z PPO

### 3.1. Dlaczego PPO
- Stabilność uczenia (mechanizm clipping)
- Dobre działanie dla zadań sterowania ciągłego
- Mniejsza wrażliwość na pojedyncze niestabilne aktualizacje niż A2C

### 3.2. Konfiguracja bazowa PPO
- Policy: CnnPolicy
- gamma: 0.99 (bazowo)
- środowisko: CarRacing-v3 continuous
- opakowanie środowiska: Monitor + DummyVecEnv + VecFrameStack(n_stack=4)
- eval callback: eval_freq=10000, n_eval_episodes=10, deterministic=True
- budżet uczenia: total_timesteps=500000
- logging: monitor.csv + TensorBoard


Krzywa uczenia: średnia nagroda z ewaluacji na przestrzeni kolejnych epok treningu:
![PPO wykres nagrody](./imgs/ppo_99.png)

Krzywa uczenia: średnia nagroda z fazy rollout (eksploracji) na przestrzeni kolejnych kroków treningowych:
![PPO wykres nagrody podczas uczenia](./imgs/ppo_99_train.png)



### 3.3. Wyniki bazowe PPO
Uczenie PPO przebiegało stabilnie: po początkowej fazie eksploracji model stopniowo zwiększał średnią nagrodę, a krzywa ewaluacyjna miała wyraźny trend rosnący.

Najlepszy wariant PPO (gamma=0.99) osiągał najwyższe wartości `eval/mean_reward` spośród wszystkich testów i wyraźnie przewyższał zarówno warianty gamma=0.9 i gamma=0.999.

Po treningu agent jechał płynnie po torze, lepiej utrzymywał się na drodze i rzadziej wpadał w oscylacje sterowania.

W modelu nie występuje zjawisko przeuczenia, ponieważ wyniki uzyskiwane podczas treningu (rollout) oraz ewaluacji są ze sobą zbieżne.

---

# Na 6 pkt

## 4. Porównanie trzech współczynników dyskontowych w algorytmie PPO dla ciągłej przestrzeni akcji

### 4.1. Założenia eksperymentu
- Testowane wartości gamma:
  - 0.9
  - 0.99
  - 0.999
- Pozostałe hiperparametry bez zmian
- Taki sam budżet treningu dla każdego modelu

### Definicja i trening modeli:

```python
# PPO 0.9
eval_env = gym.make("CarRacing-v3",render_mode="rgb_array",continuous=True)
eval_env = Monitor(eval_env)
eval_env = DummyVecEnv([lambda: eval_env])
eval_env = VecFrameStack(eval_env, n_stack=4)
eval_callback = EvalCallback(
    eval_env, 
    best_model_save_path="./logs/best_model/",
    log_path="./logs/results/", 
    eval_freq=10000,
    deterministic=True,
    n_eval_episodes=10,
    render=False,
    verbose=0,
)
model_car = PPO("CnnPolicy",env_car,gamma=0.9,verbose=0,tensorboard_log=tb_log_dir)
model_car.learn(total_timesteps=500_000,callback=eval_callback,tb_log_name="05_mln_g99_cont")
```

```python
# PPO 0.99
eval_env = gym.make("CarRacing-v3",render_mode="rgb_array",continuous=True)
eval_env = Monitor(eval_env)
eval_env = DummyVecEnv([lambda: eval_env])
eval_env = VecFrameStack(eval_env, n_stack=4)
eval_callback = EvalCallback(
    eval_env, 
    best_model_save_path="./logs/best_model/",
    log_path="./logs/results/", 
    eval_freq=10000,
    deterministic=True,
    n_eval_episodes=10,
    render=False,
    verbose=0,
)
model_car = PPO("CnnPolicy",env_car,gamma=0.99,verbose=0,tensorboard_log=tb_log_dir)
model_car.learn(total_timesteps=500_000,callback=eval_callback,tb_log_name="05_mln_g99_cont")
```

```python
# PPO 0.999
eval_env = gym.make("CarRacing-v3",render_mode="rgb_array",continuous=True)
eval_env = Monitor(eval_env)
eval_env = DummyVecEnv([lambda: eval_env])
eval_env = VecFrameStack(eval_env, n_stack=4)
eval_callback = EvalCallback(
    eval_env, 
    best_model_save_path="./logs/best_model/",
    log_path="./logs/results/", 
    eval_freq=10000,
    deterministic=True,
    n_eval_episodes=10,
    render=False,
    verbose=0,
)
model_car = PPO("CnnPolicy",env_car,gamma=0.999,verbose=0,tensorboard_log=tb_log_dir)
model_car.learn(total_timesteps=500_000,callback=eval_callback,tb_log_name="05_mln_g999_cont")
```

### 4.2. Wyniki

Krzywa uczenia: średnia nagroda z ewaluacji (eval/mean_reward) na przestrzeni kolejnych kroków treningowych dla wszystkich trzech modeli:
![PPO wykres nagrody](./imgs/ppo_all.png)

Krzywa uczenia: średnia nagroda z fazy rollout (rollout/ep_rew_mean) na przestrzeni kolejnych kroków treningowych:
![PPO wykres nagrody podczas uczenia](./imgs/ppo_all_train.png)

Wykresy TensorBoard (`eval/mean_reward` i `rollout/ep_rew_mean`) wskazały, że najlepszy przebieg uczenia uzyskano dla `gamma=0.99`.

Zestawienie jakościowe końcowych rezultatów:

| Wariant PPO | Stabilność uczenia | Końcowa jakość jazdy | Ocena ogólna |
|---|---|---|---|
| gamma=0.9 | niska | model źle kieruje pojazdem | słaba |
| gamma=0.99 | wysoka | najbardziej płynna jazda, najlepsza nagroda | najlepsza |
| gamma=0.999 | średnia | słaba jazda, ale lepsza niż 0.9 | średnia |

### 4.3. Interpretacja
Najlepszy okazał się współczynnik `gamma=0.99`, ponieważ daje dobry kompromis między nagrodą natychmiastową i długoterminową.

`gamma=0.9` powodował zbyt krótkowzroczne decyzje (model za bardzo faworyzował szybki, lokalny zysk). Z kolei `gamma=0.999` zwiększał horyzont planowania, ale utrudniał stabilne uczenie i spowalniał poprawę polityki.

---

# Na 8 pkt

## 5. Implementacja dwóch algorytmów PPO i A2C oraz ich porównanie

### 5.1. Opis implementacji
PPO i A2C zaimplementowano w Stable-Baselines3 na identycznym pipeline środowiska (CarRacing-v3, continuous=True, Monitor, DummyVecEnv, VecFrameStack).

Wspólne elementy eksperymentu:
- to samo środowisko i ten sam preprocessing danych wejściowych,
- ta sama procedura ewaluacji (`EvalCallback`),
- porównywalny budżet treningowy (`500000` kroków).

Różnica dotyczyła algorytmu aktualizacji polityki: PPO (clipping) vs A2C (klasyczny actor-critic bez clippingu).



### 5.2. Porównanie wyników PPO vs A2C

Krzywa uczenia: średnia nagroda z ewaluacji (eval/mean_reward) na przestrzeni kolejnych kroków treningowych dla modelu PPO oraz A2C:
![PPO wykres nagrody](./imgs/ppo_a2c.png)

Krzywa uczenia: średnia nagroda z fazy rollout (rollout/ep_rew_mean) na przestrzeni kolejnych kroków treningowych dla porównywanych modeli:
![PPO wykres nagrody podczas uczenia](./imgs/ppo_a2c_train.png)

Na wykresach ewaluacyjnych PPO osiągało wyraźnie wyższe wartości `eval/mean_reward` i bardziej stabilny trend uczenia. A2C kompletnie sobie nie radziło.

Zestawienie jakościowe:

| Algorytm | Stabilność | Wynik końcowy | Zachowanie auta |
|---|---|---|---|
| PPO | wysoka | najwyższy | płynna jazda, mniej błędów |
| A2C | niska | niższy | częste utraty toru, brak rezultatów |

### 5.3. Wniosek z porównania
- PPO osiąga lepsze i stabilniejsze wyniki niż A2C.
W środowisku CarRacing zadanie jest trudne (ciągłe sterowanie, obraz jako wejście, opóźnione skutki decyzji). PPO lepiej radzi sobie z taką dynamiką.

---

## 6. Optymalizacja hiperparametrów (PPO i A2C)

### 6.1. Cel i metodologia
- Celem tej części jest automatyczne przeszukiwanie hiperparametrów metodą random search dla dwóch algorytmów: PPO i A2C.
- Punkt startowy dla obu algorytmów stanowią wcześniej wytrenowane modele.
- Każda epoka random search losuje nowy zestaw parametrów z zdefiniowanej przestrzeni i uruchamia dalsze dotrenowanie modelu.

### 6.2. PPO: przestrzeń strojenia
W random search dla PPO uwzględniono następujące hiperparametry:

- learning_rate: [1e-4, 2e-4, 3e-4, 5e-4]
- n_steps: [128, 256, 512, 1024, 2048, 4096]
- ent_coef: [0.0, 0.001, 0.005, 0.01, 0.02]


### 6.3. A2C: przestrzeń strojenia
W random search dla A2C uwzględniono następujące hiperparametry:

- learning_rate: [5e-5, 1e-4, 2e-4, 3e-4]
- n_steps: [16, 32, 64]
- gae_lambda: [0.95, 0.97, 0.99]

### 6.4. Wyniki optymalizacji
Krzywa uczenia: średnia nagroda z ewaluacji (eval/mean_reward) na przestrzeni kolejnych kroków treningowych dla optymalizowanych modeli:
![PPO wykres nagrody](./imgs/fine_tune.png)

Krzywa uczenia: średnia nagroda z fazy rollout (rollout/ep_rew_mean) na przestrzeni kolejnych kroków treningowych dla porównywanych modeli:
![PPO wykres nagrody podczas uczenia](./imgs/fine_tune_train.png)

Optymalizacja modeli bazujących na algorytmie A2C nie przyniosła oczekiwanych rezultatów – modele te wykazały brak stabilności lub niską efektywność w zadanym środowisku. Z kolei algorytm PPO skutecznie poprawił swoje wyniki, osiągając najwyższą wydajność przy następującej konfiguracji hiperparametrów:

Najlepszy PPO: 
``` json
{
  'epoch': 1,
  'algo': 'PPO',
  'params':
  {
    'learning_rate': 0.0003,
    'n_steps': 2048,
    'ent_coef': 0.001
  },
  'eval_freq': 1000,
  'total_timesteps': 30000,
  'best_mean_reward': 923.76,
  'model_path': './logs/fine_tune/models\\ppo_epoch_1.zip'
}
```

---

## 7. Wnioski

### 7.1. Najważniejsze obserwacje
Przeprowadzone eksperymenty pokazują, że w środowisku CarRacing najbardziej skutecznym i jednocześnie najstabilniejszym algorytmem okazało się PPO. Spośród testowanych wartości współczynnika dyskontowego najlepsze rezultaty dała konfiguracja z gamma równym 0.99, która zapewniała najlepszy kompromis pomiędzy reagowaniem na bieżące zdarzenia na torze a planowaniem długoterminowym. W praktyce przekładało się to na wyższą średnią nagrodę oraz płynniejsze prowadzenie pojazdu. W porównaniu z PPO algorytm A2C był wyraźnie bardziej wrażliwy na dobór parametrów i częściej wykazywał niestabilność uczenia, przez co trudniej było uzyskać powtarzalne, wysokie wyniki.

### 7.2. Ograniczenia eksperymentu
Najważniejszym ograniczeniem badań był dostępny budżet obliczeniowy, który ograniczał zarówno liczbę pełnych przebiegów treningu, jak i zakres możliwych eksperymentów porównawczych. Dodatkowo liczba powtórzeń z różnymi seedami była ograniczona, co utrudnia pełną ocenę odporności wyników na losowość procesu uczenia. W badaniach wykorzystano również skończoną przestrzeń hiperparametrów, dlatego nie można wykluczyć, że lepsze konfiguracje znajdują się poza testowanymi zakresami. Z tego samego powodu przedstawiony proces strojenia należy traktować jako etap wstępny, a nie wyczerpującą optymalizację całej przestrzeni parametrów.
