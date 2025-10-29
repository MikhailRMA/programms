import re
import streamlit as st
from datetime import datetime
import base64

# Настройка страницы
st.set_page_config(
    page_title="OZON SKU Extractor",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Полностью адаптивный CSS
st.markdown("""
<style>
    /* CSS переменные для адаптации */
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #4ECDC4;
        --background-color: #FFFFFF;
        --secondary-background-color: #F8F9FA;
        --text-color: #333333;
        --text-muted: #666666;
        --border-color: #E0E0E0;
        --shadow-color: rgba(0,0,0,0.1);
        --code-background: #F1F3F4;
        --code-color: #D32F2F;
        --success-color: #56ab2f;
        --error-color: #ff6b6b;
        --card-padding: 1.2rem;
        --font-size-base: 1rem;
        --font-size-sm: 0.9rem;
        --font-size-lg: 1.1rem;
        --border-radius: 12px;
    }
    
    /* Темная тема */
    @media (prefers-color-scheme: dark) {
        :root {
            --primary-color: #4ECDC4;
            --secondary-color: #FF6B6B;
            --background-color: #1E1E1E;
            --secondary-background-color: #2D2D2D;
            --text-color: #FFFFFF;
            --text-muted: #6b6b6b;
            --border-color: #404040;
            --shadow-color: rgba(0,0,0,0.3);
            --code-background: #2D2D2D;
            --code-color: #4ECDC4;
            --success-color: #a8e063;
            --error-color: #ff8e8e;
        }
    }
    
    /* Адаптация для планшетов */
    @media (max-width: 1024px) {
        :root {
            --card-padding: 1rem;
            --font-size-base: 0.95rem;
        }
    }
    
    /* Адаптация для мобильных устройств */
    @media (max-width: 768px) {
        :root {
            --card-padding: 0.9rem;
            --font-size-base: 0.9rem;
            --font-size-sm: 0.85rem;
            --border-radius: 10px;
        }
    }
    
    /* Адаптация для очень маленьких экранов */
    @media (max-width: 480px) {
        :root {
            --card-padding: 0.8rem;
            --font-size-base: 0.85rem;
            --font-size-sm: 0.8rem;
            --border-radius: 8px;
        }
    }
    
    /* Для очень больших экранов (32+ дюймов) */
    @media (min-width: 1920px) {
        :root {
            --card-padding: 1.5rem;
            --font-size-base: 1.1rem;
            --font-size-lg: 1.3rem;
        }
    }
    
    /* Базовые стили */
    .main-header {
        font-size: clamp(1.8rem, 5vw, 2.5rem);
        color: var(--primary-color);
        text-align: center;
        margin-bottom: clamp(0.5rem, 2vw, 1rem);
        font-weight: 800;
        line-height: 1.2;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-subtitle {
        text-align: center;
        color: var(--text-muted);
        margin-bottom: clamp(1rem, 3vw, 2rem);
        font-size: var(--font-size-base);
        line-height: 1.4;
    }
    
    /* Заголовки разделов основной области */
    .section-header {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: var(--primary-color);
        padding: clamp(0.8rem, 2vw, 1rem) clamp(1rem, 2.5vw, 1.5rem);
        border-radius: var(--border-radius);
        margin: clamp(0.8rem, 2vw, 1rem) 0 clamp(0.4rem, 1vw, 0.5rem) 0;
        font-size: clamp(1.1rem, 3vw, 1.3rem);
        font-weight: 600;
        text-align: center;
        box-shadow: 0 2px 8px var(--shadow-color);
    }

    
    
    /* Карточки */
    .card {
        background: var(--background-color);
        padding: var(--card-padding);
        border-radius: var(--border-radius);
        box-shadow: 0 2px 12px var(--shadow-color);
        border: 1px solid var(--border-color);
        margin: clamp(0.5rem, 1.5vw, 0.8rem) 0;
        color: var(--text-color);
        font-size: var(--font-size-base);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 4px 20px var(--shadow-color);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.8rem;
        gap: 0.5rem;
    }
    
    .card-icon {
        font-size: 1.3em;
    }
    
    .card-title {
        margin: 0;
        color: var(--primary-color);
        font-size: var(--font-size-base);
        font-weight: 600;
    }
    
    /* Status Item */
    .status-item {
        background: var(--secondary-background-color);
        padding: clamp(0.6rem, 1.5vw, 0.8rem);
        border-radius: 8px;
        margin: clamp(0.3rem, 1vw, 0.5rem) 0;
        border-left: 4px solid var(--primary-color);
        color: var(--text-color);
        font-size: var(--font-size-sm);
        line-height: 1.4;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .status-item strong {
        color: var(--primary-color);
    }
    
    .status-item code {
        background: var(--code-background);
        color: var(--code-color);
        padding: 0.1rem 0.3rem;
        border-radius: 4px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 0.85em;
        word-break: break-word;
    }
    
    /* Кнопки */
    .stButton button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: clamp(0.5rem, 1.5vw, 0.6rem) clamp(1rem, 2.5vw, 1.2rem);
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        font-size: var(--font-size-base);
        min-height: 44px;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Текстовые поля */
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid var(--border-color);
        padding: clamp(0.6rem, 1.5vw, 0.8rem);
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: var(--font-size-sm);
        background: var(--background-color);
        color: var(--text-color);
        min-height: 150px;
        resize: vertical;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(46, 134, 171, 0.1);
    }
    
    /* Уведомления */
    .alert {
        padding: clamp(0.6rem, 1.5vw, 0.8rem);
        border-radius: 8px;
        margin: clamp(0.5rem, 1.5vw, 0.8rem) 0;
        font-size: var(--font-size-base);
        line-height: 1.4;
    }
    
    .alert-success {
        background: linear-gradient(45deg, var(--success-color), #a8e063);
        color: white;
    }
    
    .alert-info {
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        color: white;
    }
    
    .alert-warning {
        background: linear-gradient(45deg, #f7971e, #ffd200);
        color: white;
    }
    
    .alert-error {
        background: linear-gradient(45deg, var(--error-color), #ff8e8e);
        color: white;
    }
    
    /* Ссылки для скачивания */
    .download-link {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(45deg, var(--success-color), #a8e063);
        color: white;
        padding: clamp(8px, 2vw, 10px) clamp(16px, 3vw, 20px);
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        margin: 8px 0;
        font-size: var(--font-size-base);
        min-height: 44px;
        gap: 0.5rem;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .download-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(86, 171, 47, 0.4);
    }
    
    /* Сайдбар */
    .sidebar-header {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: clamp(1rem, 2.5vw, 1.5rem);
        border-radius: var(--border-radius);
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .sidebar-title {
        color: white;
        margin: 0;
        font-size: var(--font-size-lg);
        font-weight: 600;
    }
    
    /* Анимации */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.4s ease-out;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Утилиты */
    .text-center { text-align: center; }
    .text-success { color: var(--success-color); }
    .text-error { color: var(--error-color); }
    .mb-1 { margin-bottom: 0.5rem; }
    .mb-2 { margin-bottom: 1rem; }
    
    /* Специальные стили для очень маленьких экранов */
    @media (max-width: 360px) {
        .card-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def extract_sku_from_text(text):
    """Извлекает SKU из текста"""
    try:
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
            if sku.isdigit() and sku not in seen_sku:
                unique_sku.append(sku)
                seen_sku.add(sku)
        
        # Сортируем для удобства
        unique_sku.sort()
        return unique_sku
        
    except Exception as e:
        raise Exception(f"Ошибка при извлечении SKU: {str(e)}")

def create_csv_content(sku_list):
    """Создает содержимое CSV файла"""
    csv_content = "SKU\n"
    for sku in sku_list:
        csv_content += f"{sku}\n"
    return csv_content

def get_csv_download_link(sku_list, filename):
    """Генерирует ссылку для скачивания CSV файла"""
    csv_content = create_csv_content(sku_list)
    b64 = base64.b64encode(csv_content.encode()).decode()
    
    href = f'''
    <div class="card fade-in">
        <div class="card-header">
            <span class="card-icon">📊</span>
            <h4 class="card-title">Результаты готовы!</h4>
        </div>
        <div class="status-item text-success">
            ✅ Успешно извлечено SKU: <strong>{len(sku_list)}</strong>
        </div>
        <a class="download-link pulse" href="data:file/csv;base64,{b64}" download="{filename}">
            📥 Скачать CSV файл
        </a>
    </div>
    '''
    return href

def main():
    # Кастомный заголовок
    st.markdown('<h1 class="main-header">🛍️ SKU Extractor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Извлекайте SKU из ссылок OZON и любого текста</p>', unsafe_allow_html=True)
    
    # Сайдбар с карточками
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header fade-in">
            <h3 class="sidebar-title">ℹ️ Информация</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Карточка "Формат SKU"
        st.markdown("""
        <div class="card fade-in">
            <div class="card-header">
                <span class="card-icon">📝</span>
                <h4 class="card-title">Формат SKU</h4>
            </div>
            <div class="status-item">
                <strong>Из ссылок OZON:</strong><br>
                <code>...-1650868905/...</code>
            </div>
            <div class="status-item">
                <strong>Из текста:</strong><br>
                9-10 цифр, не начинается с 0
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Карточка "Примеры SKU"
        st.markdown("""
        <div class="card fade-in">
            <div class="card-header">
                <span class="card-icon">💡</span>
                <h4 class="card-title">Примеры SKU</h4>
            </div>
            <div class="status-item text-success">
                <strong>✅ Валидные:</strong><br>
                <code>1650868905</code><br>
                <code>123456789</code><br>
                <code>9876543210</code>
            </div>
            <div class="status-item text-error">
                <strong>❌ Невалидные:</strong><br>
                <code>012345678</code> (0 в начале)<br>
                <code>12345678</code> (мало цифр)<br>
                <code>12345678901</code> (много цифр)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Карточка "Быстрые клавиши"
        st.markdown("""
        <div class="card fade-in">
            <div class="card-header">
                <span class="card-icon">🚀</span>
                <h4 class="card-title">Быстрые клавиши</h4>
            </div>
            <div class="status-item">
                <strong>Ctrl+A</strong> - Выделить все
            </div>
            <div class="status-item">
                <strong>Ctrl+C</strong> - Копировать
            </div>
            <div class="status-item">
                <strong>Ctrl+V</strong> - Вставить
            </div>
            <div class="status-item">
                <strong>Ctrl+Z</strong> - Отменить
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div class="text-center" style="color: var(--text-muted); padding: 1rem;">
            <p>With ❤️ by <strong>mroshchupkin and DS</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Адаптивная основная область
    # На мобильных - одна колонка, на десктопе - две
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.markdown('<div class="section-header">📥 Ввод данных</div>', unsafe_allow_html=True)
    
            
    
        default_text = """https://www.ozon.ru/product/salfetki-ot-pyaten-na-odezhde-vlazhnye-pyatnovyvodyashchie-sredstvo-ochishchayushchie-1650868905/
https://www.ozon.ru/product/noutbuk-apple-macbook-air-13-m1-8gb-256gb-space-gray-1234567890/
https://www.ozon.ru/product/telefon-samsung-galaxy-s21-987654321/

Товары: 9876543210, 555666777, 8889990001."""
    
        input_text = st.text_area(
            "",  # Пустой заголовок, т.к. он уже в карточке
            value=default_text,
            height=280,
            placeholder="Вставьте ваш текст здесь...",
            label_visibility="collapsed"
     )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Адаптивные кнопки
        button_col1, button_col2, button_col3 = st.columns(3)
        
        with button_col1:
            extract_btn = st.button("🔍 Извлечь SKU", type="primary", use_container_width=True)
        with button_col2:
            clear_btn = st.button("🗑️ Очистить", use_container_width=True)
        with button_col3:
            example_btn = st.button("📋 Пример", use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">📤 Результаты</div>', unsafe_allow_html=True)
        
        # Инициализация session state
        if 'sku_list' not in st.session_state:
            st.session_state.sku_list = []
        if 'extraction_stats' not in st.session_state:
            st.session_state.extraction_stats = {"found": 0, "duplicates": 0}
        
        # Обработка кнопок
        if clear_btn:
            st.session_state.sku_list = []
            st.session_state.extraction_stats = {"found": 0, "duplicates": 0}
            st.rerun()
            
        if example_btn:
            st.rerun()
        
        # Обработка извлечения SKU
        if extract_btn:
            if not input_text.strip():
                st.markdown("""
                <div class="alert alert-warning">
                    <strong>⚠️ Внимание</strong><br>
                    Введите текст для извлечения SKU
                </div>
                """, unsafe_allow_html=True)
            else:
                with st.spinner("🔍 Извлекаем SKU..."):
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
                        st.markdown(f"""
                        <div class="alert alert-error">
                            <strong>❌ Ошибка</strong><br>
                            {str(e)}
                        </div>
                        """, unsafe_allow_html=True)
        
       # Отображение результатов
        if st.session_state.sku_list:
            stats = st.session_state.extraction_stats
    
            # Статистика
            duplicate_info = f'<div class="status-item">♻️ Удалено дубликатов: <strong>{stats["duplicates"]}</strong></div>' if stats['duplicates'] > 0 else ''
    
            st.markdown(f"""
            <div class="alert alert-success fade-in">
                <strong>✅ Успешно извлечено!</strong><br>
                <div class="status-item" style="background: transparent; border: none; padding: 0.5rem 0;">
                    Найдено SKU: <strong>{stats['found']}</strong>
                </div>
                {duplicate_info}
             </div>
            """, unsafe_allow_html=True)
    
            # Карточка с результатами - ВАРИАНТ 3 (рекомендуемый)
            st.markdown("""
            <div class="card fade-in">
                <div class="card-header">
                    <span class="card-icon">📋</span>
                    <h4 class="card-title">Найденные SKU</h4>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
            result_text = "\n".join(st.session_state.sku_list)
            st.text_area("**Список извлеченных SKU:**", value=result_text, height=200, key="results", label_visibility="collapsed")
    
            # Скачивание
            if st.session_state.sku_list:
                timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
                filename = f"sku_{timestamp}.csv"
                st.markdown(get_csv_download_link(st.session_state.sku_list, filename), unsafe_allow_html=True)

    # Дополнительная информация
    with st.expander("📊 Подробнее о работе приложения", expanded=False):
        st.markdown("#### 🔧 Как работает извлечение")
    
        st.markdown("""
        <div class="status-item">
            <strong>📎 Из ссылок OZON:</strong> ищет паттерн <code>-1650868905/</code> в URL
        </div>
        <div class="status-item">
            <strong>📝 Из текста:</strong> находит числа 9-10 цифр, не начинающиеся с 0
        </div>
        """, unsafe_allow_html=True)
    
        st.markdown("#### 🔄 Обработка данных")
    
        st.markdown("""
        <div class="status-item">✅ <strong>Автоматическое удаление дубликатов</strong> - убирает повторяющиеся SKU</div>
        <div class="status-item">📊 <strong>Сортировка по возрастанию</strong> - упорядочивает SKU для удобства</div>
        <div class="status-item">🔍 <strong>Валидация формата</strong> - проверяет что SKU соответствуют требованиям</div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()