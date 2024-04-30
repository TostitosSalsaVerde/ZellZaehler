import streamlit as st

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
    "Baso", "Mono", "Ly", "Blast", "NRBC", "Div"
]

button_positions = [
    ["Pro", "Mye", "Meta"],
    ["Stab", "Seg", "Eos"],
    ["Baso", "Mono", "Ly"],
    ["Blast", "NRBC", "Div"]
]

for name in button_names:
    if f'count_{name}' not in st.session_state:
        st.session_state[f'count_{name}'] = 0

if 'edit_mode' not in st.session_state:
    st.session_state['edit_mode'] = False

if 'name_edit_mode' not in st.session_state:
    st.session_state['name_edit_mode'] = False

def increment_button_count(name):
    total_count = sum(st.session_state[f'count_{name}'] for name in button_names)
    if total_count >= 100:
        st.error("Das Zählziel von 100 wurde bereits erreicht.")
    else:
        st.session_state[f'count_{name}'] += 1

if st.button('Korrigieren'):
    st.session_state['edit_mode'] = not st.session_state['edit_mode']

if st.button('Zelle hinzufügen'):
    st.session_state['name_edit_mode'] = not st.session_state['name_edit_mode']

total_count = sum(st.session_state[f'count_{name}'] for name in button_names)
st.write(f"{total_count}/100")

if total_count == 100:
    st.success("100 Zellen gezählt!")

cols_per_row = 3
rows = [st.columns(cols_per_row) for _ in range(len(button_positions))]

button_pressed = None  # Vor der Schleife hinzufügen

for row_index, row in enumerate(button_positions):
    for col_index, name in enumerate(row):
        col = rows[row_index][col_index]
        with col:
            if name == "Blast" or name == "NRBC" or name == "Div":
                display_name = st.session_state.get(f'custom_name_{name}', "Neu")
            else:
                display_name = name
            button_label = f"{display_name}\n({st.session_state[f'count_{name}']})"
            if st.button(button_label, key=f'button_{name}'):
                if not st.session_state['edit_mode'] and not st.session_state['name_edit_mode']:
                    button_pressed = name
            if st.session_state['edit_mode']:
                new_count = st.number_input("Zähler korrigieren", value=st.session_state[f'count_{name}'], key=f'edit_{name}')
                st.session_state[f'count_{name}'] = new_count
            if st.session_state['name_edit_mode'] and (name == "Blast" or name == "NRBC" or name == "Div"):
                new_display_name = st.text_input("Zelle bearbeiten", value=display_name, key=f'new_name_{name}')
                if new_display_name != display_name:
                    st.session_state[f'custom_name_{name}'] = new_display_name

# Nach der Schleife hinzufügen
if button_pressed is not None:
    increment_button_count(button_pressed)
    if total_count + 1 == 100:
        st.rerun()

if button_pressed is not None:   
    if total_count == 100:
        st.error("Das Zählziel von 100 wurde bereits erreicht.")
        st.rerun()

if st.button('Reset All Counts'):
    for name in button_names:
        st.session_state[f'count_{name}'] = 0

if button_pressed is not None:
    st.rerun()
