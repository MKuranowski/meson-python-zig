project('pypkg', 'c')

py = import('python').find_installation(pure: false)

py.install_sources(
    [
        'pypkg/__init__.py',
        'pypkg/__main__.py',
    ],
    subdir: 'pypkg',
)

shared_library(
    'extern',
    ['pypkg/extern.c'],
    install: true,
    install_dir: py.get_install_dir() / 'pypkg',
)
