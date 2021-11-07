
import unittest

from header_parser import HeaderParser
from file_reading import FileReading

class TestHeadPars(unittest.TestCase):    # наследуемся от unittest.TestCase

    def setUp(self):    # в методе setUp() подготавливаем данные

        self.file = open('acer-xf290c.edid', "rb")  # открываем бинарник
        self.data = self.file.read(20)             # читаем первые 20 байт из файла
        self.file.close()
        self.hed_pars = HeaderParser(self.data)     # передаём данные в объект класса HeaderParser()

        # Варианты правильных вопросов-ответов для тестов
        # 'ACR' - 'Acer Technologies'
        # 'BUT' - '21ST CENTURY ENTERTAINMENT'
        # 'ABV' - 'Advanced Research Technology'
        # 'AKI' - 'AKIA Corporation'
        # 'AOT' - 'Alcatel'

        self.v_c_1 = 'ACR'
        self.v_c_2 = 'BUT'
        self.v_c_3 = 'ABV'

    # далее идёт серия методов тестирования 
    def test_1(self):
        self.assertEqual(self.hed_pars.company_name_read(self.v_c_1), 'Acer Technologies')
    
    def test_2(self):
        self.assertEqual(self.hed_pars.company_name_read(self.v_c_2), '21ST CENTURY ENTERTAINMENT')

    def test_3(self):
        self.assertEqual(self.hed_pars.company_name_read(self.v_c_3), 'dadaeqaeQDaq')


# Запускаем на выполнение класс, описанный выше
# Этот класс вызывается экземпляром в ф-ии main() модуля unittest
if __name__ == "__main__":
  unittest.main()