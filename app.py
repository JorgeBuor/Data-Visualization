import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="University Analytics Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 University Student Analytics Dashboard")
st.caption("Data Mining — Universidad de la Costa | Author: Samuel")

# ── Carga del dataset ────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("university_student_data.csv")
    return df

df = load_data()

dept_cols  = ["Engineering Enrolled", "Business Enrolled",
              "Arts Enrolled", "Science Enrolled"]
dept_names = ["Engineering", "Business", "Arts", "Science"]

# ── Filtros interactivos ─────────────────────────────────────────────────────
st.sidebar.header("🔎 Filters")

years_available = sorted(df["Year"].unique())
year_range = st.sidebar.select_slider(
    "Year range",
    options=years_available,
    value=(years_available[0], years_available[-1])
)

term_filter = st.sidebar.multiselect(
    "Term",
    options=["Spring", "Fall"],
    default=["Spring", "Fall"]
)

dept_filter = st.sidebar.multiselect(
    "Department (enrollment view)",
    options=dept_names,
    default=dept_names
)

show_grid = st.sidebar.checkbox("Show grid on charts", value=True)
palette   = st.sidebar.selectbox("Color palette", ["muted", "Set2", "pastel", "dark"])

# ── Filtrado del dataframe ───────────────────────────────────────────────────
mask = (
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1]) &
    (df["Term"].isin(term_filter))
)
df_f = df[mask].copy()

if df_f.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ── KPI Cards ────────────────────────────────────────────────────────────────
st.subheader("📊 Key Metrics")

avg_retention    = df_f["Retention Rate (%)"].mean()
avg_satisfaction = df_f["Student Satisfaction (%)"].mean()
total_enrolled   = df_f["Enrolled"].sum()
total_apps       = df_f["Applications"].sum()
admit_rate       = (df_f["Admitted"].sum() / total_apps * 100) if total_apps > 0 else 0

# Deltas respecto al año más temprano del filtro
df_first = df_f[df_f["Year"] == df_f["Year"].min()]
df_last  = df_f[df_f["Year"] == df_f["Year"].max()]

delta_ret  = df_last["Retention Rate (%)"].mean()    - df_first["Retention Rate (%)"].mean()
delta_sat  = df_last["Student Satisfaction (%)"].mean() - df_first["Student Satisfaction (%)"].mean()
delta_enr  = df_last["Enrolled"].sum()               - df_first["Enrolled"].sum()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Avg Retention Rate",    f"{avg_retention:.1f}%",    f"{delta_ret:+.1f}% vs first year")
col2.metric("Avg Satisfaction",      f"{avg_satisfaction:.1f}%", f"{delta_sat:+.1f}% vs first year")
col3.metric("Total Enrolled",        f"{total_enrolled:,}",      f"{delta_enr:+,} vs first year")
col4.metric("Total Applications",    f"{total_apps:,}")
col5.metric("Avg Admission Rate",    f"{admit_rate:.1f}%")

st.divider()

# ── Visualizaciones ──────────────────────────────────────────────────────────
st.subheader("📈 Trend Analysis")

tab1, tab2, tab3, tab4 = st.tabs([
    "📉 Retention & Satisfaction",
    "🏫 Spring vs Fall",
    "🥧 Department Breakdown",
    "📋 Raw Data"
])

import matplotlib as mpl
colors = plt.get_cmap(
    {"muted": "tab10", "Set2": "Set2", "pastel": "Pastel1", "dark": "Dark2"}[palette]
).colors

# ────────────────────────────────────────────────────────────────────────────
# TAB 1: Retention Rate & Satisfaction trends
# ────────────────────────────────────────────────────────────────────────────
with tab1:
    yearly = (
        df_f.groupby("Year")[["Retention Rate (%)", "Student Satisfaction (%)"]]
        .mean()
        .reset_index()
    )

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # ── Retention Rate — línea ───────────────────────────────────────────────
    axes[0].plot(
        yearly["Year"], yearly["Retention Rate (%)"],
        marker="o", linewidth=2.5, color=colors[0],
        markersize=8, markerfacecolor="white", markeredgewidth=2
    )
    axes[0].fill_between(yearly["Year"], yearly["Retention Rate (%)"],
                         alpha=0.12, color=colors[0])
    for _, row in yearly.iterrows():
        axes[0].annotate(
            f"{row['Retention Rate (%)']:.1f}%",
            xy=(row["Year"], row["Retention Rate (%)"]),
            xytext=(0, 9), textcoords="offset points",
            ha="center", fontsize=8.5, fontweight="bold", color=colors[0]
        )
    axes[0].set_title("Retention Rate Trends Over Time", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Academic Year", fontsize=11)
    axes[0].set_ylabel("Retention Rate (%)", fontsize=11)
    axes[0].set_xticks(yearly["Year"])
    axes[0].tick_params(axis="x", rotation=45)
    axes[0].yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
    axes[0].grid(show_grid, alpha=0.4)

    # ── Satisfaction — barras + línea de tendencia ───────────────────────────
    bars = axes[1].bar(
        yearly["Year"], yearly["Student Satisfaction (%)"],
        color=[colors[i % len(colors)] for i in range(len(yearly))],
        edgecolor="white", width=0.6, alpha=0.85
    )
    axes[1].plot(
        yearly["Year"], yearly["Student Satisfaction (%)"],
        color="darkred", linewidth=1.8, linestyle="--",
        marker="D", markersize=5, label="Trend"
    )
    for bar in bars:
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.2,
            f"{bar.get_height():.1f}%",
            ha="center", va="bottom", fontsize=8.5, fontweight="bold"
        )
    axes[1].set_title("Student Satisfaction by Year", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Academic Year", fontsize=11)
    axes[1].set_ylabel("Satisfaction (%)", fontsize=11)
    axes[1].set_xticks(yearly["Year"])
    axes[1].tick_params(axis="x", rotation=45)
    axes[1].yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
    axes[1].legend(fontsize=10)
    axes[1].grid(show_grid, alpha=0.4)

    plt.tight_layout()
    st.pyplot(fig)

# ────────────────────────────────────────────────────────────────────────────
# TAB 2: Spring vs Fall comparison
# ────────────────────────────────────────────────────────────────────────────
with tab2:
    if len(term_filter) < 2:
        st.info("Select both Spring and Fall in the sidebar to see this comparison.")
    else:
        enrolled_term = (
            df_f.groupby(["Year", "Term"])["Enrolled"]
            .sum()
            .reset_index()
        )
        term_avg = (
            df_f.groupby("Term")[["Applications", "Enrolled",
                                   "Retention Rate (%)", "Student Satisfaction (%)"]]
            .mean()
            .reset_index()
        )

        fig, axes = plt.subplots(1, 2, figsize=(13, 5))

        # ── sns-style lineplot manual ────────────────────────────────────────
        for i, term in enumerate(["Spring", "Fall"]):
            sub = enrolled_term[enrolled_term["Term"] == term]
            axes[0].plot(
                sub["Year"], sub["Enrolled"],
                marker="o", linewidth=2.2, label=term,
                color=colors[i], markersize=7
            )
        axes[0].set_title("Enrolled Students: Spring vs Fall", fontsize=13, fontweight="bold")
        axes[0].set_xlabel("Academic Year", fontsize=11)
        axes[0].set_ylabel("Enrolled Students", fontsize=11)
        axes[0].set_xticks(df_f["Year"].unique())
        axes[0].tick_params(axis="x", rotation=45)
        axes[0].legend(title="Term")
        axes[0].grid(show_grid, alpha=0.4)

        # ── Bar chart comparativo de métricas ────────────────────────────────
        metrics_labels = ["Applications", "Enrolled", "Retention\nRate (%)", "Satisfaction\n(%)"]
        metric_keys    = ["Applications", "Enrolled", "Retention Rate (%)", "Student Satisfaction (%)"]
        x     = np.arange(len(metric_keys))
        width = 0.35

        spring_row = term_avg[term_avg["Term"] == "Spring"]
        fall_row   = term_avg[term_avg["Term"] == "Fall"]

        if not spring_row.empty and not fall_row.empty:
            sv = spring_row[metric_keys].values[0]
            fv = fall_row[metric_keys].values[0]
            maxv = np.maximum(sv, fv)
            sn = np.where(maxv > 0, sv / maxv * 100, 0)
            fn = np.where(maxv > 0, fv / maxv * 100, 0)

            b1 = axes[1].bar(x - width/2, sn, width, label="Spring",
                             color=colors[0], alpha=0.85, edgecolor="white")
            b2 = axes[1].bar(x + width/2, fn, width, label="Fall",
                             color=colors[1], alpha=0.85, edgecolor="white")

            for bar in list(b1) + list(b2):
                axes[1].text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.6,
                    f"{bar.get_height():.1f}",
                    ha="center", va="bottom", fontsize=8
                )

            axes[1].set_title("Term Metrics Comparison (Normalized to 100)",
                              fontsize=13, fontweight="bold")
            axes[1].set_xticks(x)
            axes[1].set_xticklabels(metrics_labels, fontsize=9)
            axes[1].set_ylabel("Relative Score (max = 100)", fontsize=11)
            axes[1].set_ylim(0, 115)
            axes[1].legend(title="Term")
            axes[1].grid(show_grid, alpha=0.4)

        plt.tight_layout()
        st.pyplot(fig)

# ────────────────────────────────────────────────────────────────────────────
# TAB 3: Department Breakdown
# ────────────────────────────────────────────────────────────────────────────
with tab3:
    selected_dept_cols  = [c for c, n in zip(dept_cols, dept_names) if n in dept_filter]
    selected_dept_names = [n for n in dept_names if n in dept_filter]

    if not selected_dept_cols:
        st.info("Select at least one department in the sidebar.")
    else:
        dept_totals  = df_f[selected_dept_cols].sum()
        dept_by_year = df_f.groupby("Year")[selected_dept_cols].mean()
        dept_by_year.columns = selected_dept_names

        fig, axes = plt.subplots(1, 2, figsize=(13, 5))

        # ── Donut chart ──────────────────────────────────────────────────────
        pie_colors = [colors[i % len(colors)] for i in range(len(selected_dept_cols))]
        wedges, texts, autotexts = axes[0].pie(
            dept_totals,
            labels=selected_dept_names,
            autopct="%1.1f%%",
            startangle=90,
            colors=pie_colors,
            wedgeprops={"edgecolor": "white", "linewidth": 1.8, "width": 0.65}
        )
        for at in autotexts:
            at.set_fontsize(10)
            at.set_fontweight("bold")
        centre_circle = plt.Circle((0, 0), 0.35, fc="white")
        axes[0].add_artist(centre_circle)
        axes[0].set_title("Overall Enrollment Share by Department",
                          fontsize=13, fontweight="bold")

        # ── Stacked bar por año ──────────────────────────────────────────────
        dept_by_year.plot(
            kind="bar", stacked=True,
            color=pie_colors, edgecolor="white",
            alpha=0.88, ax=axes[1]
        )
        axes[1].set_title("Avg Enrollment per Department by Year",
                          fontsize=13, fontweight="bold")
        axes[1].set_xlabel("Academic Year", fontsize=11)
        axes[1].set_ylabel("Average Enrolled Students", fontsize=11)
        axes[1].tick_params(axis="x", rotation=45)
        axes[1].legend(title="Department", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
        axes[1].grid(show_grid, alpha=0.4)

        plt.tight_layout()
        st.pyplot(fig)

# ────────────────────────────────────────────────────────────────────────────
# TAB 4: Raw data
# ────────────────────────────────────────────────────────────────────────────
with tab4:
    st.write(f"Showing **{len(df_f)}** records matching the current filters.")
    st.dataframe(df_f.reset_index(drop=True), use_container_width=True)
    st.download_button(
        label="⬇️ Download filtered data as CSV",
        data=df_f.to_csv(index=False).encode("utf-8"),
        file_name="university_filtered_data.csv",
        mime="text/csv"
    )

st.divider()
st.caption("Universidad de la Costa — Data Mining | Activity I: Data Visualization & Dashboard Deployment")
