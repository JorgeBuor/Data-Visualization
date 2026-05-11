# 🎓 University Student Analytics Dashboard

**Data Mining — Universidad de la Costa**  
**Author:** Jorge Estiiven Burgos Ortega

---

## Purpose

This project analyzes university student data covering applications, admissions, enrollment, retention, and satisfaction from 2015 to 2024. The goal is to identify key trends and support data-driven decision-making through an interactive dashboard built with Streamlit.

---

## Dataset

`university_student_data.csv` — contains the following columns:

| Column | Description |
|---|---|
| `Year` | Academic year (2015–2024) |
| `Term` | Academic term: Spring or Fall |
| `Applications` | Total applications received |
| `Admitted` | Students officially admitted |
| `Enrolled` | Students who enrolled |
| `Retention Rate (%)` | Percentage of students who continued the following term |
| `Student Satisfaction (%)` | Average satisfaction score from institutional surveys |
| `Engineering Enrolled` | Enrolled students in Engineering |
| `Business Enrolled` | Enrolled students in Business |
| `Arts Enrolled` | Enrolled students in Arts |
| `Science Enrolled` | Enrolled students in Science |

---

## Repository Structure

```
├── app.py                        # Streamlit dashboard
├── university_student_data.csv   # Dataset
├── requirements.txt              # Python dependencies
└── README.md                     # This file
└── Data_Visualization.ipynb      # Colab Notebook
```

---

## How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/JorgeBuor/Data-Visualization.git
   cd Data-Visualization
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## Dashboard Features

- **Sidebar filters:** year range, term (Spring / Fall), and department selection
- **KPI cards:** retention rate, satisfaction, total enrolled, applications, and admission rate — all with year-over-year deltas
- **Tab 1 — Retention & Satisfaction:** line chart and bar chart with trend line
- **Tab 2 — Spring vs Fall:** dual line plot and normalized comparison bar chart
- **Tab 3 — Department Breakdown:** donut chart and stacked bar chart
- **Tab 4 — Raw Data:** filterable table with CSV download option

---

## Deployment

The dashboard is deployed on **Streamlit Cloud**:  
🔗 `https://data-visualization-wvdygv9fcynjvvcadewyml.streamlit.app`

---

## Key Findings

- Retention rate grew consistently from **85% (2015)** to **90% (2024)**, with a slight dip in 2020.
- Student satisfaction increased from **78% to 88%** over the same period.
- Spring and Fall terms show virtually identical metrics across all indicators.
- Engineering leads department enrollment with ~38% of total students; Science shows a slight downward trend.
