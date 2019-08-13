import os
import wx
import fitz
from PyPDF2 import PdfFileReader, PdfFileWriter

class APDFTool:
    def __init__(self, files):
        if files == None:
            self.files = []
        self.files = files
        pass

    def writePDF(self, pages, name):
        if pages == None or len(pages) == 0:
            return
        if name == None or name == "":
            name = "temp"
        writer = PdfFileWriter()
        for page in pages:
            writer.addPage(page)
        writer.write(open(name+'.pdf', 'wb'))

    def split(self, pos):
        if self.files == None or len(self.files) == 0:
            return
        for file in self.files:
            reader = PdfFileReader(file)
            pages = []
            pages2 = []
            pageCount = reader.getNumPages()
            name = os.path.basename(file)
            for idx in range(pos):
                page = reader.getPage(idx)
                pages.append(page)
            for idx in range(pos, pageCount):
                page = reader.getPage(idx)
                pages2.append(page)
            self.writePDF(pages, name+"1")
            self.writePDF(pages2, name+"2")

    def getTotalPageCount(self):
        totalPageCount = 0
        for file in self.files:
            reader = PdfFileReader(file)
            totalPageCount = totalPageCount + reader.getNumPages()

        return totalPageCount

    def merge(self, name, callback):
        processCount = 0
        writer = PdfFileWriter()
        for file in self.files:
            reader = PdfFileReader(file)
            pageCount = reader.getNumPages()

            for pageIndex in range(pageCount):
                page = reader.getPage(pageIndex)
                writer.addPage(page)
                processCount = processCount + pageIndex + 1
                callback(processCount)

        writer.write(open(name, 'wb'))

    def toImages(self):
        if self.files is None or len(self.files) == 0:
            return
        images = []
        for file in self.files:
            doc = fitz.open(file)
            pageNum = len(doc)
            for idx in range(pageNum):
                dl = doc[idx]
                rato = 0.24
                pix = dl.getPixmap(matrix = fitz.Matrix(rato, rato), alpha = False)
                bmp = wx.Bitmap.FromBuffer(pix.w, pix.h, pix.samples)
                images.append(bmp)

        return images
