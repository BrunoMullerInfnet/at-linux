import sys


def pedir_desempenho():
    # este notebook tem nucleos lentos; sem isso o Windows joga o Python neles
    if sys.platform != "win32":
        return
    import ctypes
    from ctypes import wintypes

    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.GetCurrentProcess.restype = ctypes.c_void_p
    k.SetProcessInformation.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_size_t]
    k.SetProcessInformation.restype = ctypes.c_int
    k.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint]
    k.SetPriorityClass.restype = ctypes.c_int

    class Estado(ctypes.Structure):
        _fields_ = [
            ("Version", wintypes.ULONG),
            ("ControlMask", wintypes.ULONG),
            ("StateMask", wintypes.ULONG),
        ]

    h = k.GetCurrentProcess()
    estado = Estado(1, 1, 0)
    k.SetProcessInformation(h, 4, ctypes.byref(estado), ctypes.sizeof(estado))
    k.SetPriorityClass(h, 0x00008000)
