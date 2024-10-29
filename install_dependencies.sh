pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade build
python -m build
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade --editable .