import setuptools

_requires = [
    'setuptools-scm',
    'ebs-linuxnode-gui-kivy-core>=2.0',
    # ebs Widgets
    'kivy_garden.ebs.core',
    'kivy_garden.ebs.cefkivy>=66.0.13',
]

setuptools.setup(
    name='ebs-linuxnode-gui-kivy-netconfig',
    url='https://github.com/ebs-universe/ebs-linuxnode-kivy-netconfig',

    author='Chintalagiri Shashank',
    author_email='shashank.chintalagiri@gmail.com',

    description='NetConfig integration for interactive EBS Linuxnode Kivy Applications',
    long_description='',

    packages=setuptools.find_packages(),

    package_dir={'ebs.linuxnode.gui.kivy.netconfig': 'ebs/linuxnode/gui/kivy/netconfig'},

    package_data={'ebs.linuxnode.gui.kivy.netconfig': ['images/settings.png',
                                                       'images/close.png']},

    install_requires=_requires,

    setup_requires=['setuptools_scm'],
    use_scm_version=True,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
    ],
)
