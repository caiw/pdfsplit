from os import path

from PyPDF2 import PdfFileReader, PdfFileWriter
from gooey import Gooey, GooeyParser


@Gooey(program_name="PDF Splitter",
       program_description="Split a PDF on its blank pages. Segments will be saved in the same directory as the "
                           "original file.")
def main():
    parser = GooeyParser()
    parser.add_argument("path",
                        type=str,
                        widget='FileChooser',
                        # title="Combined PDF file."
                        )

    args = parser.parse_args()

    combined_path = args.path

    print(f"Loading \"{path.basename(combined_path)}\"...")
    print(f"Splitting on blank pages...")

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
    out_filename = path.join(path.dirname(combined_path),
                             f"{path.splitext(path.basename(combined_path))[0]} split {outfile_i:02}.pdf")
    if path.isfile(out_filename):
        raise FileExistsError(f"Tried to save file {path.basename(out_filename)} but it already exists. Please delete "
                              f"or move so it doesn't get overwrittn.")
    out_pdf = PdfFileWriter()
    for buffered_page in this_file_page_buffer:
        out_pdf.addPage(buffered_page)
    print(f"Saving split pdf \"{path.basename(out_filename)}\"...")
    with open(out_filename, mode="wb") as out_file:
        out_pdf.write(out_file)


if __name__ == '__main__':
    main()
