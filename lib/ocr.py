from PyPDF2 import PdfFileReader


def ocr_core(filename):
    with open(filename, 'rb') as f:
        print(filename)
        pdf = PdfFileReader(f)

        # get the first page
        #page = pdf.getPage(1)
        #print(page)
        #print('Page type: {}'.format(str(type(page))))
        page = pdf.getPageNumber()
        print(page)
        #text = page.extractText()
        #print(text)
