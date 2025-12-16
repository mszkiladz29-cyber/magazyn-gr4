import streamlit as st
import random

# Inicjalizacja stanu sesji dla listy produktów
# Używamy st.session_state, aby lista produktów była zachowywana
# pomiędzy interakcjami użytkownika w aplikacji Streamlit.
if 'inventory' not in st.session_state:
    st.session_state.inventory = ["Kabel HDMI", "Mysz Bezprzewodowa", "Klawiatura Mechaniczna"]

def add_product(product_name):
    """Dodaje produkt do magazynu."""
    if product_name and product_name not in st.session_state.inventory:
        st.session_state.inventory.append(product_name)
        st.success(f"Dodano produkt: **{product_name}**")
    elif product_name in st.session_state.inventory:
        st.warning(f"Produkt **{product_name}** jest już w magazynie.")
    else:
        st.warning("Nazwa produktu nie może być pusta.")

def delete_product(product_name):
    """Usuwa produkt z magazynu."""
    if product_name and product_name in st.session_state.inventory:
        st.session_state.inventory.remove(product_name)
        st.success(f"Usunięto produkt: **{product_name}**")
    else:
        st.error(f"Nie znaleziono produktu: **{product_name}** w magazynie.")

# --- Interfejs użytkownika Streamlit ---

st.set_page_config(page_title="Prosty Magazyn", layout="wide")
st.title("🛒 Prosta Aplikacja Magazynowa")
st.markdown("Aplikacja pozwala na dodawanie i usuwanie produktów. Dane są przechowywane tylko podczas trwania sesji.")

# --- Sekcja Dodawania Produktu ---
st.header("➕ Dodaj Produkt")
with st.form("add_form", clear_on_submit=True):
    new_product_name = st.text_input("Nazwa nowego produktu", key="new_product_input")
    submitted = st.form_submit_button("Dodaj do Magazynu")
    if submitted:
        add_product(new_product_name.strip())

# --- Sekcja Usuwania Produktu ---
st.header("➖ Usuń Produkt")
# Użycie funkcji selectbox do wyboru z istniejących produktów
if st.session_state.inventory:
    product_to_delete = st.selectbox(
        "Wybierz produkt do usunięcia",
        options=st.session_state.inventory,
        key="delete_select"
    )
    if st.button("Usuń Wybrany Produkt"):
        delete_product(product_to_delete)
else:
    st.info("Magazyn jest pusty. Dodaj najpierw jakieś produkty.")


# --- Sekcja Aktualnego Stanu Magazynu ---
st.header("📋 Aktualny Stan Magazynu")

if st.session_state.inventory:
    # Wyświetlanie listy produktów w formie tabeli
    # Stworzenie listy słowników dla lepszego wyświetlenia w Streamlit
    inventory_data = [{"ID": i + 1, "Nazwa Produktu": name} for i, name in enumerate(st.session_state.inventory)]
    st.dataframe(inventory_data, use_container_width=True)
    st.caption(f"Liczba unikalnych produktów w magazynie: **{len(st.session_state.inventory)}**")
else:
    st.info("Magazyn jest obecnie pusty.")

# Stopka
st.markdown("---")
st.markdown("Pamiętaj: dane nie są zapisywane i znikną po odświeżeniu strony.")
