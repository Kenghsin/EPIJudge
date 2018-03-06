# @library
import collections
import os
import re

from test_framework.test_failure import TestFailure, PropertyName


def split_tsv_file(tsv_file):
    ROW_DELIM = '\n'
    FIELD_DELIM = '\t'

    try:
        with open(tsv_file) as input_data:
            return [
                row.replace(ROW_DELIM, '').split(FIELD_DELIM)
                for row in input_data
            ]
    except OSError:
        raise RuntimeError('Test data file not found')


def get_default_test_data_dir_path():
    MAX_SEARCH_DEPTH = 4
    ENV_KEY = 'EPI_TEST_DATA_DIR'
    DIR_NAME = 'test_data'

    env_result = os.getenv(ENV_KEY, '')
    if env_result:
        if not os.path.isdir(env_result):
            raise RuntimeError(
                '{} environment variable is set to "{}", but it\'s not a directory'
                .format(ENV_KEY, env_result))
        return env_result

    path = DIR_NAME
    for _ in range(MAX_SEARCH_DEPTH):
        if os.path.isdir(path):
            return path
        path = os.path.join(os.path.pardir, path)

    raise RuntimeError(
        'Can\'t find test data directory. Specify it with {} environment variable (you may need to restart PC) or '
        'start the program with "--test_data_dir <path>" command-line option'.
        format(ENV_KEY))


def filter_bracket_comments(s):
    """
    Serialized type name can contain multiple comments, enclosed into brackets.
    This function removes all such comments.
    """
    bracket_enclosed_comment = r"(\[[^\]]*\])"
    return re.sub(bracket_enclosed_comment, '', s, 0).replace(' ', '')


def assert_all_values_present(reference, result):
    reference_set = collections.defaultdict(int)

    for x in reference:
        reference_set[x] += 1

    for x in result:
        reference_set[x] -= 1

    flatten = lambda l: [item for sublist in l for item in sublist]
    excess_items = flatten(
        [x] * -count for x, count in reference_set.items() if count < 0)
    missing_items = flatten(
        [x] * count for x, count in reference_set.items() if count > 0)

    if excess_items or missing_items:
        e = TestFailure('Value set changed')\
            .with_property(PropertyName.RESULT, result)
        if excess_items:
            e.with_property(PropertyName.EXCESS_ITEMS, excess_items)
        if missing_items:
            e.with_property(PropertyName.MISSING_ITEMS, missing_items)
        raise e


def completely_sorted(x):
    """Multi-dimensional container sort.

    If x is list of lists of ... of lists,
    then the argument is lexicographically sorted on all levels,
    starting from the bottom.
    """
    if isinstance(x, list):
        return sorted(completely_sorted(e) for e in x)
    else:
        return x


def unordered_compare(a, b):
    """Compares elements of 2 (multi-dimensional) list."""
    return completely_sorted(a) == completely_sorted(b)


def has_executor_hook(func):
    return hasattr(func, 'executor_hook') and func.executor_hook


def enable_executor_hook(func):
    func.executor_hook = True
    return func


def enable_timer_hook(func):
    raise RuntimeError("This program uses deprecated timer_hook")
