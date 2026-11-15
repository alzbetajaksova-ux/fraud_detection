# Fraud Detection – PaySim (OZ, TUKE)

Zadanie z predmetu Objavovanie znalostí: detekcia podvodných mobilných transakcií podľa metodológie CRISP-DM (úroveň 3).
Hlavný nástroj je RapidMiner (Altair AI Studio), Python len doplnkovo.

**Autori:** Betka (osoba A – úroveň 1), Martin (osoba B – úrovne 2 a 3)

## Dáta

Dataset PaySim (Kaggle: *Synthetic Financial Datasets For Fraud Detection*), súbor `PS_20174392719_1491204439457_log.csv`
(6 362 620 riadkov, 471 MB). Do repozitára sa nedáva – stiahni ho z Teams a ulož do `data/raw/`.

## Spustenie

1. Nainštaluj RapidMiner / Altair AI Studio a aktivuj edukačnú licenciu (bezplatná verzia má limit 10 000 riadkov).
2. Z Marketplace nainštaluj rozšírenia **Operator Toolbox** a **Python Scripting**.
3. V RapidMineri vytvor v `Local Repository` priečinok `fraud_detection` s podpriečinkami `data` a `models`.
4. Importuj procesy z `rapidminer/processes/` (File → Import Process) a spúšťaj ich v poradí 01 → 06.
5. Kontrola: po `02_priprava_dat` musí mať filtrovaný dataset 2 770 409 riadkov a 8 213 podvodov.

## Štruktúra

```
rapidminer/processes/        procesy 01–06 (.rmp)
rapidminer/building_blocks/  vyhodnotenie.rmp
python/                      doplnky (PR-AUC, grafy)
reports/figures/             grafy pre dokumentáciu
reports/results/             model_comparison.xlsx
```
