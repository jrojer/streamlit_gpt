from streamlit.web import cli as stcli
from streamlit import runtime
from app.src.streamlit.application import application_run
import sys


if __name__ == "__main__":
    if runtime.exists():
        application_run()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
