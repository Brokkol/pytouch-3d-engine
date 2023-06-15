from distutils.core import setup, Extension

pytouch_c_module = Extension("pytouch_c", sources=["pytouch_c.c"])

setup(
    name="pytouch_c",
    version="1.0",
    description="This is a pytouch_c package",
    ext_modules=[pytouch_c_module],
)
