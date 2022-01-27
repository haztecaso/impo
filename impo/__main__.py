"""
Usage:
  impo [options] <input_file> [<output_file>]

Options:
  -h --help       Show this screen.
  --version       Show version.
  -s, --span int  Span of pages to include [default: all]
  -k int          Number of pages per booklet
  -b int          Number of blank pages to insert before document [default: 0]
  -v              Verbose mode
"""

from gettext import gettext as _

from docopt import docopt

from .doc import Doc
from .pagelist import PageList
from .span import str2span


def choose_k(n:int) -> int:
    for k in range(1, min(n // 4, 9)):
        pl = PageList(n, k)
        s = "[%d] %d " % (k, pl.booklets)
        s += _("booklets of") + " %d " % k + _("pages each")
        s += "\t(%d " % pl.blank + _("blank pages")+")"
        print(s)
    k = int(input(_("number of pages per booklet")+": "))
    return k


def main():
    args = docopt(__doc__, version="impo v2.1.1")
    doc = Doc(args['<input_file>'])
    if args['-k'] is not None:
        args['-k'] = int(args['-k'])
        if args['-k'] < 1 or args['-k'] > doc.n // 4:
            raise ValueError(_("Invalid k"))
    else:
        args['-k'] = choose_k(doc.n)
    args['--span'] = None if args['--span'] == "all" else str2span(args['--span'])
    args['-b'] = int(args['-b'])

    pl = PageList(doc.n, args['-k'], args['-b'], args['--span'])
    print(doc, pl)
    print(f"Saving output file to {doc.output_file(pl)}")

    doc.save(pl, args['<output_file>'])
    print("Done!")

if __name__ == "__main__":
    main()
