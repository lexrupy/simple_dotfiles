import os
import subprocess
from powerline_shell.utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        env = (
            os.getenv("VIRTUAL_ENV")
            or os.getenv("CONDA_ENV_PATH")
            or os.getenv("CONDA_DEFAULT_ENV")
        )
        if os.getenv("VIRTUAL_ENV") and os.path.basename(env) == ".venv":
            env = os.path.basename(os.path.dirname(env))
        #version_info = str(p1.communicate())
        if not env:
            return

        p1 = subprocess.Popen(['python', '-V'], stdout=subprocess.PIPE)
        version_info = p1.communicate()[0].decode('utf-8').rstrip()

        env_name = os.path.basename(env)
        bg = self.powerline.theme.VIRTUAL_ENV_BG
        fg = self.powerline.theme.VIRTUAL_ENV_FG
        self.powerline.append(" " + version_info + " 󰉀 " + env_name + "", fg, bg)
