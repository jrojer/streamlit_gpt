import streamlit as st
from uuid import uuid4
from streamlit_cookies_controller import CookieController  # type: ignore
import hashlib
from app.src.internal import env

controller = CookieController()


def hash_password(password: str):
    password_bytes = password.encode("utf-8")
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()


@st.cache_data(ttl=env.PASSWORD_TTL_SECONDS())
def _token() -> str:
    return str(uuid4())


def check_password():
    try:
        tkn = controller.get("customAuthToken")
    except Exception:
        tkn = None
    if tkn == _token():
        return True

    text = st.text_input(
        "Password",
        type="password",
        key="password",
        label_visibility="collapsed",
    )
    if hash_password(text) == env.PASSWORD_HASH():
        del st.session_state["password"]
        tkn = _token()
        controller.set("customAuthToken", tkn)
        st.rerun()
        return True
    return False


def logout() -> None:
    controller.remove("customAuthToken")
