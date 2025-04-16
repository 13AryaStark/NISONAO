
import streamlit as st
import pandas as pd
import plotly.express as px

# Загрузка данных
df = pd.read_csv("nisoplus_sample_data.csv")
students_df = pd.read_csv("nisoplus_students_sample.csv")

st.set_page_config(page_title="НИСО+ Дэшборд", layout="wide")
st.title("НИСО+ | Национальная Интегрированная Система Оценивания")

tab1, tab2 = st.tabs(["📊 Анализ по темам", "👩‍🎓 Анализ по ученикам"])

with tab1:
    st.markdown("### Сравнительный анализ по темам между внутренним и внешним оцениванием")
    selected_theme = st.selectbox("Выберите тему:", df["Тема"].unique())

    filtered = df[df["Тема"] == selected_theme].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Результат класса (СОЧ)", f"{filtered['Класс (внутр.)']}%")
        st.metric("Результат школы", f"{filtered['Школа']}%")
        st.metric("Результат региона", f"{filtered['Регион']}%")
        st.metric("Национальный уровень (МОДО)", f"{filtered['Нац. уровень (МОДО)']}%")
    with col2:
        st.metric("Отклонение класса от МОДО", f"{filtered['Отклонение (класс)']}%", delta_color="inverse")
        st.metric("Отклонение школы от МОДО", f"{filtered['Отклонение (школа)']}%", delta_color="inverse")

    st.markdown("### Визуализация сравнения")
    chart_df = pd.DataFrame({
        "Уровень": ["Класс", "Школа", "Регион", "МОДО"],
        "Результат (%)": [
            filtered["Класс (внутр.)"],
            filtered["Школа"],
            filtered["Регион"],
            filtered["Нац. уровень (МОДО)"]
        ]
    })
    fig = px.bar(chart_df, x="Уровень", y="Результат (%)", color="Уровень",
                 title=f"Результаты по теме: {selected_theme}", text_auto=True)
    st.plotly_chart(fig)

    st.markdown("#### Загрузка всех тем")
    st.dataframe(df.style.background_gradient(cmap='RdYlGn', subset=["Отклонение (класс)", "Отклонение (школа)"]))

with tab2:
    st.markdown("### Анализ индивидуальных результатов по теме 'Животные'")
    selected_student = st.selectbox("Выберите ученика:", students_df["Ученик"].unique())

    student_row = students_df[students_df["Ученик"] == selected_student].iloc[0]

    st.write(f"**Класс:** {student_row['Класс']} | **Школа:** {student_row['Школа']} | **Регион:** {student_row['Регион']}")
    st.metric("Результат СОЧ", f"{student_row['СОЧ (%)']}%")
    st.metric("Национальный уровень (МОДО)", f"{student_row['МОДО (%)']}%")
    st.metric("Отклонение от МОДО", f"{student_row['Отклонение от МОДО']}%", delta_color="inverse")

    st.markdown("### Сравнение с другими учениками")
    fig2 = px.bar(students_df, x="Ученик", y="СОЧ (%)", color="Отклонение от МОДО",
                  title="Результаты СОЧ по теме 'Животные'", text="СОЧ (%)")
    st.plotly_chart(fig2)

    st.markdown("#### Все ученики по теме")
    st.dataframe(students_df.style.background_gradient(cmap='RdYlGn', subset=["Отклонение от МОДО"]))
