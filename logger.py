import colorama


def do_print(*args, flag=None, color=None, sep=' ', start='    ', nident=True):
    argv = []
    for x in args:
        argv.append(str(x))

    content = ''.join([flag, start, str(sep.join(argv)).replace('\n', str(
        str('\n'+' '*len(flag) if flag else 0) + start) if nident else '\n')]).strip()
    
    print(str('' if not color else color) + content +
          colorama.Back.RESET+colorama.Fore.RESET+colorama.Style.RESET_ALL)


def exception(exception):
    do_print(exception, flag='EXCEPTION', color=colorama.Fore.RED)


def log(*args, sep=' ', start='    ', nident=True, **kw):
    if kw:
        do_print(*args, str(kw), flag='LOG',
                 sep=sep, start=start, nident=nident)
    else:
        do_print(*args, flag='LOG', sep=sep, start=start, nident=nident, color=colorama.Style.DIM)

def info(*args, sep=' ', start='    ', nident=True, **kw):
    if kw:
        do_print(*args, str(kw), flag='INFO',
                 sep=sep, start=start, nident=nident, color=colorama.Fore.GREEN)
    else:
        do_print(*args, flag='INFO', sep=sep, start=start, nident=nident, color=colorama.Fore.GREEN)

def handled_exception(*args, sep=' ', start='    ', nident=True, **kw):
    if kw:
        do_print(*args, str(kw), flag='HANEX',
                 sep=sep, start=start, nident=nident)
    else:
        do_print(*args, flag='HANEX', sep=sep, start=start, nident=nident)


def hanex(*args,**kw):
    'A shorthand for handled_exception'
    handled_exception(*args,**kw)