import streamlit as st
from utils.multipage import MultiPage
from pages import home

# Create an instance of the app
app = MultiPage()

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
                st.session_state["username"] in st.secrets["passwords"]
                and st.session_state["password"]
                == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            # del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False, None
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("User not known or password incorrect")
        return False, None
    else:
        user = st.session_state["username"]
        # Password correct.
        return True, user

check, user = check_password()
if check:
    st.session_state["username"] = user

    # Add all your applications (pages) here
    app.add_page("Overzicht", home.app)
    # app.add_page("Kosten", data_upload.app)
    # app.add_page("Update budget & estimate", data_table.app)

    # The main app
    app.run()