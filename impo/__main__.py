from . import Doc, PageList
import argparse, gettext
_ = gettext.gettext

from typing import Tuple
from PyPDF2.utils import PdfReadError


def choose_k(n:int) -> int:
    for k in range(1, 9):
        pl = PageList(n, k)
        s = "[%d] %d " % (k, pl.booklets)
        s += _("booklets of") + " %d " % k + _("pages each")
        s += "\t(%d " % pl.blank + _("blank pages")+")"
        print(s)
    k = int(input(_("number of pages per booklet")+": "))
    return k


def str2doc(path:str) -> Doc:
    try:
        doc = Doc(path)
        return doc
    except PdfReadError as err:
        raise argparse.ArgumentTypeError(f'_("Error reading file"): {err}')


def str2span(strspan:str) -> Tuple[int, int]:
    try:
        span = strspan.split("-")
        return (int(span[0]), int(span[1]))
    except IndexError as e:
        raise ValueError(f'{_("Invalid span")} ({e})')

def main():
    import argparse
    parser = argparse.ArgumentParser(description=_(
        "impo is a program for impositioning documents"))
    parser.add_argument("input", metavar="in.pdf",
                        help=_("input file"), type=str2doc)
    parser.add_argument("output", nargs="?", metavar="out.pdf",
                        help=_("output file"), type=str)
    parser.add_argument("-k", metavar="n",
                        help=_("pages per booklet"), type=int)
    parser.add_argument("-s", metavar="span",
                        help=_("span of pages to include"), type=str2span)
    parser.add_argument(
        "-b", metavar="n", help=_("blank pages to insert before document"), type=int)
    parser.add_argument("-v", help=_("verbosity"), action="store_true")
    args = parser.parse_args()
    doc = args.input
    n = doc.n
    if args.k is not None:
        k = args.k
        if k < 1 or k > n // 4:
            raise ValueError(_("Invalid k"))
    else:
        k = choose_k(n)
    pl = PageList(n, k, args.b, args.s)
    print(doc, pl)
    print(f"Saving output file to {doc.output_file()}")
    doc.save(pl, args.output)
    print("Done!")

if __name__ == "__main__":
    main()
