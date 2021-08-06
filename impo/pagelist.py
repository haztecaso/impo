from math import ceil, log
from typing import Tuple

import gettext
_ = gettext.gettext

# Span utilities
def check_span(span, n): return span[0] > 0 and span[1] <= n
def spanSize(span): return span[1] - span[0] + 1

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

    def __init__(self, n:int, k:int=4, b:int=0, span:Tuple[int, int]=None):
        """
        Constructor arguments:
            n       number of document pages
            k       number of paper pages per booklet
            b       number of blank pages to insert before document
            span    span of pages to include   
        """
        if span:
            if check_span(span, n):
                self.span = span
                self.n = spanSize(span)
            else:
                raise IndexError(_("Span out of range"))
        else:
            self.span = (1, n)  # Default span
            self.n = n
        self.k = k
        if b is None:
            b = 0
        self.b = b % (self.k*4)
        self.booklets = ceil((self.n+self.b)/self.k/4)
        self.N = self.booklets*4*self.k
        self.pages = [-1]*self.b + \
            [*range(self.span[0], self.span[1]+1)] + \
            [-1]*(4*self.k*self.booklets-self.n)
        self.blank = self.b + 4*self.k*self.booklets - self.n

    def order(self) -> list:
        """Order indices for a booklet with 4*self.k pages."""
        l = [*range(1, 4*self.k+1)]
        l = [l.pop(i % 4//2-1)-1 for i in l*1]
        result = []
        for i in range(self.booklets):
            result += [4*self.k*i + j for j in l]
        return result

    def ordered_pages(self) -> list:
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
