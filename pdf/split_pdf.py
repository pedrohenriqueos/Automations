from PyPDF2 import PdfFileReader, PdfFileWriter
import sys


def split_pdf(file_pdf):
	pdf = PdfFileReader(file_pdf)
	pages = pdf.getNumPages()
	for p in range(pages):
		page = pdf.getPage(p)
		pdf_writer = PdfFileWriter()
		pdf_writer.addPage(page)
		output = 'pg'+str(p+1)+'.pdf'
		with open(output ,'wb') as output_pdf:
			pdf_writer.write(output_pdf)

if __name__=='__main__':
	pdf = sys.argv[1]
	split_pdf(pdf)	
