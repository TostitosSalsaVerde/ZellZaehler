import streamlit as st

# List of custom button names
button_names = [
    "Pro", "Mye", "Meta", "Stab", "Seg", "Eos",
    "Baso", "Mono", "Ly", "neu1", "neu2", "neu3"
]
# Initialize session states for button counts, edit mode, name edit mode, and custom names
for name in button_names:
    if f'count_{name}' not in st.session_state:
        st.session_state[f'count_{name}'] = 0
if 'edit_mode' not in st.session_state:
    st.session_state['edit_mode'] = False  # Count edit mode state
if 'name_edit_mode' not in st.session_state:
    st.session_state['name_edit_mode'] = False  # Name edit mode state

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
rows = [st.columns(cols_per_row) for _ in range(len(button_names) // cols_per_row)]
current_row = 0
button_pressed = None  # Track which button was pressed       

for index, name in enumerate(button_names):
    col = rows[current_row][index % cols_per_row]
    with col:
        if index >= 9:
            display_name = st.session_state.get(f'custom_name_{name}', "Neu")
        else:
            display_name = name

        button_label = f"{display_name}\n({st.session_state[f'count_{name}']})"
        if st.button(button_label, key=f'button_{name}'):
            if not st.session_state['edit_mode'] and not st.session_state['name_edit_mode']:
                button_pressed = name  # Mark button as pressed

        if st.session_state['edit_mode']:
            new_count = st.number_input("Zähler korrigieren", value=st.session_state[f'count_{name}'], key=f'edit_{name}')
            st.session_state[f'count_{name}'] = new_count

        if st.session_state['name_edit_mode'] and index >= 9:
            new_display_name = st.text_input("Zelle bearbeiten", value=display_name, key=f'new_name_{name}')
            if new_display_name != display_name:
                st.session_state[f'custom_name_{name}'] = new_display_name

if button_pressed is not None:
    increment_button_count(button_pressed)
    if total_count + 1 == 100:  # Check if reaching 100 after button press
        st.experimental_rerun()

if button_pressed is not None:   
    if total_count == 100:
        st.error("Das Zählziel von 100 wurde bereits erreichte.")
        st.experimental_rerun()



if st.button('Reset All Counts'):
    for name in button_names:
        st.session_state[f'count_{name}'] = 0

# Handle button press after all buttons are displayed
if button_pressed is not None:
    st.experimental_rerun()  # Optionally force a rerun to update the UI immediately
