import streamlit as st
import pandas as pd
# Importowanie datetime dla małego dodatku świątecznego
from datetime import date

# Inicjalizacja stanu sesji dla listy produktów
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        "Latające Sanki 🛷", 
        "Czekoladowe Bombki 🍫", 
        "Robot-Elfik Pomocnik 🤖", 
        "Magiczny Płaszcz Niewidka ✨", 
        "Ekspres do Gorącej Czekolady"
    ]

# --- Funkcje (bez zmian, tylko komunikaty) ---

def add_product(product_name):
    """Dodaje produkt do magazynu prezentów."""
    normalized_name = product_name.strip().capitalize()
    
    if normalized_name and normalized_name not in st.session_state.inventory:
        st.session_state.inventory.append(normalized_name)
        st.balloons() # Dodajemy balony (konfetti) Streamlit na udane dodanie
        st.success(f"Ho! Ho! Ho! Dodano prezent: **{normalized_name}** do worka Mikołaja! 🎅")
    elif normalized_name in st.session_state.inventory:
        st.warning(f"Ten prezent (**{normalized_name}**) już jest na liście dla grzecznych dzieci. Sprawdź dokładnie!")
    else:
        st.warning("Nazwa prezentu nie może być pusta. Sprawdź listę!")

def delete_product(product_name):
    """Usuwa prezent z magazynu."""
    if product_name and product_name in st.session_state.inventory:
        st.session_state.inventory.remove(product_name)
        st.info(f"Usunięto prezent: **{product_name}**. Może trafi na przyszły rok? 🎄")
    else:
        st.error(f"Błąd! Nie znaleziono prezentu: **{product_name}** w worku Mikołaja.")

# --- Interfejs użytkownika Streamlit ---

st.set_page_config(page_title="Magazyn Mikołaja", layout="wide")

# Używamy HTML do lekkiej personalizacji nagłówka i emotikonów
st.markdown(
    """
    <style>
    .christmas-header {
        font-size: 40px;
        color: #A30B1C; /* Ciemna Czerwień Mikołaja */
        text-shadow: 2px 2px #38761d; /* Ciemna Zieleń Elfów */
        padding-bottom: 10px;
    }
    .stApp {
        background-color: #F8F8F8; /* Jasne tło, aby kolory były widoczne */
    }
    </style>
    <div class="christmas-header">
        🎅 Skład Prezentów Świętego Mikołaja 🎁
    </div>
    """, 
    unsafe_allow_html=True
)
st.caption("Zarządzaj listą prezentów, które Mikołaj musi dostarczyć. Ho! Ho! Ho!")

# --- Sekcja Metryki i Daty ---

current_count = len(st.session_state.inventory)
target_count = 100 # Cel: Mikołaj musi mieć 100 prezentów!

# Ile dni pozostało do Świąt (przy założeniu, że jest grudzień)
today = date.today()
christmas_day = date(today.year, 12, 24)
days_to_christmas = (christmas_day - today).days

col_metric, col_info, col_date = st.columns([1, 1, 1])

with col_metric:
    st.metric(
        label="🎁 Liczba Prezentów w Worku", 
        value=current_count, 
        delta=f"Brakuje: {target_count - current_count} do celu {target_count}", 
        delta_color="off"
    )
    
with col_date:
    if days_to_christmas >= 0:
        st.metric(
            label="🗓️ Dni do Wigilii", 
            value=days_to_christmas, 
            delta="Pracujemy ciężko!", 
            delta_color="normal"
        )
    else:
        st.metric(label="🗓️ Dni do Wigilii", value="Święta minęły!", delta="Wracamy za rok! 🥳")

st.markdown("---")

# --- Sekcja Dodawania i Usuwania ---
col_add, col_delete = st.columns(2)

with col_add:
    st.header("✨ Wpisz Nowy Prezent na Listę Grzecznych Dzieci")
    with st.form("add_form", clear_on_submit=True):
        new_product_name = st.text_input("Nazwa Magicznego Prezentu", key="new_product_input")
        submitted = st.form_submit_button("🌟 Dodaj Prezent")
        if submitted:
            add_product(new_product_name.strip())

with col_delete:
    st.header("🗑️ Usuń z Listy (dla Niegrzecznych Dzieci)")
    if st.session_state.inventory:
        sorted_inventory = sorted(st.session_state.inventory)
        product_to_delete = st.selectbox(
            "Wybierz Prezent do Anulowania",
            options=sorted_inventory,
            key="delete_select"
        )
        if st.button("❌ Usuń Wybrany Prezent (Węgiel?)", use_container_width=True):
            delete_product(product_to_delete)
    else:
        st.info("Lista Prezentów Mikołaja jest pusta. Dodaj coś szybko!")

st.markdown("---")

# --- Sekcja Aktualnego Stanu Magazynu i Filtrowania ---

st.header("🔎 Lista Prezentów w Worku Mikołaja")

if st.session_state.inventory:
    
    search_term = st.text_input(
        "Filtruj prezenty (wpisz, np. 'magiczny' lub 'robot'):", 
        key="search_input"
    ).lower().strip()
    
    inventory_data = [{"ID Prezentu": i + 1, "Nazwa Magicznego Przedmiotu": name} for i, name in enumerate(st.session_state.inventory)]
    df_inventory = pd.DataFrame(inventory_data)
    
    if search_term:
        filtered_df = df_inventory[df_inventory['Nazwa Magicznego Przedmiotu'].str.lower().str.contains(search_term)]
        st.subheader(f"Znaleziono {len(filtered_df)} prezentów pasujących do frazy:")
    else:
        filtered_df = df_inventory
        st.subheader("Cała Lista Prezentów:")
        
    st.dataframe(
        filtered_df, 
        use_container_width=True,
        hide_index=True
    )
    
    st.caption(f"Elfy z Laponii zarządzają aktualnie {len(df_inventory)} unikalnymi rodzajami prezentów. 🎄")
    
else:
    st.error("Alarm! Magazyn Mikołaja jest pusty! Wzywamy Elfy!")

# --- Stopka ---
st.markdown("---")
st.markdown("Pamiętaj, że wszystkie prezenty są magiczne i znikną po odświeżeniu strony! ✨")
