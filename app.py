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

# Кастомный CSS
# Кастомный CSS с адаптацией под тему
st.markdown("""
<style>
    /* Основные стили */
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
    }
    
    .subheader {
        font-size: 1.3rem;
        color: var(--primary-color);
        border-left: 4px solid var(--primary-color);
        padding-left: 1rem;
        margin: 1rem 0 0.5rem 0;
    }
    
    /* Карточки - адаптивные */
    .card {
        background: var(--background-color);
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px var(--shadow-color);
        border: 1px solid var(--border-color);
        margin: 0.8rem 0;
        color: var(--text-color);
    }
    
    /* Кнопки */
    .stButton button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Текстовые поля */
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid var(--border-color);
        padding: 0.8rem;
        font-family: 'Consolas', monospace;
        font-size: 0.9rem;
        background: var(--background-color);
        color: var(--text-color);
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Status Item - АДАПТИВНЫЙ */
    .status-item {
        background: var(--secondary-background-color);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid var(--primary-color);
        color: var(--text-color);
        font-size: 0.95rem;
    }
    
    .status-item strong {
        color: var(--primary-color);
    }
    
    .status-item code {
        background: var(--code-background);
        color: var(--code-color);
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Consolas', monospace;
        font-size: 0.85rem;
    }
    
    /* Уведомления */
    .success-box {
        background: linear-gradient(45deg, #56ab2f, #a8e063);
        color: white;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.8rem 0;
    }
    
    .info-box {
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        color: white;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.8rem 0;
    }
    
    .warning-box {
        background: linear-gradient(45deg, #f7971e, #ffd200);
        color: white;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.8rem 0;
    }
    
    /* Ссылки для скачивания */
    .download-link {
        display: inline-block;
        background: linear-gradient(45deg, #56ab2f, #a8e063);
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 6px;
        font-weight: bold;
        margin: 8px 0;
        text-align: center;
    }
    
    /* Сайдбар */
    .sidebar-header {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    /* Анимации */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.3s ease-in;
    }
</style>

<script>
// JavaScript для определения темы и применения CSS переменных
function updateTheme() {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (isDark) {
        // Темная тема
        document.documentElement.style.setProperty('--primary-color', '#4ECDC4');
        document.documentElement.style.setProperty('--background-color', '#1E1E1E');
        document.documentElement.style.setProperty('--secondary-background-color', '#2D2D2D');
        document.documentElement.style.setProperty('--text-color', '#FFFFFF');
        document.documentElement.style.setProperty('--border-color', '#404040');
        document.documentElement.style.setProperty('--shadow-color', 'rgba(0,0,0,0.3)');
        document.documentElement.style.setProperty('--code-background', '#2D2D2D');
        document.documentElement.style.setProperty('--code-color', '#4ECDC4');
    } else {
        // Светлая тема
        document.documentElement.style.setProperty('--primary-color', '#2E86AB');
        document.documentElement.style.setProperty('--background-color', '#FFFFFF');
        document.documentElement.style.setProperty('--secondary-background-color', '#F8F9FA');
        document.documentElement.style.setProperty('--text-color', '#333333');
        document.documentElement.style.setProperty('--border-color', '#E0E0E0');
        document.documentElement.style.setProperty('--shadow-color', 'rgba(0,0,0,0.1)');
        document.documentElement.style.setProperty('--code-background', '#F1F3F4');
        document.documentElement.style.setProperty('--code-color', '#D32F2F');
    }
}

// Применяем тему при загрузке и при изменении
updateTheme();
window.matchMedia('(prefers-color-scheme: dark)').addListener(updateTheme);
</script>
""", unsafe_allow_html=True)

def extract_sku_from_text(text):
    """
    Извлекает SKU из текста. SKU должны быть 9 или 10 цифр, не начинаться с 0
    """
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
            # Проверяем, что SKU состоит только из цифр и не был добавлен ранее
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
    csv_content = "SKU\n"  # Заголовок
    for sku in sku_list:
        csv_content += f"{sku}\n"
    return csv_content

def get_csv_download_link(sku_list, filename):
    """Генерирует ссылку для скачивания CSV файла"""
    csv_content = create_csv_content(sku_list)
    b64 = base64.b64encode(csv_content.encode()).decode()
    
    href = f'''
    <div class="card fade-in">
        <h4>📊 Результаты готовы!</h4>
        <div style="margin: 0.5rem 0;">
            <div class="status-item">✅ Найдено SKU: <strong>{len(sku_list)}</strong></div>
        </div>
        <a class="download-link" href="data:file/csv;base64,{b64}" download="{filename}">
            📥 Скачать CSV файл
        </a>
    </div>
    '''
    return href

def main():
    # Кастомный заголовок
    st.markdown('<h1 class="main-header">🛍️ OZON SKU Extractor</h1>', unsafe_allow_html=True)
    
    # Краткое описание
    st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">Извлекайте SKU из ссылок OZON и любого текста</p>', unsafe_allow_html=True)
    
    # Сайдбар с улучшенным дизайном
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h3 style="color: white; margin: 0;">ℹ️ Информация</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h4>📝 Формат SKU</h4>
            <div class="status-item">
                <strong>Из ссылок:</strong><br>
                <code>...-1650868905/...</code>
            </div>
            <div class="status-item">
                <strong>Из текста:</strong><br>
                9-10 цифр, не начинается с 0
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h4>💡 Примеры SKU</h4>
            <div style="font-family: monospace; font-size: 0.8rem;">
                ✅ 1650868905<br>
                ✅ 123456789<br>
                ✅ 9876543210<br>
                ❌ 012345678<br>
                ❌ 12345678<br>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h4>🚀 Быстрые клавиши</h4>
            <div class="status-item">
                <strong>Ctrl+A</strong> - Выделить все
            </div>
            <div class="status-item">
                <strong>Ctrl+C</strong> - Копировать
            </div>
            <div class="status-item">
                <strong>Ctrl+V</strong> - Вставить
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
            <p>With ❤️ by <strong>mroshchupkin and DS</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Основная область в колонках
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="subheader">📥 Ввод данных</div>', unsafe_allow_html=True)
        
        # Карточка для ввода данных
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        
        default_text = """https://www.ozon.ru/product/salfetki-ot-pyaten-na-odezhde-vlazhnye-pyatnovyvodyashchie-sredstvo-ochishchayushchie-1650868905/
https://www.ozon.ru/product/noutbuk-apple-macbook-air-13-m1-8gb-256gb-space-gray-1234567890/
https://www.ozon.ru/product/telefon-samsung-galaxy-s21-987654321/

Заказ 123456789, товары: 9876543210, 555666777."""
        
        input_text = st.text_area(
            "**Вставьте текст со ссылками OZON или любой текст:**",
            value=default_text,
            height=250,
            placeholder="Вставьте ваш текст здесь...",
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Кнопки действий
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            extract_btn = st.button("🔍 Извлечь SKU", type="primary", use_container_width=True)
        with col_btn2:
            clear_btn = st.button("🗑️ Очистить", use_container_width=True)
        with col_btn3:
            example_btn = st.button("📋 Пример", use_container_width=True)
    
    with col2:
        st.markdown('<div class="subheader">📤 Результаты</div>', unsafe_allow_html=True)
        
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
                <div class="warning-box">
                    <h4>⚠️ Внимание</h4>
                    <p>Введите текст для извлечения SKU</p>
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
                        st.error(f"❌ Ошибка при извлечении SKU: {str(e)}")
        
        # Отображение результатов
        if st.session_state.sku_list:
            stats = st.session_state.extraction_stats
            
            # Статистика
            st.markdown(f"""
            <div class="success-box fade-in">
                <h4>✅ Успешно извлечено!</h4>
                <div class="status-item">Найдено SKU: <strong>{stats['found']}</strong></div>
                {f'<div class="status-item">Удалено дубликатов: <strong>{stats["duplicates"]}</strong></div>' if stats['duplicates'] > 0 else ''}
            </div>
            """, unsafe_allow_html=True)
            
            # Карточка с результатами
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            result_text = "\n".join(st.session_state.sku_list)
            st.text_area("**Найденные SKU:**", value=result_text, height=180, key="results")
            st.markdown('</div>')
            
            # Скачивание
            if st.session_state.sku_list:
                timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
                filename = f"sku_{timestamp}.csv"
                st.markdown(get_csv_download_link(st.session_state.sku_list, filename), unsafe_allow_html=True)
        
        else:
            if not extract_btn:
                st.markdown("""
                <div class="info-box">
                    <h4>👆 Готов к работе</h4>
                    <p>Введите текст и нажмите "Извлечь SKU"</p>
                </div>
                """, unsafe_allow_html=True)

    # Дополнительная информация
    with st.expander("📊 Подробнее о работе приложения"):
        st.markdown("""
        <div class="card">
            <h4>🔧 Как работает извлечение</h4>
            <div class="status-item">
                <strong>Из ссылок OZON:</strong> ищет паттерн <code>-1650868905/</code> в URL
            </div>
            <div class="status-item">
                <strong>Из текста:</strong> находит числа 9-10 цифр, не начинающиеся с 0
            </div>
            
            <h4>🔄 Обработка данных</h4>
            <div class="status-item">Автоматическое удаление дубликатов</div>
            <div class="status-item">Сортировка SKU по возрастанию</div>
            <div class="status-item">Валидация формата чисел</div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
