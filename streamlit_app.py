from random import choice
import streamlit as st

QUERY_PARAM_NAME = 'choices'
st.title('Random choice selector 🎲')
get_next = False


def update_choice(option, it=None):
    available_choices = st.query_params.get_all(QUERY_PARAM_NAME)
    if it is not None:
        available_choices[it] = option
    else:
        available_choices.append(option)

    st.query_params[QUERY_PARAM_NAME] = available_choices


def delete_choice(option):
    available_choices = st.query_params.get_all(QUERY_PARAM_NAME)
    try:
        available_choices.remove(option)
    except ValueError:
        pass

    st.query_params[QUERY_PARAM_NAME] = available_choices


def get_random_choice():
    available_choices = st.query_params.get_all(QUERY_PARAM_NAME)
    next_choice = choice(available_choices, )
    available_choices.remove(next_choice)
    st.query_params[QUERY_PARAM_NAME] = available_choices
    return next_choice


def generate_row(it, option):
    col1, col2 = st.columns(2)
    with col1:
        updated_text = st.text_input(label=f'Option: {it+1}', value=option, label_visibility='collapsed')
        if updated_text != option:
            update_choice(updated_text, it)
    with col2:
        st.button(label='Delete ❌', on_click=lambda: delete_choice(option), key=f'Delete: {it}', use_container_width=True)


with st.expander(label='Choices'):
    st.markdown('''
        Provide multiple choices, you can edit, add and delete them from this section
        After you are done click the roll button to get a new random choice,
        You can save your preselected choices by simply copying link or bookmarking it
    ''')

    for it, option in enumerate(st.query_params.get_all(QUERY_PARAM_NAME)):
        generate_row(it, option)

    col1, col2 = st.columns(2)
    with col1:
        new_text = st.text_input(label=f'New Option', value='', label_visibility='collapsed', key='new')

    with col2:
        st.button(label='Add ✅', use_container_width=True, on_click=lambda: update_choice(new_text))

st.subheader('Options')
st.text(', '.join(st.query_params.get_all(QUERY_PARAM_NAME)))

if st.query_params.get_all(QUERY_PARAM_NAME):
    get_next = st.button('Roll 🎰', use_container_width=True)

if get_next:
    st.header('_Next choice:_')
    st.markdown(f"<h1 style='text-align: center;'>{get_random_choice()}</h1>", unsafe_allow_html=True)

    st.balloons()
