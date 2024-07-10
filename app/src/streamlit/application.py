# type: ignore
import streamlit as st
import asyncio
from app.src.gpt.gpt_completer import GptCompleter
from app.src.gpt.content_type import ContentType
from app.src.gpt.message import Message, user_message, image_message
from app.src.gpt.image import Image
from app.src.streamlit.utils import hide_menu, get_or_create_eventloop
from app.src.streamlit.auth import check_password

SYSTEM_PROMPT = r"""\
Ouput markdown as for jupyter notebook. Single dollar "$" for inline math. Double "$$" for block math.
Do not enclose the output in triple quotes "```".
Example:
The matrix $\mathbf{C}^*$.
"""


def redraw(my_bar, loop: asyncio.AbstractEventLoop):
    messages: list[Message] = st.session_state["messages"]
    gpt_reply_container = st.container(border=1)
    for m in reversed(messages):
        if m.content_type() == ContentType.Image:
            st.image(Image.from_base64(m.content())._image_data)
        else:
            st.container(border=1).markdown(m.content())

    completed = False

    async def gpt_complete(messages: list[Message]) -> Message:
        res = await GptCompleter(SYSTEM_PROMPT).complete(messages)
        nonlocal completed
        completed = True
        return res

    async def progress():
        for i in range(1, 101):
            if completed:
                break
            my_bar.progress(i)
            await asyncio.sleep(0.5)

    res = loop.run_until_complete(asyncio.gather(gpt_complete(messages), progress()))
    completion: Message = res[0]
    gpt_reply_container.markdown(completion.content())
    messages.append(completion)
    my_bar.progress(0)


def application_run():
    hide_menu()
    if not check_password():
        st.stop()
    loop = get_or_create_eventloop()
    my_bar = st.progress(0)
    my_bar.progress(0)
    with st.form(key="my_form", clear_on_submit=True):
        col1, col2 = st.columns([9, 1])
        with col1:
            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
            )
            user_input = st.text_area(
                label="Your message", label_visibility="collapsed"
            )
        with col2:
            st.container(height=105, border=0)  # placeholder
            st.form_submit_button(label="➤")
        messages = st.session_state.get("messages", [])
        st.session_state["messages"] = messages
        if uploaded_file:
            bytes_data = uploaded_file.getvalue()
            messages.append(image_message(Image.from_bytes(bytes_data)))
        if user_input:
            messages.append(user_message(user_input))
        if user_input or uploaded_file:
            redraw(my_bar, loop)
