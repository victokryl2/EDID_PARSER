import sys


class FileReading():
    def __init__(self):
        # читаем бинарник в переменную data
        file_name = sys.argv[1] # читаем первый аргумент командной строки
        self._file = open(file_name, "rb") # открываем бинарник
        self._data = self._file.read(20)   # читаем первые 20 байт из файла
        self._file.close()
        
    
    ############  ГЕТТЕРЫ, СЕТТЕРЫ   ######################################################
    #######################################################################################

    # геттер data
    def get_data(self):
        return self._data

    # экземпляр встроенного класса property
    data = property(fget = get_data)