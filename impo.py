#!/bin/env python3
import math
from os import path
from PyPDF2 import PdfFileReader, PdfFileWriter

import gettext 
_ = gettext.gettext

# Span utilities
defaultSpan = lambda n : (1,n)
checkSpan = lambda span, n: span[0]>0 and span[1] <= n
spanSize = lambda span: span[1] - span[0] + 1

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
    def __init__(self, n, k=4, b=0, span=None):
        """
        Constructor arguments:
            n       number of document pages
            k       number of paper pages per booklet
            b       number of blank pages to insert before document
            span    span of pages to include   
        """
        if span:
            if checkSpan(span, n):
                self.span = span
                self.n = spanSize(span)
            else:
                raise IndexError(_("Invalid span"))
        else:
            self.span = defaultSpan(n)
            self.n = n
        self.k = k
        self.b = b%(self.k*4)
        self.booklets = math.ceil((self.n+self.b)/self.k/4)
        self.N = self.booklets*4*self.k
        self.pages = [-1]*self.b + \
                [*range(self.span[0],self.span[1]+1)] + \
                [-1]*(4*self.k*self.booklets-self.n)
        self.blank = self.b + 4*self.k*self.booklets - self.n

    def order(self) -> list:
        """Order indices for a booklet with 4*self.k pages."""
        l = [*range(1,4*self.k+1)]
        l = [l.pop(i%4//2-1)-1 for i in l*1]
        result = []
        for i in range(self.booklets):
            result += [4*self.k*i + j for j in l]
        return result

    def orderedPages(self) -> list:
        """List page numbers in booklet order. Empty pages are represented with -1."""
        return [self.pages[i] for i in self.order()]
    
    def __repr__(self):
        pages = self.orderedPages()
        result = ""
        for i in range(self.booklets * self.k):
            p = [*map(lambda n: "()" if n<0 else n, pages[4*i:4*i+4])]
            result += "%s\t%s\t%s\t%s \n" % (p[0], p[1], p[2], p[3])
            result += "\n" if (i>0 and (not (i+1)%self.k)) else ""
        tabw = math.ceil(math.log(self.N,10))+1
        return result.expandtabs(tabw)

    def __str__(self):
        result = _("_N_ booklets of _K_ pages each.")+"\n\n"
        result = result.replace("_N_",str(self.booklets))
        result = result.replace("_K_",str(self.k))
        if(self.booklets <= 2):
            result +="Booklets:\n%s" % repr(self)
            return result
        lines = repr(self).splitlines()
        result += _("First booklet:")+"\n"
        for i in range(self.k):
            result += "%s \n" % lines[i]
        result += "\n[%d " % (self.booklets - 2)
        result += _("booklets") + "]\n\n"
        result += _("Last booklet")+"\n"
        for i in reversed(range(self.k)):
            result += "%s \n" % lines[-(i+2)]
        return result

class Doc:
    def __init__(self, path):
        self.path = path
        try:
            self.input_pdf = PdfFileReader(self.path, strict=False)
            self.n = self.input_pdf.getNumPages()
        except Exception as e:
            raise ValueError(_("Error reading file") + " (%s)" % e)

    def pathname(self):
        """
        input file name without extension
        """
        return path.splitext(path.basename(self.path))[0]

    def avgPageSize(self):
        """
        Calc average page size of input document.
        """
        result = [0, 0]
        for i in range(self.n):
            page = self.input_pdf.getPage(i)
            result[0] += page.mediaBox[0]
            result[1] += page.mediaBox[1]
        result[0] /= self.n
        result[1] /= self.n
        return result

    def save(self, pl):
        """
        Generates and saves new output_pdf given PageList object 
        """
        output_pdf = PdfFileWriter()
        (w, h) = self.avgPageSize()
        for i in pl.orderedPages():
            if i == -1:
                output_pdf.addBlankPage(w, h)
            else:
                page = self.input_pdf.getPage(i-1)
                output_pdf.addPage(page)

        outf = open( "out.pdf", "wb+" )
        output_pdf.write(outf)
        return output_pdf

    def __str__(self):
        result = self.pathname()+" ("
        result += "%s " % self.n
        result += _("pages") + ")"
        return result

def ks(n):
    for k in range(1,9):
        pl = PageList(n,k)
        s = "[%d] %d " % (k, pl.booklets)
        s+= _("booklets of") + " %d " % k + _("pages each")
        s+="\t(%d " % pl.blank + _("blank pages")+")"
        print(s)

if __name__ == "__main__":
    book = Doc("./test.pdf")
    ks(book.n)
    k = int(input(_("number of pages per booklet")+": "))
    pl = PageList(book.n,k)
    print(pl)
    book.save(pl)
