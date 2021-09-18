#!/usr/bin/env python3

import sys
from PyPDF2 import PdfFileWriter, PdfFileReader

def width(page):
    box = page.mediaBox
    return box.lowerRight[0] - box.lowerLeft[0]

def height(page):
    box = page.mediaBox
    return box.upperLeft[1] - box.lowerLeft[1]

def booklet(in_file, out_file):
    in_pdf = PdfFileReader(open(in_file, 'rb'))
    out_pdf = PdfFileWriter()

    n = in_pdf.numPages // 2
    for i in range(n):
        print('page {}/{}'.format(i+1,n))
        a = i
        b = 2*n - i - 1
        if i % 2 == 0:
            a, b = b, a
        page_a = in_pdf.getPage(a)
        page_b = in_pdf.getPage(b)
        w_a = width(page_a)
        w_b = width(page_b)
        h_a = height(page_a)
        h_b = height(page_b)
        w = w_a + w_b
        h = max(h_a, h_b)
        page_out = out_pdf.addBlankPage(w, h)
        page_out.mergeTranslatedPage(page_a,0,0)
        page_out.mergeTranslatedPage(page_b,w_a,0)

    with open(out_file, 'wb') as f:
        out_pdf.write(f)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: python3 booklet.py <in_file> <out_file>')
        sys.exit(1)
    booklet(*sys.argv[1:])
