from os import path

from PyPDF2 import PdfFileReader, PdfFileWriter


def main(combined_path):
    with open(combined_path, mode="rb") as combined_file:
        combined_pdf = PdfFileReader(combined_file)

        total_pages = combined_pdf.getNumPages()

        outfile_i = 0
        this_file_page_buffer = []

        for page_i in range(total_pages):
            p = combined_pdf.getPage(page_i)
            if len(p.extractText()) == 0:
                # blank page
                empty_buffer(this_file_page_buffer, outfile_i, combined_path)
                this_file_page_buffer = []
                outfile_i += 1
            else:
                this_file_page_buffer.append(p)

        empty_buffer(this_file_page_buffer, outfile_i, combined_path)


def empty_buffer(this_file_page_buffer, outfile_i, combined_path):
    out_filename = path.join(path.dirname(combined_path), f"split{outfile_i}.pdf")
    out_pdf = PdfFileWriter()
    for buffered_page in this_file_page_buffer:
        out_pdf.addPage(buffered_page)
    with open(out_filename, mode="wb") as out_file:
        out_pdf.write(out_file)


if __name__ == '__main__':
    main("/Users/cai/Desktop/combined test.pdf")
