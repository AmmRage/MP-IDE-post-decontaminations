"""
/usr/bin/pybricks-repl content:
#!/bin/sh
brickrun -r -- pybricks-micropython -i -c 'from core import *'

help("modules"):

__main__          mmap              pybricks/tools    ufcntl
_thread           nxtdevices_c      pybricks/uev3dev/__init__           uhashlib
array             parameters_c      pybricks/uev3dev/_alsa              uheapq
bluetooth_c       pybricks/__init__ pybricks/uev3dev/_wand              uio
btree             pybricks/bluetooth                  pybricks/uev3dev/display            ujson
builtins          pybricks/display  pybricks/uev3dev/i2c                umachine
cmath             pybricks/ev3brick pybricks/uev3dev/messaging          uos
core              pybricks/ev3devices                 pybricks/uev3dev/sound              urandom
ev3devices_c      pybricks/ev3devio pybricks/uev3dev/util               ure
experimental_c    pybricks/experimental               robotics_c        uselect
ffi               pybricks/hubs     sys               usignal
framebuf          pybricks/iodevices                  termios           usocket
gc                pybricks/media/ev3dev               tools             ussl
hubs_c            pybricks/messaging                  ubinascii         ustruct
iodevices_c       pybricks/nxtdevices                 ucollections      utime
math              pybricks/parameters                 ucryptolib        utimeq
media_ev3dev_c    pybricks/robotics uctypes           uwebsocket
micropython       pybricks/speaker  uerrno            uzlib
Plus any modules on the filesystem


"""

from tkinter import ttk

from thonny import get_workbench
from thonny.config_ui import (
    add_label_and_text,
    add_label_and_url,
    add_text_row,
    add_vertical_separator,
)
from thonny.languages import tr
from thonny.misc_utils import running_on_windows
from thonny.plugins.micropython import (
    SshMicroPythonConfigPage,
    SshMicroPythonProxy,
    add_micropython_backend,
)
from thonny.ui_utils import create_url_label, ems_to_pixels


class EV3MicroPythonProxy(SshMicroPythonProxy):
    def _get_launcher_with_args(self):
        import thonny.plugins.ev3.ev3_back

        args = {
            "cwd": get_workbench().get_option(f"{self.backend_name}.cwd") or "",
            "interpreter": self._target_executable,
            "host": self._host,
            "user": self._user,
        }

        args.update(self._get_time_args())
        args.update(self._get_extra_launcher_args())

        cmd = [
            thonny.plugins.ev3.ev3_back.__file__,
            repr(args),
        ]
        return cmd

    def _get_extra_launcher_args(self):
        return {"interpreter_launcher": ["brickrun", "-r", "--"]}


class EV3MicroPythonConfigPage(SshMicroPythonConfigPage):
    def _init_connection_page(self):
        add_label_and_url(
            self.connection_page,
            tr("Preparations (skip the VS Code part)"),
            "https://pybricks.com/ev3-micropython/",
        )

        add_vertical_separator(self.connection_page)
        super()._init_connection_page()
        add_vertical_separator(self.connection_page)

        add_label_and_text(self.connection_page, "EV3 default password", "maker")

    def has_editable_interpreter(self) -> bool:
        return False


def load_plugin():
    add_micropython_backend(
        "EV3MicroPython",
        EV3MicroPythonProxy,
        "MicroPython (EV3)",
        EV3MicroPythonConfigPage,
        bare_metal=False,
        sort_key="23",
    )
    get_workbench().set_default("EV3MicroPython.executable", "pybricks-micropython")
    get_workbench().set_default("EV3MicroPython.make_uploaded_shebang_scripts_executable", True)
    get_workbench().set_default("EV3MicroPython.cwd", None)
    get_workbench().set_default(
        "EV3MicroPython.host", "ev3dev" if running_on_windows() else "ev3dev.local"
    )
    get_workbench().set_default("EV3MicroPython.user", "robot")
    get_workbench().set_default("EV3MicroPython.auth_method", "password")
