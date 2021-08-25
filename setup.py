from cx_Freeze import setup, Executable

executables = [
        Executable(script = "generateur_labyrinthe.py",icon = "images/icon_laby.ico", base = "Win32GUI" )
]

buildOptions = dict(
        includes = ["tkinter","random","tkinter.messagebox","module_laby.py","module_pile.py"],
        include_files = ["images"]
)

setup(
    name = "Generateur de Labyrinthe",
    version = "2.0",
    description = "Labyrinthe & Co",
    author = "Didier Mathias",
    options = dict(build_exe = buildOptions),
    executables = executables
)