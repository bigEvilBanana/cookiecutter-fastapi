from __future__ import print_function

import sys

WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

project_slug = "{{ cookiecutter.project_slug }}"
if hasattr(project_slug, "isidentifier"):
    assert (
        project_slug.isidentifier()
    ), "'{}' project slug is not a valid Python identifier.".format(project_slug)

assert (
        project_slug == project_slug.lower()
), "'{}' project slug should be all lowercase".format(project_slug)

assert (
        "\\" not in "{{ cookiecutter.author_name }}"
), "Don't include backslashes in author name."

python_major_version = sys.version_info[0]
if python_major_version == 2:
    print(
        WARNING + "You're running cookiecutter under Python 2, but the generated "
                  "project requires Python 3.8+."
    )
    sys.exit(1)
