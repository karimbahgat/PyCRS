
import doctest
import sys

def test(**kwargs):
    doctest.NORMALIZE_WHITESPACE = 1
    verbosity = kwargs.get('verbose', 0)
    if verbosity == 0:
        print('Running doctests...')

    # ignore py2-3 unicode differences
    import re
    class Py23DocChecker(doctest.OutputChecker):
        def check_output(self, want, got, optionflags):
            if sys.version_info[0] == 2:
                got = re.sub("u'(.*?)'", "'\\1'", got)
                got = re.sub('u"(.*?)"', '"\\1"', got)
            res = doctest.OutputChecker.check_output(self, want, got, optionflags)
            return res
        def summarize(self):
            doctest.OutputChecker.summarize(True)

    # run tests
    runner = doctest.DocTestRunner(checker=Py23DocChecker(), verbose=verbosity)
    import pycrs
    doc = pycrs.__doc__
    test = doctest.DocTestParser().get_doctest(string=doc, globs={}, name="__init__", filename="__init__.py", lineno=0)
    failure_count, test_count = runner.run(test)

    # print results
    if verbosity:
        runner.summarize(True)
    else:
        if failure_count == 0:
            print('All test passed successfully')
        elif failure_count > 0:
            runner.summarize(verbosity)

    return failure_count

if __name__ == '__main__':
    failure_count = test()
    sys.exit(failure_count)


