import streamlit as st
import pandas as pd
import numpy as np

# --- Generate spoof financial data ---
np.random.seed(42)

years = [2021, 2022, 2023]
companies = ["Acme Corp", "Globex Inc", "Soylent LLC", "Initech", "Umbrella Co"]

data = []
for year in years:
    for company in companies:
        revenue = np.random.randint(5_000_000, 50_000_000)
        expenses = np.random.randint(2_000_000, 30_000_000)
        profit = revenue - expenses
        data.append({
            "Year": year,
            "Company": company,
            "Revenue ($)": revenue,
            "Expenses ($)": expenses,
            "Profit ($)": profit
        })

df = pd.DataFrame(data)

# --- Streamlit UI ---
st.title("📊 Spoof Financial Dashboard")

year_selected = st.selectbox("Select a Year", sorted(df["Year"].unique(), reverse=True))
filtered_df = df[df["Year"] == year_selected]

sort_by = st.selectbox("Sort by", ["Revenue ($)", "Expenses ($)", "Profit ($)"])
sorted_df = filtered_df.sort_values(by=sort_by, ascending=False)

st.dataframe(sorted_df, use_container_width=True)

st.markdown("---")
st.caption("This is fake financial data used for demo purposes only.")
