import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, chi2_contingency


# Загрузка CSV-файла
def load_data(file_path):
    data = pd.read_csv(file_path)

    return data


# Проверка гипотезы о различии количества пропущенных дней между мужчинами и женщинами
def compare_gender(data, num_sick_days):
    male_data = data[data['Sex'] == 'М']
    female_data = data[data['Sex'] == 'Ж']

    t_statistic, p_value = ttest_ind(male_data['Num_sick_days'] > num_sick_days,
                                     female_data['Num_sick_days'] > num_sick_days)

    if p_value < 0.05:
        return "Мужчины пропускают значимо чаще женщин."
    else:
        return "Нет значимой разницы в количестве пропусков между мужчинами и женщинами."


# Проверка гипотезы о различии количества пропущенных дней между сотрудниками старше и младше 35 лет
def compare_age(data, age, num_sick_days):
    cross_table = pd.crosstab(data['Age'] > age, data['Num_sick_days'] > num_sick_days)
    chi2, p_value, _, _ = chi2_contingency(cross_table)

    if p_value < 0.05:
        return f"Сотрудники старше {age} лет пропускают значимо чаще своих более молодых коллег."
    else:
        return f"Нет значимой разницы в количестве пропусков между сотрудниками старше {age} лет" \
               f" и их более молодыми коллегами."


# Отображение графиков распределений
def plot_distributions(data, age, num_sick_days):
    male_data = data[data['Sex'] == 'М']
    female_data = data[data['Sex'] == 'Ж']
    young_data = data[data['Age'] <= age]
    old_data = data[data['Age'] > age]
    st.set_option('deprecation.showPyplotGlobalUse', False)

    male_data = male_data[male_data['Num_sick_days'] > num_sick_days]
    female_data = female_data[female_data['Num_sick_days'] > num_sick_days]
    # График сравнения количества пропущенных дней между мужчинами и женщинами
    plt.figure(figsize=(8, 6))
    plt.boxplot([male_data['Num_sick_days'], female_data['Num_sick_days']],
                labels=['Мужчины', 'Женщины'])
    plt.xlabel('Пол')
    plt.ylabel('Количество пропущенных дней')
    plt.title('Сравнение количества пропущенных дней между мужчинами и женщинами')
    st.pyplot()

    # Гистограмма сравнения количества пропущенных дней между мужчинами и женщинами
    plt.figure(figsize=(8, 6))
    plt.hist([male_data['Num_sick_days'], female_data['Num_sick_days']],
             bins=10, label=['Мужчины', 'Женщины'])
    plt.xlabel('Количество пропущенных дней')
    plt.ylabel('Частота')
    plt.title('Сравнение количества пропущенных дней между мужчинами и женщинами')
    plt.legend()
    st.pyplot()

    young_data = young_data[young_data['Num_sick_days'] > num_sick_days]
    old_data = old_data[old_data['Num_sick_days'] > num_sick_days]

    # График сравнения количества пропущенных дней между сотрудниками старше и младше 35 лет
    plt.figure(figsize=(8, 6))
    plt.boxplot([old_data['Num_sick_days'], young_data['Num_sick_days']],
                labels=[f'Старше {age} лет', f'Моложе {age} лет'])
    plt.xlabel('Возрастная группа')
    plt.ylabel('Количество пропущенных дней')
    plt.title('Сравнение количества пропущенных дней между сотрудниками старше 35 лет и моложе 35 лет')
    st.pyplot()

    # Гистограмма сравнения количества пропущенных дней между сотрудниками старше и младше 35 лет
    plt.figure(figsize=(8, 6))
    plt.hist([old_data['Num_sick_days'], young_data['Num_sick_days']],
             bins=10, label=[f'Старше {age} лет', f'Моложе {age} лет'])
    plt.xlabel('Количество пропущенных дней')
    plt.ylabel('Частота')
    plt.title('Сравнение количества пропущенных дней между сотрудниками старше 35 лет и моложе 35 лет')
    plt.legend()
    st.pyplot()


# Главная функция для отображения дашборда
def main():
    st.title("Анализ статистики по пропущенным дням")

    # Загрузка CSV-файла
    file_path = st.file_uploader("Выберите CSV-файл", type="csv")
    if file_path:
        data = load_data(file_path)

        # Отображение таблицы с данными
        st.subheader("Данные")
        st.write(data)
        data['Age'] = data['Age'].astype(int)

        # Задание параметров age и Num_sick_days
        age = st.slider("Выберите возраст", min_value=int(data['Age'].min()), max_value=int(data['Age'].max()))
        num_sick_days = st.slider("Выберите количество рабочих дней", min_value=int(data['Num_sick_days'].min()),
                              max_value=int(data['Num_sick_days'].max()))

        # Проверка гипотез и вывод результатов
        st.subheader("Результаты проверки гипотез")

        # Проверка гипотезы о различии количества пропущенных дней между мужчинами и женщинами
        st.write(f"Гипотеза: 1)	Мужчины пропускают в течение года более {num_sick_days} рабочих дней по болезни значимо чаще женщин.")
        st.write(compare_gender(data, num_sick_days))

        # Проверка гипотезы о различии количества пропущенных дней между сотрудниками старше и младше 35 лет
        st.write(f"Гипотеза: 2)	Работники старше {age} лет пропускают в течение года более {num_sick_days} рабочих"
                 " дней по болезни значимо чаще своих более молодых коллег.")
        st.write(compare_age(data, age, num_sick_days))

        # Отображение графиков распределений
        st.subheader("Графики распределений")
        plot_distributions(data, age, num_sick_days)


# Запуск дашборда
if __name__ == "__main__":
    main()
