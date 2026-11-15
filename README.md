# Fraud Detection – PaySim (OZ, TUKE)

Zadanie z predmetu Objavovanie znalostí: detekcia podvodných mobilných transakcií podľa metodológie CRISP-DM (úroveň 3).
Hlavný nástroj je RapidMiner (Altair AI Studio), Python len doplnkovo (grafy, PR-AUC, ekonomika).

**Autori:** Betka (osoba A – úroveň 1), Martin (osoba B – úrovne 2 a 3)

## Dáta

Dataset PaySim (Kaggle: *Synthetic Financial Datasets For Fraud Detection*), súbor `PS_20174392719_1491204439457_log.csv`
(6 362 620 riadkov, 471 MB). Do gitu sa nedáva – stiahni ho z Teams a ulož do `data/raw/`.

## Príprava prostredia

1. Altair AI Studio s **edukačnou licenciou** (bezplatná verzia má limit 10 000 riadkov).
2. V AI Studiu: panel Repository → ≡ → **Create repository** → New local repository, alias `fraud_detection`,
   zrušiť „Use standard location“, Root directory = `<cesta k projektu>\rapidminer`.
3. V každom procese nastav makro **`projekt`** na cestu k priečinku projektu
   (otvor proces → View → Show Panel → **Context** → Macros → hodnota `projekt`, napr. `C:\Users\meno\fraud_detection`).
   Všetky cesty k súborom (CSV, výsledky) sa skladajú z tohto makra.

## Spustenie (poradie je dôležité)

| Proces | Čo robí | Trvanie | Kontrola |
|---|---|---|---|
| `01_import` | načíta CSV, uloží `data/paysim_raw` | ~3 min | 6 362 620 riadkov |
| `01_pochopenie_dat` | tabuľky podľa typu/hodiny/triedy, korelačná matica, spojenie s agregáciou príjemcov → `data/paysim_joined` | ~6 min | 3 CSV v `reports/results` |
| `02_priprava_dat` | filter TRANSFER/CASH_OUT, odvodené atribúty, váhy atribútov, split 70/30 → `data/train`, `data/test` | ~4 min | test = 831 123 riadkov |
| `03_baseline_modely` | logistická regresia a rozhodovací strom na S1/S2, vyhodnotenie train/test | ~4 min | 8 kontingenčných tabuliek + predikcie |

Dáta v `rapidminer/data/` a súbory `reports/results/03_predikcie_*.csv` sú mimo gitu – vzniknú spustením procesov.

Python doplnky (`pip install -r python/requirements.txt`):
- `python/eda_grafy.py` – grafy k prieskumu dát (kapitola 2)
- `python/roc_pr_grafy.py` – ROC a PR krivky modelov (po procese 03)
- `python/ekonomika.py` – zachránené/stratené sumy z kontingenčných tabuliek

## Sady atribútov

- **S1** (hlavná): `is_transfer`, `amount_log`, 4 zostatky, `hour`, `dest_tx_count`, `dest_total_amount`
- **S2**: S1 + `errorBalanceOrig`, `errorBalanceDest`, `drains_account`, `dest_zero_balances`
  (atribúty zo zostatkov robia úlohu takmer triviálnou – porovnanie metód a ladenie sa hodnotí na S1)

## Štruktúra

```
rapidminer/processes/   procesy 01–03 (.rmp), RapidMiner repozitár je priečinok rapidminer/
python/                 doplnkové skripty
reports/figures/        grafy pre dokumentáciu
reports/results/        výsledné tabuľky (CSV)
```
