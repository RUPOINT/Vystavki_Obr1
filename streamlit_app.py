# streamlit_app.py
# -*- coding: utf-8 -*-

import time
import pandas as pd
import streamlit as st
from ecwatech_export import load_exhibitors_any, save_excel, save_csv, save_json

st.set_page_config(page_title="EcwaTech Export", layout="wide")
st.title("Экспорт экспонентов → единая таблица (без логотипов)")

uploaded = st.file_uploader(
    "Загрузите целиковый файл (search.json или DOCX с JSON внутри)",
    type=["json", "docx"]
)

col1, col2, col3 = st.columns(3)
with col1:
    preview = st.number_input("Размер предпросмотра", 10, 2000, 100, 10)
with col2:
    do_xlsx = st.checkbox("Сохранить Excel", True)
with col3:
    do_csv = st.checkbox("Сохранить CSV", False)
do_json = st.checkbox("Сохранить очищенный JSON", False)

if uploaded:
    tmp = f"/tmp/{int(time.time())}_{uploaded.name}"
    with open(tmp, "wb") as f:
        f.write(uploaded.read())

    rows, n = load_exhibitors_any(tmp)
    st.success(f"Найдено записей: {n}")

    df = pd.DataFrame(rows)
    st.dataframe(df.head(int(preview)))

    if do_xlsx:
        fn = f"Экватэк_{int(time.time())}.xlsx"
        save_excel(rows, fn)
        with open(fn, "rb") as f:
            st.download_button("⬇️ Скачать Excel", f, file_name=fn,
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    if do_csv:
        fn = f"Экватэк_{int(time.time())}.csv"
        save_csv(rows, fn)
        with open(fn, "rb") as f:
            st.download_button("⬇️ Скачать CSV", f, file_name=fn, mime="text/csv")

    if do_json:
        fn = f"Экватэк_{int(time.time())}.json"
        save_json(rows, fn)
        with open(fn, "rb") as f:
            st.download_button("⬇️ Скачать JSON", f, file_name=fn, mime="application/json")
