from setuptools import setup


def main():
    setup(
        package_dir={'': 'src'},
        packages=['blurring'],
        include_package_data=True,
        use_scm_version=True,
        install_requires=[
            'ffmpeg-python',
            'opencv-python',
            'numpy'
        ],
        setup_requires=[
            'setuptools_scm',
        ],
        entry_points={
            'console_scripts': [
                'blurring=blurring.cli:create_blurred_video',
                'blurring-t=blurring.cli:create_template',
            ],
            'wmc.register_setup': [
                'blurring=blurring.hook:setup',
            ],
            'wmc.register_main': [
                'blurring=blurring.hook:main',
            ],
        },
    )


if __name__ == '__main__':
    main()
