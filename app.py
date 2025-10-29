import re
import os
import pandas as pd
import streamlit as st
from datetime import datetime
import base64
from io import StringIO

# Настройка страницы
st.set_page_config(
    page_title="OZON SKU Extractor",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def extract_sku_from_text(text):
    """
    Извлекает SKU из текста. SKU должны быть 9 или 10 цифр, не начинаться с 0
    """
    # Ищем SKU в ссылках (между '-' и '/')
    pattern_links = r'-(\d{9,10})/'
    sku_from_links = re.findall(pattern_links, text)
    
    # Ищем SKU в любом тексте (9-10 цифр, не начинающихся с 0)
    pattern_anywhere = r'(?<!\d)([1-9]\d{8,9})(?!\d)'
    sku_from_text = re.findall(pattern_anywhere, text)
    
    # Объединяем оба списка
    all_sku = sku_from_links + sku_from_text
    
    # Удаляем дубликаты и проверяем валидность SKU
    unique_sku = []
    seen_sku = set()
    
    for sku in all_sku:
        # Проверяем, что SKU состоит только из цифр и не был добавлен ранее
        if sku.isdigit() and sku not in seen_sku:
            unique_sku.append(sku)
            seen_sku.add(sku)
    
    # Сортируем для удобства
    unique_sku.sort()
    return unique_sku

def get_csv_download_link(df, filename):
    """Генерирует ссылку для скачивания CSV файла"""
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Скачать CSV файл</a>'
    return href

def main():
    # Заголовок приложения
    st.title("🛍️ OZON SKU Extractor")
    st.markdown("---")
    
    # Сайдбар с информацией
    with st.sidebar:
        st.header("ℹ️ Информация")
        st.markdown("""
        **Формат SKU:**
        - Из ссылок: `...-1650868905/...`
        - Из текста: числа 9-10 цифр, не начинающиеся с 0
        
        **Примеры валидных SKU:**
        - 1650868905
        - 123456789
        - 9876543210
        """)
        
        st.markdown("---")
        st.markdown("**💡 Подсказка:**")
        st.markdown("Вставьте текст со ссылками OZON или любой текст содержащий SKU")
        
        st.markdown("---")
        st.markdown("With ❤️ by mroshchupkin and DS")
    
    # Основная область
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 Ввод данных")
        
        # Пример текста по умолчанию
        default_text = """Ссылки OZON:
https://www.ozon.ru/product/salfetki-ot-pyaten-na-odezhde-vlazhnye-pyatnovyvodyashchie-sredstvo-ochishchayushchie-1650868905/?at=46tRgwAkNhXyZOEBt1zBAK8FkDN5R6c15lRwvI5VV8jY
https://www.ozon.ru/product/noutbuk-apple-macbook-air-13-m1-8gb-256gb-space-gray-1234567890/
https://www.ozon.ru/product/telefon-samsung-galaxy-s21-987654321/?param=value

Текст с SKU:
Заказ номер 123456789, товары: 9876543210, 555666777, 8889990001.
Некорректные: 012345678 (начинается с 0), 12345 (мало цифр), 12345678901 (много цифр)."""
        
        # Текстовое поле для ввода
        input_text = st.text_area(
            "Вставьте текст со ссылками OZON или любой текст:",
            value=default_text,
            height=300,
            placeholder="Вставьте ваш текст здесь..."
        )
        
        # Кнопки действий
        col1_1, col1_2, col1_3 = st.columns(3)
        
        with col1_1:
            extract_btn = st.button("🔍 Извлечь SKU", type="primary", use_container_width=True)
        with col1_2:
            clear_btn = st.button("🗑️ Очистить", use_container_width=True)
        with col1_3:
            if st.button("📋 Пример", use_container_width=True):
                st.experimental_rerun()
    
    with col2:
        st.subheader("📤 Результаты")
        
        # Инициализация session state для хранения SKU
        if 'sku_list' not in st.session_state:
            st.session_state.sku_list = []
        if 'extraction_stats' not in st.session_state:
            st.session_state.extraction_stats = {"found": 0, "duplicates": 0}
        
        # Обработка кнопки очистки
        if clear_btn:
            st.session_state.sku_list = []
            st.session_state.extraction_stats = {"found": 0, "duplicates": 0}
            st.experimental_rerun()
        
        # Обработка извлечения SKU
        if extract_btn and input_text.strip():
            with st.spinner("Извлекаем SKU..."):
                try:
                    sku_list = extract_sku_from_text(input_text)
                    
                    # Статистика
                    original_count = len(re.findall(r'-(\d{9,10})/', input_text)) + len(re.findall(r'(?<!\d)([1-9]\d{8,9})(?!\d)', input_text))
                    duplicate_count = original_count - len(sku_list)
                    
                    st.session_state.sku_list = sku_list
                    st.session_state.extraction_stats = {
                        "found": len(sku_list),
                        "duplicates": duplicate_count
                    }
                    
                except Exception as e:
                    st.error(f"Ошибка при извлечении SKU: {str(e)}")
        
        # Отображение результатов
        if st.session_state.sku_list:
            # Статистика
            stats = st.session_state.extraction_stats
            st.success(f"✅ Найдено SKU: {stats['found']}")
            if stats['duplicates'] > 0:
                st.info(f"♻️ Удалено дубликатов: {stats['duplicates']}")
            
            # Поле с результатами
            result_text = "\n".join(st.session_state.sku_list)
            st.text_area("Найденные SKU:", value=result_text, height=200)
            
            # Кнопка скачивания
            st.markdown("---")
            st.subheader("💾 Сохранение результатов")
            
            if st.session_state.sku_list:
                # Создаем DataFrame для скачивания
                df = pd.DataFrame(st.session_state.sku_list, columns=["SKU"])
                timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
                filename = f"sku_{timestamp}.csv"
                
                # Ссылка для скачивания
                st.markdown(get_csv_download_link(df, filename), unsafe_allow_html=True)
                
                # Предпросмотр таблицы
                st.markdown("**Предпросмотр данных:**")
                st.dataframe(df, use_container_width=True)
        
        else:
            if extract_btn and not input_text.strip():
                st.warning("⚠️ Введите текст для извлечения SKU")
            elif extract_btn:
                st.error("❌ SKU не найдены! Проверьте формат введенных данных.")
            else:
                st.info("👆 Нажмите 'Извлечь SKU' для получения результатов")

    # Разделитель
    st.markdown("---")
    
    # Информация о работе приложения
    with st.expander("📊 Детальная информация"):
        st.markdown("""
        **Как работает извлечение:**
        
        1. **Из ссылок OZON**: ищет паттерн `-1650868905/` в URL
        2. **Из текста**: находит числа 9-10 цифр, не начинающиеся с 0
        
        **Обработка данных:**
        - Автоматическое удаление дубликатов
        - Сортировка SKU по возрастанию
        - Валидация формата чисел
        """)

if __name__ == "__main__":
    main()