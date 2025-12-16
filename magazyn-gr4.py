import streamlit as st
import pandas as pd
from datetime import date
import random # Potrzebne do losowej mocy Reniferów

# Inicjalizacja stanu sesji
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        "Latające Sanki 🛷", 
        "Czekoladowe Bombki 🍫", 
        "Robot-Elfik Pomocnik 🤖", 
        "Magiczny Płaszcz Niewidka ✨", 
        "Ekspres do Gorącej Czekolady"
    ]
if 'reindeer_power' not in st.session_state:
    # Początkowa, losowa moc zaprzęgu
    st.session_state.reindeer_power = random.randint(70, 95)

# --- Funkcje (Dodajemy funkcję zarządzania reniferami) ---

def add_product(product_name):
    """Dodaje produkt do magazynu prezentów."""
    normalized_name = product_name.strip().capitalize()
    
    if normalized_name and normalized_name not in st.session_state.inventory:
        st.session_state.inventory.append(normalized_name)
        st.balloons() 
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

def feed_reindeer():
    """Symulacja karmienia reniferów - zwiększa ich moc."""
    # Losowe zwiększenie mocy
    power_boost = random.randint(5, 15)
    st.session_state.reindeer_power = min(100, st.session_state.reindeer_power + power_boost)
    st.success(f"Dano marchewki i magiczny owies! Moc zaprzęgu wzrosła o {power_boost}!")

# --- Interfejs użytkownika Streamlit ---

st.set_page_config(page_title="Magazyn Mikołaja - Renifery!", layout="wide")

# Używamy HTML do lekkiej personalizacji nagłówka i emotikonów
st.markdown(
