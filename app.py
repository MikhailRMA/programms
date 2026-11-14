import re
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import base64
from urllib.parse import urlparse

# Настройка страницы
st.set_page_config(
    page_title="OZON SKU Extractor",
    page_icon="https://cdn1.ozone.ru/s3/common-image-storage/bx/box-open-ozon-alt_m.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS в стиле OZON
st.markdown("""
<style>
    :root {
        --ozon-primary: #005BFF;
        --ozon-primary-dark: #004ACC;
        --ozon-secondary: #FF6B00;
        --ozon-background: #1A1A1A;
        --ozon-surface: #2D2D2D;
        --ozon-text: #FFFFFF;
        --ozon-text-muted: #B3B3B3;
        --ozon-border: #404040;
        --ozon-shadow: rgba(0, 91, 255, 0.2);
        --ozon-success: #00A650;
        --ozon-warning: #FFB800;
        --ozon-error: #FF3B30;
        --ozon-card-padding: 1.2rem;
        --ozon-font-size-base: 1rem;
        --ozon-font-size-sm: 0.9rem;
        --ozon-border-radius: 8px;
    }

    .main, .stApp {
        background-color: var(--ozon-background) !important;
    }
    
    .stTextInput, .stTextArea, .stNumberInput, .stSelectbox {
        color: var(--ozon-text) !important;
    }
    
    .stTextInput label, .stTextArea label, .stNumberInput label, .stSelectbox label {
        color: var(--ozon-text) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--ozon-text) !important;
    }
    
    .main .block-container {
        background-color: var(--ozon-background) !important;
        color: var(--ozon-text) !important;
    }
    
    .main-header {
        font-size: clamp(1.8rem, 5vw, 2.5rem);
        background: linear-gradient(135deg, var(--ozon-primary), var(--ozon-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: var(--ozon-primary);
        text-align: center;
        margin-bottom: clamp(0.5rem, 2vw, 1rem);
        font-weight: 800;
        line-height: 1.2;
    }
    
    .main-subtitle {
        text-align: center;
        color: var(--ozon-text-muted);
        margin-bottom: clamp(1rem, 3vw, 2rem);
        font-size: var(--ozon-font-size-base);
        line-height: 1.4;
    }
    
    .section-header {
        background: url('https://brandlab.ozon.ru/images/tild6365-6165-4064-b161-626431393363__pattern_bg-1.png');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white;
        padding: clamp(1rem, 2.5vw, 1.5rem);
        border-radius: var(--ozon-border-radius);
        margin-bottom: 1rem;
        text-align: center;
        position: relative;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: clamp(1.5rem, 1.5vw, 5rem) !important;
        font-weight: 900 !important;
    }
    
    .ozon-card {
        background: var(--ozon-surface);
        padding: var(--ozon-card-padding);
        border-radius: var(--ozon-border-radius);
        box-shadow: 0 2px 12px var(--ozon-shadow);
        border: 1px solid var(--ozon-border);
        margin: clamp(0.5rem, 1.5vw, 0.8rem) 0;
        color: var(--ozon-text);
        font-size: var(--ozon-font-size-base);
        transition: all 0.3s ease;
    }
    
    .ozon-card:hover {
        box-shadow: 0 4px 20px var(--ozon-shadow);
        transform: translateY(-2px);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.8rem;
        gap: 0.5rem;
    }
    
    .card-icon {
        font-size: 1.3em;
        color: var(--ozon-primary);
    }
    
    .card-title {
        margin: 0;
        color: var(--ozon-primary);
        font-size: var(--ozon-font-size-base);
        font-weight: 600;
    }
    
    .ozon-status {
        background: var(--ozon-surface);
        padding: clamp(0.6rem, 1.5vw, 0.8rem);
        border-radius: 6px;
        margin: clamp(0.3rem, 1vw, 0.5rem) 0;
        border-left: 4px solid var(--ozon-primary);
        color: var(--ozon-text);
        font-size: var(--ozon-font-size-sm);
        line-height: 1.4;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .ozon-status strong {
        color: var(--ozon-primary);
    }
    
    .ozon-status code {
        background: var(--ozon-surface);
        color: var(--ozon-primary);
        padding: 0.1rem 0.3rem;
        border-radius: 4px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 0.85em;
        word-break: break-word;
        border: 1px solid var(--ozon-border);
    }
    
    .stButton button {
        background: linear-gradient(135deg, var(--ozon-primary), var(--ozon-primary-dark));
        color: white;
        border: none;
        padding: clamp(0.5rem, 1.5vw, 0.6rem) clamp(1rem, 2.5vw, 1.2rem);
        border-radius: var(--ozon-border-radius);
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        font-size: var(--ozon-font-size-base);
        min-height: 44px;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, var(--ozon-primary-dark), var(--ozon-primary));
        transform: translateY(-2px);
        box-shadow: 0 6px 20px var(--ozon-shadow);
    }
    
    .stTextArea textarea {
        border-radius: var(--ozon-border-radius);
        border: 2px solid var(--ozon-border);
        padding: clamp(0.6rem, 1.5vw, 0.8rem);
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: var(--ozon-font-size-sm);
        background: var(--ozon-surface);
        color: var(--ozon-text);
        min-height: 150px;
        resize: vertical;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--ozon-primary);
        box-shadow: 0 0 0 3px rgba(0, 91, 255, 0.1);
    }
    
    .ozon-alert {
        padding: clamp(0.6rem, 1.5vw, 0.8rem);
        border-radius: var(--ozon-border-radius);
        margin: clamp(0.5rem, 1.5vw, 0.8rem) 0;
        font-size: var(--ozon-font-size-base);
        line-height: 1.4;
        border-left: 4px solid;
    }
    
    .ozon-alert-success {
        background: var(--ozon-surface) !important;
        border-left: 4px solid var(--ozon-primary) !important;
        color: #FFFFFF !important;
        padding: clamp(0.6rem, 1.5vw, 0.8rem);
        border-radius: var(--ozon-border-radius);
        margin: clamp(0.5rem, 1.5vw, 0.8rem) 0;
        font-size: var(--ozon-font-size-base);
        line-height: 1.4;
    }

    .ozon-alert-success strong {
        color: #FFFFFF !important;
    }
    
    .ozon-alert-info {
        background: var(--ozon-surface);
        border-left-color: var(--ozon-primary);
        color: var(--ozon-text);
    }
    
    .ozon-alert-warning {
        background: var(--ozon-surface);
        border-left-color: var(--ozon-warning);
        color: var(--ozon-text);
    }
    
    .ozon-alert-error {
        background: var(--ozon-surface);
        border-left-color: var(--ozon-error);
        color: var(--ozon-text);
    }
    
    .ozon-download {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: #f91155 !important;
        color: white !important;
        padding: clamp(8px, 2vw, 10px) clamp(16px, 3vw, 20px);
        text-decoration: none;
        border-radius: var(--ozon-border-radius);
        font-weight: 600;
        margin: 8px 0;
        font-size: var(--ozon-font-size-base);
        min-height: 44px;
        gap: 0.5rem;
        transition: all 0.3s ease;
        text-align: center;
        border: none;
        width: 100%;
    }
            
    .ozon-download:hover {
        background: #e0104a !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(249, 17, 85, 0.4);
        color: white;
    }
    
    .ozon-sidebar-header {
        background:  url('https://brandlab.ozon.ru/images/tild6365-6165-4064-b161-626431393363__pattern_bg-1.png');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white;
        padding: clamp(1rem, 2.5vw, 1.5rem);
        border-radius: var(--ozon-border-radius);
        margin-bottom: 1rem;
        text-align: center;
        position: relative;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .sidebar-title {
        color: white;
        margin: 0;
        font-size: clamp(1.5rem, 2vw, 2.5rem) !important;
        font-weight: 900;
    }
    
    @keyframes ozonFadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .ozon-fade-in {
        animation: ozonFadeIn 0.4s ease-out;
    }
    
    @keyframes ozonPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .ozon-pulse {
        animation: ozonPulse 2s infinite;
    }
    
    .text-center { text-align: center; }
    .text-success { color: var(--ozon-success); }
    .text-warning { color: var(--ozon-warning); }
    .text-error { color: var(--ozon-error); }
    .text-primary { color: var(--ozon-primary); }
    .mb-1 { margin-bottom: 0.5rem; }
    .mb-2 { margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

def extract_sku_from_text(text: str):
    """
    Надежное извлечение SKU:
    1. Захватывает ссылку целиком до последнего SKU в пути (жадный поиск до конца слага),
       игнорируя родительские ID склеек.
    2. Отрезает только стандартные параметры ссылки (включая 10-значный sh=...), не трогая прилипшие сзади артикулы.
    3. Вырезает саму ссылку и извлекает все оставшиеся артикулы из обычного текста.
    """
    try:
        extracted_skus = []
        
        # Жадный [a-zA-Z0-9_-]* доходит до ПОСЛЕДНЕГО дефиса перед финальным 9-10-значным SKU.
        # Граница после SKU: слэш, знак вопроса или любой символ, не являющийся частью слага (буквой/цифрой/дефисом).
        product_url_pattern = (
            r'https?://(?:www\.)?ozon\.ru/product/'
            r'(?:[a-zA-Z0-9_-]*-)?([1-9]\d{8,9})'
            r'(?:(?=/|\?|[^a-zA-Z0-9_-]|$))/?'
            r'(?:\?(?:sh=[a-zA-Z0-9_-]{10}|[^\s"\'<>0-9]*))?'
        )
        
        clean_text = text
        
        for match in re.finditer(product_url_pattern, text, flags=re.IGNORECASE):
            full_url = match.group(0)
            target_sku = match.group(1)
            
            extracted_skus.append(target_sku)
            # Вырезаем найденную ссылку целиком (включая родительский ID внутри неё)
            clean_text = clean_text.replace(full_url, ' ', 1)
            
        # Вырезаем служебные ссылки (/seller/, /brand/, /category/)
        other_ozon_urls = r'https?://(?:www\.)?ozon\.ru/(?:seller|brand|category|highlight)/[a-zA-Z0-9_/-]+(?:\?[^\s"\'<>]*)?'
        clean_text = re.sub(other_ozon_urls, ' ', clean_text, flags=re.IGNORECASE)
        
        # Извлекаем все валидные SKU из оставшегося обычного текста
        pattern_text = r'(?<!\d)([1-9]\d{8,9})(?!\d)'
        text_skus = re.findall(pattern_text, clean_text)
        extracted_skus.extend(text_skus)
        
        raw_count = len(extracted_skus)
        unique_sku = sorted(list(set(extracted_skus)))
        
        return unique_sku, raw_count
        
    except Exception as e:
        raise Exception(f"Ошибка при извлечении SKU: {str(e)}")

def create_csv_content(sku_list):
    """Создает содержимое CSV файла"""
    csv_content = ""
    for sku in sku_list:
        csv_content += f"{sku}\n"
    return csv_content

def get_csv_download_link(sku_list, filename):
    """Генерирует ссылку для скачивания CSV файла"""
    csv_content = create_csv_content(sku_list)
    b64 = base64.b64encode(csv_content.encode()).decode()
    
    href = f'''
    <div class="ozon-card ozon-fade-in">
        <div class="card-header">
            <span class="card-icon">📊</span>
            <h4 class="card-title">Результаты готовы!</h4>
        </div>
        <div class="ozon-status">
    ✅ Успешно извлечено SKU: <strong>{len(sku_list)}</strong>
        </div>
        <a class="ozon-download ozon-pulse" href="data:file/csv;base64,{b64}" download="{filename}" 
           onclick="if(typeof ym!=='undefined')ym(104969939,'reachGoal','download_clicked')">
            📥 Скачать CSV файл
        </a>
    </div>
    '''
    return href

def main():
    # Яндекс.Метрика
    metrika_code = """
    <script>
        (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
        m[i].l=1*new Date();
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
        (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
    
        ym(104969939, "init", {
            clickmap:true,
            trackLinks:true,
            accurateTrackBounce:true,
            webvisor:true
        });
        ym(104969939,'reachGoal','extraction_started')
        ym(104969939,'reachGoal','extraction_success')
        ym(104969939,'reachGoal','download_clicked')
    </script>
    <noscript><div><img src="https://mc.yandex.ru/watch/104969939" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
    """
    
    st.markdown(metrika_code, unsafe_allow_html=True)

    # Заголовок
    st.markdown('<div style="display: flex; align-items: center; justify-content: center; gap: 12px;"><img src="https://cdn1.ozone.ru/s3/common-image-storage/bx/box-open-ozon-alt_m.png" alt="Коробка Ozon" style="height: 80px; width: 80px; object-fit: contain;"><h1 style="color: #005BFF; font-size: 2.5rem; text-align: center; font-weight: 800; margin: 0; line-height: 1;">OZON SKU Extractor</h1></div>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Извлекайте SKU из ссылок OZON и любого текста </p>', unsafe_allow_html=True)
    
    # Сайдбар
    with st.sidebar:
        st.markdown("""
        <div class="ozon-sidebar-header ozon-fade-in">
            <h3 class="sidebar-title" > Информация</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="ozon-card ozon-fade-in">
            <div class="card-header">
                <span class="card-icon">📝</span>
                <h4 class="card-title">Формат SKU</h4>
            </div>
            <div class="ozon-status">
                <strong>Из ссылок OZON:</strong><br>
                Строго 1 артикул карточки (последнее число после дефиса, включая склейки и URL без слэша)
            </div>
            <div class="ozon-status">
                <strong>Из текста:</strong><br>
                Все числа длиной 9-10 цифр, не начинающиеся с 0
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="ozon-card ozon-fade-in">
            <div class="card-header">
                <span class="card-icon">💡</span>
                <h4 class="card-title">Примеры SKU</h4>
            </div>
            <div class="ozon-status text-success">
                <strong>✅ Валидные:</strong><br>
                <code>...-4091214783-6179307890/</code> → <code>6179307890</code><br>
                <code>...-987654321</code> (без слэша)<br>
                <code>1650868905</code><br>
                <code>9876543210</code>
            </div>
            <div class="ozon-status text-error">
                <strong>❌ Невалидные:</strong><br>
                <code>012345678</code> (0 в начале)<br>
                <code>12345678</code> (мало цифр)<br>
                <code>12345678901</code> (много цифр)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div class="text-center" style="color: var(--ozon-text-muted); padding: 1rem;">
            <p>With ❤️ by <strong>mroshchupkin and DS</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Основная область
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.markdown('<div class="section-header">📥 Ввод данных</div>', unsafe_allow_html=True)
    
        default_text = """https://www.ozon.ru/product/salfetki-ot-pyaten-na-odezhde-vlazhnye-pyatnovyvodyashchie-sredstvo-ochishchayushchie-1650868905/
https://ozon.ru/product/yuedongze-elektricheskiy-chaynik-4091214783-6179307890/
https://www.ozon.ru/product/telefon-samsung-galaxy-s21-987654321

Товары: 9876543210, 555666777, 8889990001."""
    
        input_text = st.text_area(
            "",
            value=default_text,
            height=280,
            placeholder="Вставьте ваш текст здесь...",
            label_visibility="collapsed"
        )
        
        extract_btn = st.button("🔍 Извлечь SKU", type="primary", use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">📤 Результаты</div>', unsafe_allow_html=True)
        
        if 'sku_list' not in st.session_state:
            st.session_state.sku_list = []
        if 'extraction_stats' not in st.session_state:
            st.session_state.extraction_stats = {"found": 0, "duplicates": 0}
        
        if extract_btn:
            if not input_text.strip():
                st.markdown("""
                <div class="ozon-alert ozon-alert-warning">
                    <strong>⚠️ Внимание</strong><br>
                    Введите текст для извлечения SKU
                </div>
                """, unsafe_allow_html=True)
            else:
                with st.spinner("🔍 Извлекаем SKU..."):
                    try:
                        # Отправка события в метрику
                        st.markdown("<script>if(typeof ym!=='undefined')ym(104969939,'reachGoal','extraction_started')</script>", unsafe_allow_html=True)
                        
                        sku_list, raw_count = extract_sku_from_text(input_text)
                        duplicate_count = raw_count - len(sku_list)
                        
                        st.session_state.sku_list = sku_list
                        st.session_state.extraction_stats = {
                            "found": len(sku_list),
                            "duplicates": duplicate_count
                        }
                        
                        # Отправка события об успехе
                        st.markdown("<script>if(typeof ym!=='undefined')ym(104969939,'reachGoal','extraction_success')</script>", unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.markdown(f"""
                        <div class="ozon-alert ozon-alert-error">
                            <strong>❌ Ошибка</strong><br>
                            {str(e)}
                        </div>
                        """, unsafe_allow_html=True)
        
        if st.session_state.sku_list:
            stats = st.session_state.extraction_stats
    
            duplicate_info = f'<div class="ozon-status">♻️ Удалено дубликатов: <strong>{stats["duplicates"]}</strong></div>' if stats["duplicates"] > 0 else ''
    
            st.markdown(f"""
            <div class="ozon-alert ozon-alert-success ozon-fade-in">
                <strong>✅ Успешно извлечено!</strong><br>
                <div style="background: transparent; border: none; padding: 0.5rem 0;">
                    Найдено SKU: <strong>{stats['found']}</strong>
                </div>
                {duplicate_info}
             </div>
            """, unsafe_allow_html=True)
    
            st.markdown("""
            <div class="ozon-card ozon-fade-in">
                <div class="card-header">
                    <span class="card-icon">📋</span>
                    <h4 class="card-title">Найденные SKU</h4>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
            result_text = "\n".join(st.session_state.sku_list)
            st.text_area("**Список извлеченных SKU:**", value=result_text, height=200, key="results", label_visibility="collapsed")
    
            if st.session_state.sku_list:
                timestamp = (datetime.now() + timedelta(hours=3)).strftime("%d-%m-%Y_%H-%M-%S")
                filename = f"ozon_sku_{timestamp}.csv"
                st.markdown(get_csv_download_link(st.session_state.sku_list, filename), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
