# meson-python-zig

This is an example Python package using [meson-python](https://meson-python.readthedocs.io/en/latest/)
with [zig](https://ziglang.org/) which allows **easy cross compilation** of shared libraries,
bundled with Python packages, to be used with Python's builtin [ctypes](https://docs.python.org/3/library/ctypes.html)
module.

Provided that you have zig and llvm (for llvm-strip executable) installed,
`python -m build` will automatically build the source distribution and wheel for your current platform.
Cross compilation boils down two executing two commands:
- Passing the cross-compilation file down to meson, e.g.:
    `python -m build -w "-Csetup-args=--cross-file=$PWD/cross/aarch64-linux-musl.ini"`
- Fixing the tags of the produced wheel. [meson-python always tags the wheel as-if it was
    compiled for the host platform](https://github.com/mesonbuild/meson-python/discussions/580). Use `wheel tags`, e.g.:
    `wheel tags dist/pypkg-0.0.1-cp311-cp311-linux_x86_64.whl --python-tag py3 --abi-tag none --platform-tag musllinux_1_1_aarch64`

## Using `shared_library` instead of `custom_target`

The current meson.build file uses `custom_target` to invoke `zig build-lib`.
This allows mixing and matching C, C++ and Zig source files and more granular control over
compile options. However, it's possible to greatly simplify the config if you only use C sources by
invoking `shared_library`.

See [the repository before zig build-lib introduction](https://github.com/MKuranowski/meson-python-zig/tree/fb2831a6e751c11bf6b47595a6ee4d688566bf3f).
The TL;DR is that:
1. `zig_build_lib_wrapper.py` is not needed
2. `zig_target` property is not needed in meson cross files
    (the whole `[properties]` section can be removed)
3. `meson.build` simplified to:
    ```meson
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
        [
            'pypkg/extern/bar.c',
            'pypkg/extern/foo.c',
        ],
        install: true,
        install_dir: py.get_install_dir() / 'pypkg',
    )
    ```

This simplification should also be possible with C++, provided a similar wrapper
to `zig_cc_wrapper.py` is provided (invoking `zig c++`) and it's defined in the cross files.

## Building Python extensions

I have not tried using `zig cc` to compile Python extensions. Simple shared libraries cover
my use case, are easier to write (no need to deal with the Python C API) and don't need to be
recompiled against multiple Python versions. In principle the wrappers and cross files here
would help with cross-compiling extensions, however – you'd need to find another way to
compile against different Python versions. I'm also not sure about linking.
