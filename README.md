# 🛡️ Sentinel Spam Shield — AI SMS & Email Threat Detection

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![NLTK](https://img.shields.io/badge/NLTK-NLP-blue?style=for-the-badge)](https://www.nltk.org/)
[![Precision](https://img.shields.io/badge/Model%20Precision-100%25%20(1.0)-00f59b?style=for-the-badge)](https://github.com/Chitranshsri/SMS-Spam-Detection)
[![License](https://img.shields.io/badge/License-MIT-00f2fe?style=for-the-badge)](LICENSE)

<br/>

**An end-to-end Machine Learning web application engineered with Natural Language Processing (NLP), TF-IDF Vectorization, and Multinomial Naive Bayes — wrapped in a futuristic, glassmorphic Streamlit interface.**

[Explore Repository](https://github.com/Chitranshsri/SMS-Spam-Detection) • [Report Bug](https://github.com/Chitranshsri/SMS-Spam-Detection/issues) • [Request Feature](https://github.com/Chitranshsri/SMS-Spam-Detection/issues)

</div>

---

## 📌 Executive Summary

With the exponential surge in automated spam campaigns, SMS phishing (*smishing*), and financial fraud, real-time message classification is a vital security layer. 

**Sentinel Spam Shield** is an end-to-end AI system trained on the **SMS Spam Collection dataset (5,572+ records)**. It transforms raw, noisy natural language text into dense semantic vector representations and runs real-time inference using a **Multinomial Naive Bayes** classifier tuned specifically for **Zero False Positives (100% Precision)** — guaranteeing legitimate user messages are never falsely quarantined.

---

## ✨ Key Features

- **🔬 High-Precision NLP Preprocessing**: Multi-stage cleaning pipeline featuring case normalization, NLTK word tokenization, alphanumeric filtering, stopword stripping, and Porter Stemming.
- **⚡ Sparse Matrix TF-IDF Vectorization**: 3,000 top n-gram feature mappings capturing high-frequency deceptive vocabulary.
- **🎯 1.0 Precision Benchmark**: Evaluated against multiple classifiers (SVC, Random Forest, Logistic Regression, KNN) and optimized for **100% precision** to eliminate false positive classification.
- **🎨 Futuristic Glassmorphism UI**: Built with Streamlit and custom CSS injection — featuring cosmic animated radial gradients, Orbitron/Space Grotesk typography, and glowing cyber accents.
- **🚨 Dynamic Threat Visualization**: Responsive UI cards that dynamically shift between glowing crimson (Spam / Malicious) and emerald green (Verified Safe) with model confidence certainty meters.
- **⚡ 1-Click Interactive Presets**: Pre-configured sample payloads allowing recruiters, evaluators, and users to test spam vs. legitimate classifications instantly.
- **🔍 Pipeline Transparency**: Includes an expandable preprocessed token breakdown showing raw input transformed into stemmed token arrays.

---

## 🏗️ System Architecture & Workflow

```mermaid
flowchart TD
    A([Raw Input Message]) --> B[1. Lowercase Normalization]
    B --> C[2. NLTK Tokenization]
    C --> D[3. Alphanumeric & Punctuation Filter]
    D --> E[4. English Stopword Removal]
    E --> F[5. Porter Stemming]
    F --> G[6. TF-IDF Vectorizer max_features=3000]
    G --> H[7. Multinomial Naive Bayes Classifier]
    H --> I{Spam or Ham?}
    I -->|Class 1: Spam| J[🚨 Red Glowing Threat Card + Advisory]
    I -->|Class 0: Ham| K[🛡️ Green Glowing Safe Card + Certainty Score]
