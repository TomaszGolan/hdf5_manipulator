"""printing info, warnings, errors in different colors"""

VIOLET = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'


def _print(text, indent, color):

    """print text in given color, preceded by given #tabs

    Keyword arguments:
    text -- text to print
    indent -- no. of tabs
    color -- text color defined by global variables
    """

    if indent:
        print '\t' * indent,
    print color + text + END


def info(text, indent=None):

    """precede text with 'INFO' and call _print with GREEN color"""

    _print("\nINFO: " + text, indent, GREEN)


def warning(text, indent=None):

    """precede text with 'WARNING' and call _print with YELLOW color"""

    _print("\nWARNING: " + text + "\n", indent, YELLOW)


def error(text, indent=None):

    """precede text with 'ERROR' and call _print with RED color"""

    _print("\nERROR: " + text + "\n", indent, RED)


def box(text, width=80):

    """'draw box' and print text in the center (using BOLD font)"""

    print BLUE
    pad = (width - len(text)) / 2
    print '+' + '-' * width + '+'
    print '|' + ' ' * width + '|'
    print '|' + ' ' * pad + text + ' ' * (width - pad - len(text)) + '|'
    print '|' + ' ' * width + '|'
    print '+' + '-' * width + '+'
    print END
