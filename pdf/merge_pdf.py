from PyPDF2 import PdfFileReader, PdfFileWriter
import sys

# A ordem do input será a ordem dos merges

def merge_pages(files_pdf):
	pdf_writer = PdfFileWriter()
	for file_pdf in files_pdf:
		pdf = PdfFileReader(file_pdf)
		pages = pdf.getNumPages()
		for p in range(pages):
			page = pdf.getPage(p)
			pdf_writer.addPage(page)
	with open('merge.pdf','wb') as fh: #name file
		pdf_writer.write(fh)

if __name__ == '__main__':
	pdfs = []
	for arg in sys.argv:
		pdfs.append(arg)
	pdfs = pdfs[1:]
	merge_pages(pdfs)
	'''
	pdfs = open('list_files.txt','r').read()[:-1].split(' ')
	merge_pages(pdfs)
	'''
