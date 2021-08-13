from math import ceil, log
from gettext import gettext as _
from typing import List

from .span import Span

def booklet_order(k:int) -> List[int]:
    l = [*range(1, 4*k+1)]
    return [l.pop(i % 4//2-1)-1 for i in l*1]


class PageList:
    """
    Class for ordering pages for booklets.
    Attributes:
        n           number of document pages
        k           number of paper pages per booklet
        b           number of blank pages to insert before document
        span        span of pages to include
        booklets    number of booklets
        N           total number of pages (document + empty)
        pages       list with page numbers. Empty pages are represented with -1.
        blank       total number of blank pages (before and after)
    """

    def __init__(self, n:int, k:int=4, b:int=0, span:Span=None):
        """
        Constructor arguments:
            n       number of document pages
            k       number of paper pages per booklet
            b       number of blank pages to insert before document
            span    span of pages to include
        """
        if span:
            span.validate(n)
            self.span = span
            self.n = self.span.size
        else:
            self.span = Span(1, n)  # Default span
            self.n = n
        self.k = k
        if b is None:
            b = 0
        self.b = b % (self.k*4)
        self.booklets = ceil((self.n+self.b)/self.k/4)
        self.N = self.booklets*4*self.k
        self.pages = [-1]*self.b + \
            [*range(self.span.start, self.span.end+1)] + \
            [-1]*(4*self.k*self.booklets-self.n)
        self.blank = self.b + 4*self.k*self.booklets - self.n

    def order(self) -> List[int]:
        """Order indices for a booklet with 4*self.k pages"""
        result = []
        for i in range(self.booklets):
            result += [4*self.k*i + j for j in booklet_order(self.k)]
        return result

    def ordered_pages(self) -> List[int]:
        """List page numbers in booklet order. Empty pages are represented with -1."""
        return [self.pages[i] for i in self.order()]

    def __repr__(self):
        pages = self.ordered_pages()
        result = ""
        for i in range(self.booklets * self.k):
            p = [*map(lambda n: "()" if n < 0 else n, pages[4*i:4*i+4])]
            result += f'{p[0]}\t{p[1]}\t{p[2]}\t{p[3]}\n'
            result += "\n" if (i > 0 and (not (i+1) % self.k)) else ""
        return result.expandtabs(ceil(log(self.N, 10))+1)

    def __str__(self):
        result = _("_N_ booklets of _K_ pages each.")+"\n\n"
        result = result.replace("_N_", str(self.booklets))
        result = result.replace("_K_", str(self.k))
        if(self.booklets <= 2):
            result += f"Booklets:\n {repr(self)}"
            return result
        lines = repr(self).splitlines()
        result += _("First booklet:")+"\n"
        for i in range(self.k):
            result += f"{lines[i]} \n"
        result += f'\n[{self.booklets -2} {_("booklets")}]\n\n'
        result += f'{_("Last booklet:")}\n'
        for i in reversed(range(self.k)):
            result += f"{lines[-(i+2)]}\n"
        return result
