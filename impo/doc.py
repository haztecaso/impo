from gettext import gettext as _
from os import path
from typing import Tuple

from PyPDF2 import PdfFileReader, PdfFileWriter

from .pagelist import PageList


class Doc:
    def __init__(self, ipath:str):
        self.path = ipath
        self.name = path.splitext(path.basename(self.path))[0]
        self.input_pdf = PdfFileReader(self.path, strict=False)
        self.n = self.input_pdf.getNumPages()
        self.__avg_page_size = None

    @property
    def avg_page_size(self) -> Tuple[int, int]:
        """Average page size"""
        if self.__avg_page_size is None:
            w, h = 0, 0
            for i in range(self.n):
                page = self.input_pdf.getPage(i)
                w += page.mediaBox[0]
                h += page.mediaBox[1]
            w /= self.n
            h /= self.n
            self.__avg_page_size = (w, h)
        return self.__avg_page_size

    def arrange(self, pl:PageList) -> PdfFileWriter:
        """Generates rearranged PdfFileWriter given a PageList object"""
        pdf_writer = PdfFileWriter()
        for i in pl.ordered_pages():
            if i == -1:
                pdf_writer.addBlankPage(*self.avg_page_size)
            else:
                page = self.input_pdf.getPage(i-1)
                pdf_writer.addPage(page)
        return pdf_writer

    def output_file(self, pl:PageList, filename:str=None) -> str:
        """Generates output filename"""
        if not filename:
            filename = f"{self.name}-impo-k{pl.k}.pdf" if pl.b == 0\
                  else f"{self.name}-impo-k{pl.k}b{pl.b}.pdf"
        return filename

    def save(self, pl:PageList, output_path:str=None) -> None:
        """Generates and saves new output_pdf given PageList object"""
        pdf_writer = self.arrange(pl)
        output_path = self.output_file(pl, output_path)
        outf = open(output_path, "wb+")
        pdf_writer.write(outf)

    def __str__(self):
        return f'{self.name} ({self.n} {_("pages")})'
