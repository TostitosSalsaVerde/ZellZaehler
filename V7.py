import streamlit as st
import pandas as pd

# Funktion zur Konfiguration des Themes
def set_theme(primary_color, background_color, secondary_background_color, text_color, font):
    custom_css = f"""
    <style>
        :root {{
            --primary-color: {primary_color};
            --background-color: {background_color};
            --secondary-background-color: {secondary_background_color};
            --text-color: {text_color};
            --font: {font};
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Theme-Konfiguration
primary_color = "#f90eb6"
background_color = "#fff0f3"
secondary_background_color = "#bbb9b9"
text_color = "#bb072b"
font = "monospace"

# Setzen des Themes
set_theme(primary_color, background_color, secondary_background_color, text_color, font)

button_names = [
    "Pro", "Mye", "Meta", "Stab", "Seg", "Eos",
    "Baso", "Mono", "Ly", "Div1", "Div2", "Div3"
]

# Zähler initialisieren
if 'history' not in st.session_state:
    st.session_state['history'] = []
for name in button_names:
    if f'count_{name}' not in st.session_state:
        st.session_state[f'count_{name}'] = 0
if 'edit_mode' not in st.session_state:
    st.session_state['edit_mode'] = False
if 'name_edit_mode' not in st.session_state:
    st.session_state['name_edit_mode'] = False

# Funktion zur Inkrementierung des Zählers
def increment_button_count(name):
    total_count = sum(st.session_state[f'count_{name}'] for name in button_names)
    if total_count >= 100:
        st.error("Das Zählziel von 100 wurde bereits erreicht.")
    else:
        st.session_state[f'count_{name}'] += 1

# Funktion zum Speichern des aktuellen Zustands
def save_state():
    current_counts = {name: st.session_state[f'count_{name}'] for name in button_names}
    st.session_state['history'].append(current_counts)

# Funktion zum Rückgängigmachen des letzten Schritts
def undo_last_step():
    if st.session_state['history']:
        last_state = st.session_state['history'].pop()
        for name in button_names:
            st.session_state[f'count_{name}'] = last_state[name]

# Funktion zur Anzeige der Ergebnisse
def display_results():
    st.write("Ergebnisse:")
    result_df = pd.DataFrame({'Zellentyp': button_names, 'Anzahl': [st.session_state[f'count_{name}'] for name in button_names]})
    st.dataframe(result_df, hide_index=True)

# Hauptteil des Codes
if st.button('Korrigieren'):
    st.session_state['edit_mode'] = not st.session_state['edit_mode']
if st.button('Zelle hinzufügen'):
    st.session_state['name_edit_mode'] = not st.session_state['name_edit_mode']

# Button zum Rückgängigmachen des letzten Schritts
if st.button('Rückgängig'):
    undo_last_step()

# Button zum Zurücksetzen der Zählung
if st.button('Zählung zurücksetzen'):
    for name in button_names:
        st.session_state[f'count_{name}'] = 0

# Gesamtzahl der Zellen zählen
total_count = sum(st.session_state[f'count_{name}'] for name in button_names)
st.write(f"{total_count}/100")

# Erfolgsmeldung anzeigen, wenn das Zählziel erreicht ist
if total_count == 100:
    st.success("100 Zellen gezählt!")
    st.button('Rückgängig', disabled=True, key='undo_button')
    st.button('Zelle hinzufügen (disabled)', disabled=True, key='add_cell_button')
    display_results()

# Spalten für die Schaltflächen
cols_per_row = 3
rows = [st.columns(cols_per_row) for _ in range(len(button_names) // cols_per_row + 1)]

# Schaltflächen für jeden Zellentyp anzeigen
button_pressed = None  # Vor der Schleife hinzufügen
for name in button_names:
    index = button_names.index(name)
    row_index, col_index = divmod(index, cols_per_row)
    col = rows[row_index][col_index]
    with col:
        display_name = name
        button_label = f"{display_name}\n({st.session_state[f'count_{name}']})"
        if st.button(button_label, key=f'button_{name}'):
            if not st.session_state['edit_mode'] and not st.session_state['name_edit_mode']:
                save_state()  # Zustand speichern bevor geändert wird
                button_pressed = name  # Mark button as pressed
        if st.session_state['edit_mode']:
            new_count = st.number_input("Zähler korrigieren", value=st.session_state[f'count_{name}'], key=f'edit_{name}')
            st.session_state[f'count_{name}'] = new_count

# Nach der Schleife hinzufügen
if button_pressed is not None:
    increment_button_count(button_pressed)
    if total_count + 1 == 100:
        st.rerun()

# Fehlermeldung anzeigen, wenn das Zählziel erreicht ist
if button_pressed is not None:   
    if total_count == 100:
        st.error("Das Zählziel von 100 wurde bereits erreicht.")
        st.rerun()

# Buttons für die zweite Zählung
if st.button('Zweite Zählung'):
    st.session_state['edit_mode'] = False  # Zurücksetzen des Edit-Modus
    st.session_state['name_edit_mode'] = False  # Zurücksetzen des Name-Edit-Modus

    # Zähler für die zweite Zählung initialisieren
    if 'history_2' not in st.session_state:
        st.session_state['history_2'] = []
    for name in button_names:
        if f'count_{name}_2' not in st.session_state:
            st.session_state[f'count_{name}_2'] = 0

    # Funktion zur Inkrementierung des Zählers für die zweite Zählung
    def increment_button_count_2(name):
        total_count = sum(st.session_state[f'count_{name}_2'] for name in button_names)
        if total_count >= 100:
            st.error("Das Zählziel von 100 wurde bereits in der zweiten Zählung erreicht.")
        else:
            st.session_state[f'count_{name}_2'] += 1

    # Funktion zum Speichern des aktuellen Zustands für die zweite Zählung
    def save_state_2():
        current_counts = {name: st.session_state[f'count_{name}_2'] for name in button_names}
        st.session_state['history_2'].append(current_counts)

    # Funktion zum Rückgängigmachen des letzten Schritts für die zweite Zählung
    def undo_last_step_2():
        if st.session_state['history_2']:
            last_state = st.session_state['history_2'].pop()
            for name in button_names:
                st.session_state[f'count_{name}_2'] = last_state[name]

    # Schaltflächen für die zweite Zählung anzeigen
    st.write("Zweite Zählung:")
    total_count_2 = sum(st.session_state[f'count_{name}_2'] for name in button_names)
    st.write(f"{total_count_2}/100")

    if total_count_2 == 100:
        st.success("100 Zellen in der zweiten Zählung gezählt!")

    for name in button_names:
        if st.button(f"{name} (2. Zählung)"):
            if not st.session_state['edit_mode'] and not st.session_state['name_edit_mode']:
                save_state_2()
                increment_button_count_2(name)

    if st.button('Rückgängig (2. Zählung)'):
        undo_last_step_2()

