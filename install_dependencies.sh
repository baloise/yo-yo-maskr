alias pip-install='pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org'
pip-install --upgrade build
python -m build
pip-install --upgrade --editable .