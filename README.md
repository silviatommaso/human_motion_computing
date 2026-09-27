# Human Motion Computing

This repository contains the implementation and experimental analysis developed for the **Human Motion Computing** project.

The project investigates human movement recognition from inertial sensor data using **XROCKET** for time-series representation and a **Random Forest classifier** for movement classification.

The analysis focuses on three main aspects:

1. the contribution of different sensor signals and spatial axes;
2. the temporal scales used for movement recognition;
3. the interpretability of the most discriminative XROCKET patterns.

---

## Dataset

The project uses the **KSAS-Dataset**, which contains inertial recordings of five movements from the American Kenpo Karate *Blocking Set I*, together with recordings representing the absence of movement.

The six classes are:

| Class | Movement               |
| ----- | ---------------------- |
| M0    | Absence of movement    |
| M1    | Upward Block           |
| M2    | Hammering Inward Block |
| M3    | Extended Outward Block |
| M4    | Outward Downward Block |
| M5    | Rear Elbow Block       |

The dataset contains **240 instances**, obtained from 20 volunteers performing the movements with both arms.

Each instance contains 18 time series obtained from six sensor types, with one channel for each spatial axis (`x`, `y`, and `z`):

* Accelerometer
* Gravity
* Gyroscope
* Linear Acceleration
* Game Rotation Vector
* Magnetic Field

---

## Methodology

### XROCKET Representation

XROCKET is used to transform each multivariate time series into a fixed-dimensional feature representation.

The encoder is configured with:

| Parameter           |  Value |
| ------------------- | -----: |
| Kernel length       |      9 |
| Maximum kernel span |     33 |
| Maximum dilations   |     32 |
| Feature cap         | 10,000 |
| Combination order   |      1 |

The maximum kernel span was set to **33 samples**, approximately corresponding to the median length of the time-series instances.

With a kernel length of 9, XROCKET selected four dilation values:

| Dilation | Temporal span |
| -------: | ------------: |
|        1 |     9 samples |
|        2 |    17 samples |
|        3 |    25 samples |
|        4 |    33 samples |

Since `combination_order = 1`, each XROCKET feature operates on a single input channel.

### Classification

The XROCKET embeddings are classified using a `RandomForestClassifier`.

The dataset is divided into training and test sets using a **70/30 stratified split** with `random_state=42`.

---

## Experimental Analysis

### Task 1.1 — Sensor Signal Contribution

An ablation study is used to investigate the contribution of the inertial signals.

Different experiments remove:

* individual spatial axes (`x`, `y`, or `z`);
* combinations of spatial axes;
* individual sensor modalities;
* combinations of sensor modalities.

For each configuration, the XROCKET representation and Random Forest classifier are recomputed and the resulting classification performance is compared with the complete baseline.

Precision, recall, and confusion matrices are used to analyze how the removal of sensor information affects the different movement classes.

The experiments show that the movements rely on different combinations of translational, rotational, and orientation information and that the relevance of a sensor signal depends on the movement being recognized.

### Task 1.2 — Temporal Pattern Analysis

The second analysis investigates the temporal scales represented by the XROCKET dilation values.

Features associated with individual dilations or combinations of dilations are removed, and classification performance is measured again.

The results indicate that recognition does not depend exclusively on short-duration or long-duration patterns. Configurations containing only the shortest or only the longest temporal scales perform worse than representations combining different scales.

The results therefore support a **multi-scale temporal representation**, in which both local motion variations and broader movement structures contribute to recognition.

### Task 1.3 — Explainable Human Motion Computing

The final analysis investigates the most discriminative XROCKET features.

For each movement, a **one-vs-rest ANOVA F-test** is performed over the XROCKET representation. The 20 features with the highest F-score are selected and analyzed according to:

* sensor channel;
* dilation;
* F-score and p-value;
* mean activation for the considered movement;
* mean activation for the remaining movements.

The analysis shows that different movements are characterized by different combinations of sensor dynamics and temporal scales.

For example, the absence-of-movement class is mainly distinguished by reduced activation of dynamic patterns, while active movements exhibit characteristic combinations of acceleration, orientation, and rotational information.

These patterns provide an interpretable view of the information used to distinguish the movement classes, although they should not be interpreted as exact biomechanical descriptions of movement execution.

---

## Repository Structure

```text
human_motion_computing/
│
├── KSAS-Dataset/
│   └── movements/
│
├── experimental_results/
│   ├── task_1_1/
│   ├── task_1_2/
│   └── ...
│
├── results_analysis/
│   ├── axis_ablation.ipynb
│   ├── multiple_signal_ablation.ipynb
│   └── single_signal_ablation.ipynb
│
├── xrocket/
│
├── part_I.ipynb
├── utils.py
├── requirements.txt
├── README.md
└── .gitignore
```

`part_I.ipynb` contains the main experimental pipeline and analysis, while `utils.py` contains utility functions used for input generation and ablation experiments.

The `experimental_results` directory contains the metrics and intermediate results generated by the experiments.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/silviatommaso/human_motion_computing.git
cd human_motion_computing
```

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

After installing the dependencies, start Jupyter:

```bash
jupyter notebook
```

and open:

```text
part_I.ipynb
```

The notebook contains the implementation of the XROCKET pipeline and the experimental analyses for Tasks 1.1, 1.2, and 1.3.

---

## Main Findings

The experimental analysis highlights three main findings:

* **Sensor information is movement-dependent:** different gestures rely on different combinations of acceleration, orientation, and rotational information.
* **Temporal information is multi-scale:** combining different XROCKET dilation values is generally more effective than relying only on short or long temporal structures.
* **XROCKET features provide useful interpretability:** discriminative patterns can be related to specific sensor channels and temporal scales, providing insight into the information that distinguishes each movement.

These results show that movement recognition in the KSAS dataset depends on both **multi-sensor** and **multi-scale temporal information**.

---

## Generative AI Usage

ChatGPT was used as a Generative AI tool to support software implementation, debugging, organization of the experimental analyses.

The experimental design, execution of the experiments, and final evaluation of the obtained results were performed by the author.

---

## Author

**Silvia Tommaso**

Human Motion Computing Project