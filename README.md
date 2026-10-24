# Rein Room: Supplementary Material (Anonymized for Review)

This repository contains the supplementary material for a study that compares a browser-based reinforcement learning (RL) teaching platform ("Rein Room", RR) with a code-based Gymnasium + Google Colab workflow in a two-group classroom experiment.

All names, institutional details, student identifiers and platform URLs have been removed or replaced for anonymous review. Student IDs in the response data are replaced by pseudonyms (`P01`, `P02`, ...; `TEST01` is a test account excluded from analysis).

## Contents

| Path | Description |
|------|-------------|
| `notebooks/` | Colab notebooks for both groups (`RL_Day1*.ipynb`, `RL_Day2*.ipynb`) and `rr_envs.py`, a local re-implementation of the RR environments used in the notebooks. |
| `B.教學執行/` | Teaching materials: lesson plans for the RR group and the Gymnasium + Colab group, task plan, questionnaire design. |
| `C.數據收集/` | Pre-/post-test response data (CSV, pseudonymized), task completion records, and the analysis scripts (`analysis_v2.py`, `nasa_tlx_breakdown.py`, `timing_analysis.py`, `open_ended_extract.py`). |
| `figures/` | Scripts and HTML sources for the figures (`extract_data.py` builds `data.js` from the CSV files). |

## Study design in brief

- Two groups, each taught in two sessions: RR platform (experimental) and Gymnasium + Colab (control).
- Instruments: an 8-item knowledge test (concept understanding and chart reading), task completion records, NASA-TLX, the System Usability Scale (SUS), a 5-item platform feedback scale, and open-ended questions.
- Analysis: paired samples with non-parametric tests (Wilcoxon signed-rank, Mann-Whitney U), effect size r, chi-square with Cramer's V for completion rates.

## Reproducing the analysis

```
cd C.數據收集
python analysis_v2.py
python nasa_tlx_breakdown.py
python timing_analysis.py
```

Figure data: `python figures/extract_data.py`.

The RR notebooks download `rr_envs.py` from this anonymized repository (`notebooks/rr_envs.py`); alternatively, upload the file to the Colab session manually.
