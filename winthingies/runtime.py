import os
from winthingies.process import Process
from winthingies.win32.kernel32 import kernel32

current_process = kernel32.GetCurrentProcess()
CURRENT_PROCESS = Process(
    os.getpid(),
    current_process
)
