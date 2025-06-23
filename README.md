# A/B Testing: Comparison of Bidding Strategies

This repository contains an A/B test analysis comparing two bidding strategies — **Maximum Bidding** and **Average Bidding** — based on user conversion performance. The analysis was conducted using a dataset simulating user behavior on a fictional e-commerce platform.

The project walks through data preparation, statistical assumption checks, and hypothesis testing to evaluate whether the new bidding strategy leads to significantly more purchases.

---

## 🔍 Objective

To determine if the new bidding method (*Average Bidding*) results in a higher average number of purchases compared to the existing method (*Maximum Bidding*).

---

## 📊 Dataset Description

The dataset includes two groups:

- **Control Group**: Exposed to *Maximum Bidding*
- **Test Group**: Exposed to *Average Bidding*

Each group includes the following metrics:

- `Impression`: Number of ad impressions
- `Click`: Number of clicks on the ads
- `Purchase`: Number of purchases after clicking
- `Earning`: Revenue generated from purchases

---

## 📈 Key Steps

- Data loading and exploration
- Combining control and test groups
- Defining null and alternative hypotheses
- Running normality and variance homogeneity tests
- Performing an independent samples t-test
- Interpreting test results

---

## ✅ Result Summary

- Statistical tests (Shapiro-Wilk, Levene, and t-test) were conducted.
- **p-value = 0.3493** → No statistically significant difference in average purchases between groups.
- **Recommendation**: Since no meaningful uplift was observed with the new strategy, sticking with the current method may be more cost-effective unless other business metrics suggest otherwise.

---

## 🛠 Tools Used

- Python
- Pandas
- NumPy
- SciPy
- Matplotlib

---

## 📁 File Structure

├── ab_testing.xlsx
├── ab_testing.py
├── README.md
