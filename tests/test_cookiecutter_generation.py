"""
Tests for project generation.
NOTE: run pytest with additional argument "--template ../"
"""
import os
import re

import pytest
import sh
from binaryornot.check import is_binary
from cookiecutter.exceptions import FailedHookException

PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)


@pytest.fixture
def context():
    return {
        "project_name": "My Test Project",
        "project_slug": "my_test_project",
        "author_name": "Test Author",
        "email": "test@example.com",
        "description": "A short description of the project.",
        "domain_name": "example.com",
        "version": "0.1.0",
        "timezone": "UTC",
    }


SUPPORTED_COMBINATIONS = [
    {"open_source_license": "MIT"},
    {"open_source_license": "BSD"},
    {"open_source_license": "GPLv3"},
    {"open_source_license": "Apache Software License 2.0"},
    {"open_source_license": "Not open source"},
    {"use_pycharm": "y"},
    {"use_pycharm": "n"},
    {"use_sentry": "y"},
    {"use_sentry": "n"},
    {"ci_tool": "None"},
    {"ci_tool": "Travis"},
    {"ci_tool": "Gitlab"},
    {"ci_tool": "Github"},
    {"debug": "y"},
    {"debug": "n"},
]


def _fixture_id(ctx):
    """Helper to get a user friendly test name from the parametrized context."""
    return "-".join(f"{key}:{value}" for key, value in ctx.items())


def build_files_list(root_dir):
    """Build a list containing absolute paths to the generated files."""
    return [os.path.join(dirpath, file_path) for dirpath, subdirs, files in os.walk(root_dir) for file_path in files]


def check_paths(paths):
    """Method to check all paths have correct substitutions."""
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(path):
            continue

        for line in open(path, "r"):
            match = RE_OBJ.search(line)
            assert match is None, f"cookiecutter variable not replaced in {path}"


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_project_generation(cookies, context, context_override):
    """Test that project is generated and fully rendered."""
    result = cookies.bake(extra_context={**context, **context_override})
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == context["project_slug"]
    assert result.project.isdir()

    paths = build_files_list(str(result.project))
    assert paths
    check_paths(paths)


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_flake8_passes(cookies, context_override):
    """Generated project should pass flake8."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.flake8(_cwd=str(result.project))
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_black_passes(cookies, context_override):
    """Generated project should pass black."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.black("--check", "--diff", "--exclude", "migrations", _cwd=str(result.project))
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


# TODO:  fix tests related to docker & CI
# @pytest.mark.parametrize(
#     ["use_docker", "expected_test_script"],
#     [
#         ("n", "pytest"),
#         ("y", "docker-compose -f local.yml run django pytest"),
#     ],
# )
# def test_travis_invokes_pytest(cookies, context, use_docker, expected_test_script):
#     context.update({"ci_tool": "Travis", "use_docker": use_docker})
#     result = cookies.bake(extra_context=context)
#
#     assert result.exit_code == 0
#     assert result.exception is None
#     assert result.project.basename == context["project_slug"]
#     assert result.project.isdir()
#
#     with open(f"{result.project}/.travis.yml", "r") as travis_yml:
#         try:
#             yml = yaml.safe_load(travis_yml)["jobs"]["include"]
#             assert yml[0]["script"] == ["flake8"]
#             assert yml[1]["script"] == [expected_test_script]
#         except yaml.YAMLError as e:
#             pytest.fail(str(e))


# @pytest.mark.parametrize(
#     ["use_docker", "expected_test_script"],
#     [
#         ("n", "pytest"),
#         ("y", "docker-compose -f local.yml run django pytest"),
#     ],
# )
# def test_gitlab_invokes_flake8_and_pytest(
#     cookies, context, use_docker, expected_test_script
# ):
#     context.update({"ci_tool": "Gitlab", "use_docker": use_docker})
#     result = cookies.bake(extra_context=context)
#
#     assert result.exit_code == 0
#     assert result.exception is None
#     assert result.project.basename == context["project_slug"]
#     assert result.project.isdir()
#
#     with open(f"{result.project}/.gitlab-ci.yml", "r") as gitlab_yml:
#         try:
#             gitlab_config = yaml.safe_load(gitlab_yml)
#             assert gitlab_config["flake8"]["script"] == ["flake8"]
#             assert gitlab_config["pytest"]["script"] == [expected_test_script]
#         except yaml.YAMLError as e:
#             pytest.fail(e)
#
#
# @pytest.mark.parametrize(
#     ["use_docker", "expected_test_script"],
#     [
#         ("n", "pytest"),
#         ("y", "docker-compose -f local.yml run django pytest"),
#     ],
# )
# def test_github_invokes_linter_and_pytest(
#     cookies, context, use_docker, expected_test_script
# ):
#     context.update({"ci_tool": "Github", "use_docker": use_docker})
#     result = cookies.bake(extra_context=context)
#
#     assert result.exit_code == 0
#     assert result.exception is None
#     assert result.project.basename == context["project_slug"]
#     assert result.project.isdir()
#
#     with open(f"{result.project}/.github/workflows/ci.yml", "r") as github_yml:
#         try:
#             github_config = yaml.safe_load(github_yml)
#             linter_present = False
#             for action_step in github_config["jobs"]["linter"]["steps"]:
#                 if action_step.get("uses", "NA").startswith("pre-commit"):
#                     linter_present = True
#             assert linter_present
#
#             expected_test_script_present = False
#             for action_step in github_config["jobs"]["pytest"]["steps"]:
#                 if action_step.get("run") == expected_test_script:
#                     expected_test_script_present = True
#             assert expected_test_script_present
#         except yaml.YAMLError as e:
#             pytest.fail(e)


@pytest.mark.parametrize("slug", ["project slug", "Project_Slug"])
def test_invalid_slug(cookies, context, slug):
    """Invalid slug should failed pre-generation hook."""
    context.update({"project_slug": slug})

    result = cookies.bake(extra_context=context)

    assert result.exit_code != 0
    assert isinstance(result.exception, FailedHookException)
