# 🌙 CycleAware

**CycleAware** is a machine learning-based tool designed to **predict the phase of the menstrual cycle** based on physiological and exertion data such as training duration, distance, and perceived effort. By understanding which phase an individual is in, **CycleAware** helps improve training efficiency and keeps a check on both **physical readiness** and **mental well-being**.

---

## 🧩 Problem Statement

Tracking menstrual cycle phases is critical for optimizing physical performance, reducing injury risk, and supporting psychological well-being. Traditional cycle tracking relies heavily on manual input or hormone monitoring, which is often inaccessible. **CycleAware** offers an AI-driven alternative by classifying menstrual cycle phases using training and subjective exertion data — enabling smarter, cycle-informed decisions in sports and daily health.

---

## 🔍 Features

- 📅 **Menstrual Cycle Phase Prediction** (phases encoded from 1 to 4)
- 🧠 **Supports Mental Well-Being** via sRPE and RPE tracking
- 🚀 **Hybrid ML Model**: TabNet embeddings + Random Forest classifier
- 💾 Model persistence for deployment-ready use
- 📊 Evaluation reports with accuracy and classification metrics

---

## 🔢 Input Parameters

| Feature  | Description                       |
|----------|-----------------------------------|
| `durata` | Duration of the training session  |
| `DistTOT`| Total distance covered            |
| `HSR`    | High-speed running (intensity)    |
| `ACC`    | Accelerations                     |
| `DEC`    | Decelerations                     |
| `RPE`    | Rating of Perceived Exertion      |
| `sRPE`   | Session RPE (RPE × duration)      |

- **Target**: `phase` (Encoded menstrual cycle phase from 1 to 4)

---

## ⚙️ Tech Stack

- Python (Pandas, NumPy)
- Scikit-learn
- PyTorch TabNet (`pytorch-tabnet`)
- Google Colab or Jupyter Notebook

---
