import os
from decimal import Decimal
from pathlib import Path

from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
from PyPDF2.generic import AnnotationBuilder

from pdfeditor.file_manager import FileManager


class AddPagination(FileManager):
    def __init__(self, read_name=None, write_name=None, write_folder=None):
        super().__init__(read_name, write_name)
        self.TAG = "AddPagination"
        self.write_folder = write_folder

    @property
    def write_folder(self):
        return self._write_folder

    @write_folder.setter
    def write_folder(self, value):
        self._write_folder = Path(os.getcwd()) / '..' / 'output' / (str(value))
        print(self.TAG, "Field _write_folder: ", self._write_folder)

    def create_folder(self):
        pass

    def add_description(self):
        self.description = '给pdf的每一页都添加上页码！'

    def add_pagination(self):
        # print(self.TAG, "add_pagination<>")
        reader = PdfReader(str(self.read_dir))
        output_file_path = str(self.write_folder / (str(self.write_dir) + '.pdf'))

        writer = PdfWriter()
        pagination = paginationStart
        number = 0
        for page in reader.pages:
            writer.add_page(page)
            if pagination > 0:
                free_text = self.make_annotation(page, pagination)
                writer.add_annotation(page_number=number, annotation=free_text)
            pagination += 1
            number += 1

        with open(output_file_path, mode="wb") as output:
            writer.write(output)
        print(self.TAG, "[INFO]: Added pagination ", number, " page(s) for pdf file ", self.read_dir)
        print(self.TAG, "[INFO]: Output file path is ", output_file_path)

    def make_annotation(self, page, pagination):
        # print(self.TAG, "make_annotation<> pagination: ", pagination)
        media_box = page.mediabox
        x1, y1 = media_box.width * Decimal(0.92), media_box.height * Decimal(1 - 0.92 - 0.02)
        x2, y2 = media_box.width * Decimal(0.92 + 0.04), media_box.height * Decimal(1 - 0.92)
        free_text = AnnotationBuilder.free_text(
            text=str(pagination),
            rect=(x1, y1, x2, y2),
            font="Helvetica",
            bold=True,
            italic=True,
            font_size="14pt",
            font_color="000000",
            border_color="000000",
            background_color="ffffff",
        )
        return free_text

    def implement(self):
        # self.write_folder = str(input("输入保存的文件的名字："))
        # self.create_folder()
        self.add_pagination()


if __name__ == '__main__':
    input_file_name = "text"
    pdf = AddPagination(input_file_name, input_file_name + "_pagination_added", '')
    paginationStart = -12  # -12
    print(pdf.description)
    pdf.implement()
