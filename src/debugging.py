import pydevd_pycharm

pydevd_pycharm.settrace(
    "host.docker.internal", port=5780, stdoutToServer=True, stderrToServer=True
)
