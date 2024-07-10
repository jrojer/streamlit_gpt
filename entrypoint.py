from streamlit.web import cli as stcli
from streamlit import runtime
from app.src.streamlit.application import application_run
from app.src.internal import env
import sys


if __name__ == "__main__":
    if runtime.exists():
        application_run()
    else:
        sys.argv = [
            "streamlit",
            "run",
            sys.argv[0],
            "--server.headless",
            "true",
            f"--server.port={env.PORT()}",
            f"--server.baseUrlPath={env.PREFIX()}",
        ]
        sys.exit(stcli.main())
