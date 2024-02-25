project('purelib-and-platlib', 'c')

py = import('python').find_installation(pure: false)

py.extension_module(
    'our_first_module',
    'our_first_module.c',
    install: true,
)
