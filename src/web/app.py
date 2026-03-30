import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import json
import os

from src.config import DB_URL, PROCESSED_DATA_TABLE, QUALITY_REPORT_PATH, RESEARCH_REPORT_PATH, PLOTS_TABLE, DATA_URL

st.set_page_config(page_title="National Team Analysis 2023", layout="wide")
st.title("📊 Аналітична панель: Національна збірна 2023")
st.link_button(label="Data Source", url=DATA_URL)

st.header("1. Огляд даних (TOP-10)")
try:
    engine = create_engine(DB_URL)
    df_preview = pd.read_sql(f"SELECT * FROM {PROCESSED_DATA_TABLE} LIMIT 10", engine)
    st.dataframe(df_preview, width="stretch")
except Exception as e:
    st.error(f"Помилка завантаження таблиці: {e}")

st.header("2. Аналітичні звіти")
col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Quality Analysis")
    if os.path.exists(QUALITY_REPORT_PATH):
        with open(QUALITY_REPORT_PATH, "r", encoding="utf-8") as f:
            q_data = json.load(f)
            st.json(q_data)
    else:
        st.warning(f"Файл {QUALITY_REPORT_PATH} не знайдено")

with col2:
    st.subheader("🔬 Research Report")
    if os.path.exists(RESEARCH_REPORT_PATH):
        with open(RESEARCH_REPORT_PATH, "r", encoding="utf-8") as f:
            r_data = json.load(f)
            st.write(r_data)
    else:
        st.warning(f"Файл {RESEARCH_REPORT_PATH} не знайдено")

st.header("3. Візуалізація результатів")
try:
    plots_df = pd.read_sql(f"SELECT * FROM {PLOTS_TABLE}", engine)
    
    if not plots_df.empty:
        img_cols = st.columns(2)
        for idx, row in plots_df.iterrows():
            plot_path = row['file_path'] 
            
            with img_cols[idx % 2]:
                if os.path.exists(plot_path):
                    st.image(plot_path, caption=f"Графік: {row['plot_name']}")
                else:
                    st.info(f"Файл {plot_path} відсутній на диску")
    else:
        st.info("Таблиця графіків порожня.")
except Exception as e:
    st.error(f"Помилка завантаження графіків: {e}")
