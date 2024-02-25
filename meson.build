project('pypkg', 'c')

py = import('python').find_installation(pure: false)

py.install_sources(
    [
        'pypkg/__init__.py',
        'pypkg/__main__.py',
    ],
    subdir: 'pypkg',
)

if host_machine.system() == 'windows'
    lib_suffix = '.dll'
elif host_machine.system() == 'darwin'
    lib_suffix = '.dylib'
elif host_machine.system() == 'linux'
    lib_suffix = '.so'
else
    warning(
        'Unknown target system: ',
        host_machine.system(),
        ' - assumig shared dynamic libraries use \'.so\' suffix'
    )
    lib_suffix = '.so'
endif
lib_name = 'libextern' + lib_suffix

zig_target_args = []
if meson.is_cross_build()
    zig_target_args = ['-target', meson.get_external_property('zig_target')]
endif

zig_build_lib_wrapper = files('zig_build_lib_wrapper.py')
custom_target(
    'extern',
    input: [
        'pypkg/extern/bar.zig',
        'pypkg/extern/foo.c',
    ],
    output: lib_name,
    command: [
        py,
        zig_build_lib_wrapper,
        '-o',
        '@OUTPUT@',
        '--',
        zig_target_args,
        '--name',
        'extern',
        '-O',
        'ReleaseSafe',
        '-fstrip',
        '-I',
        meson.project_source_root() / 'pypkg' / 'extern',
        '-dynamic',
        '-lc',
        '@INPUT@'
    ],
    install: true,
    install_dir: py.get_install_dir() / 'pypkg',
)

# XXX: Resulting wheels need to be adjusted to ther target platform by calling:
# `wheel tags dist/*.whl --python-tag py3 --abi-tag none --platform-tag win_amd64`
