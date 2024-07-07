import os
from pathlib import Path

from PyPDF2 import PdfWriter, PdfReader

from pdfeditor.file_manager import FileManager


class RangeSplit(FileManager):
    def __init__(self, read_name=None, write_name=None, write_folder=None):
        super().__init__(read_name, write_name)
        self.TAG = "RangeSplit"
        self.write_folder = write_folder
        # self.description = 'Split All Pages into Small Files'

    @property
    def write_folder(self):
        return self._write_folder

    @write_folder.setter
    def write_folder(self, value):
        self._write_folder = Path(os.getcwd()) / '..' / 'output' / (str(value))
        print(self.TAG, "Field _write_folder: ", self._write_folder)

    @property
    def write_dir(self):
        return self._write_dir

    @write_dir.setter
    def write_dir(self, value):
        self._write_dir = value

    def add_description(self):
        self.description = '按照页面范围从pdf文档中提取内容，并保存！'

    def create_folder(self):
        if not os.path.exists(str(self.write_folder)):
            os.mkdir(str(self.write_folder))
        print("Create dir ", self.write_folder, " result: ", os.path.exists(str(self.write_folder)))

    def split_pdf(self):
        if os.path.exists(self.read_dir) and os.path.isfile(self.read_dir):
            pass
        else:
            print("[ERR]: Input file not exist or not a file, please check before run again! path: ", self.read_dir)
            return
        reader = PdfReader(str(self.read_dir))
        # in this case self.write_dir is the pdf name
        raw = str(self.write_folder / (str(self.write_dir) + '.pdf'))

        output_file_path = str(self.write_folder / (str(self.write_dir) + '.pdf'))
        writer = PdfWriter()
        number = 1
        for page in reader.pages:
            if startPage <= number <= endPage:
                writer.add_page(page)
            number += 1

        with open(output_file_path, mode="wb") as output:
            writer.write(output)



    def implement(self):
        # self.write_folder = str(input('输出文件路径: '))
        # self.create_folder()
        self.split_pdf()


if __name__ == '__main__':
    # input_file_name = str(input('PDF源文件名字: '))
    input_file_name = "text"
    pdf = RangeSplit(input_file_name, input_file_name + "_section_01", '')
    print(pdf.description)
    startPage = 3
    endPage = 156
    pdf.implement()
    print("run Complete!")
