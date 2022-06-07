import sys

import cpplint


class ErrorCollector(object):
    # These are a global list, covering all categories seen ever.
    _ERROR_CATEGORIES = cpplint._ERROR_CATEGORIES
    _SEEN_ERROR_CATEGORIES = {}

    def __init__(self):
        """assert_fn: a function to call when we notice a problem."""
        self._errors = []
        self._count = 0
        cpplint.ResetNolintSuppressions()

    def __call__(self, unused_filename, linenum,
                 category, confidence, message):
        self._SEEN_ERROR_CATEGORIES[category] = 1
        if cpplint._ShouldPrintError(category, confidence, linenum):
            if confidence > 2:
                self._errors.append([])
                self._errors[self._count].append('%d' % (linenum))
                self._errors[self._count].append('%s' % message)
                self._count += 1

    def results(self):
        if len(self._errors) < 2:
            return ''.join(self._errors)  # Most tests expect to have a string.
        else:
            return self._errors  # Let's give a list if there is more than one.

    def result_list(self):
        return self._errors

    def verify_all_categories_are_seen(self):
        for category in self._ERROR_CATEGORIES:
            if category not in self._SEEN_ERROR_CATEGORIES:
                sys.exit('FATAL ERROR: There are no tests for category "%s"' % category)

    def remove_if_present(self, substr):
        for (index, error) in enumerate(self._errors):
            if error.find(substr) != -1:
                self._errors = self._errors[0:index] + self._errors[(index + 1):]
                break


def perform_multiline_lint(code):
    error_collector = ErrorCollector()
    lines = code.split('\n')
    cpplint.RemoveMultiLineComments('main.cpp', lines, error_collector)
    lines = cpplint.CleansedLines(lines)
    nesting_state = cpplint.NestingState()

    for i in range(lines.NumLines()):
        nesting_state.Update('main.cpp', lines, i, error_collector)
        cpplint.CheckStyle('main.cpp', lines, i, 'cpp', nesting_state, error_collector)
        cpplint.CheckForNonStandardConstructs('main.cpp', lines, i, nesting_state, error_collector)
    nesting_state.CheckCompletedBlocks('main.cpp', error_collector)

    return error_collector.result_list()
