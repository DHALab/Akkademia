import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="akkadian",
    version="1.0.2",
    author="Ariel Elazary, Gai Gutherz",
    author_email="am.elazary@gmail.com, gaigutherz@gmail.com",
    description="Translating Akkadian signs to transliteration using NLP algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaigutherz/Translating-Akkadian-using-NLP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={'akkadian': ["output/bilstm_model.pkl", "output/memm_model.pkl", "output/hmm_model.pkl"]},
    install_requires=[
        'allennlp==0.8.5',
    ],
)