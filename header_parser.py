import pandas as pd


class HeaderParser():
    def __init__(self, data):
        self._data = data
        self._vendor_code = ''              # буквенный код производителя
        self._vendor_name = ''              # наименование производителя
        self._man_prod_code = 0             # код продукции Manufacturer product code
        self._ser_num = 0                   # серийный номер изделия
        self._manuf_week = 0                # неделя производства
        self._manuf_year = 0                # год производства
        self._edid_version = ''             # версия EDID
        self._edid_revision = ''            # ревизия EDID

        print('\n' 'Данные хедера файла  ' '*.edid:' '\n')
        self.manuf_id_read()                # читаем код производителя
        self.company_name_read(self._vendor_code) # читаем наименование компании-производителя
        self.manuf_prod_code_read()         # читаем код продукции Manufacturer product code
        self.serial_number_read()           # читаем серийный номер изделия Serial number
        self.manuf_week_year()              # читаем неделю и год производства
        print('\n' 'Данные других разделов файла - в разработке' '\n')


##########################################################################################################
################## МЕТОДЫ ################################################################################
##########################################################################################################

    # @brief  Метод чтения буквенного кода производителя
    # @detail 
    # @param  None
    # @retval None
    def manuf_id_read(self):
        bytes_8_9 = (self._data[8] << 8) | self._data[9]   # берём два байта 8 и 9 и составляем из них uint16_t
        mask = 0b11111
        capit_prefix = (0b1 << 6)               # приставка заглавной буквы ascii
        for i in range(10, -5, -5):
            offset = i                          # сдвиг для чтения первой буквы
            c = (bytes_8_9 >> offset) & mask    # 5-ти битный код буквы
            letter = chr(capit_prefix | c)      # полный код буквы
            self._vendor_code = self._vendor_code + letter
        print('Manufacturer ID:', self._vendor_code)

    # @brief  Метод чтения наименования компании-производителя
    # @detail Наименование компании определяется по таблице PNP (https://uefi.org/pnp_id_list)
    # заранее скачанной с сайта в виде файла *.xlsx
    # @param  None
    # @retval None
    def company_name_read(self, v_c):
        # определяем имя производителя по коду производителя из таблицы
        pnp_data = pd.read_excel('./pnp.xlsx')                                  # загружаем файл с кодами и названиями производителей
        id_col_name = pnp_data.columns.tolist()[1]                              # получаем название колонки с кодами произв-лей
        vendors_col_name = pnp_data.columns.tolist()[0]                         # получаем название колонки с именами компаний
        # получаем индекс строки вендора в виде списка
        ind_list = pnp_data.index[pnp_data[id_col_name] == v_c].tolist()
        ind = ind_list[0]                                                       # индекс строки с кодом вендора
        self._vendor_name = pnp_data.iloc[ind][vendors_col_name]
        print('Company name:', self._vendor_name)
        return self._vendor_name

    # @brief  Метод чтения кода продукции Manufacturer product code
    # @detail Подход little-endian
    # @param  None
    # @retval None
    def manuf_prod_code_read(self):
        # определяем Manufacturer product code 
        byte_10 = self._data[10]
        byte_11 = (self._data[11] << 8)
        self._man_prod_code = byte_11 | byte_10
        print('Manufacturer product code:', self._man_prod_code)

    
    # @brief  Метод чтения серийного номера изделия Serial number
    # @detail Подход little-endian
    # @param  None
    # @retval None
    def serial_number_read(self):
        for i in range(15, 11, -1):
            offset = (i - 12) * 8
            self._ser_num = self._ser_num | (self._data[i] << offset)
        print('Serial number:', self._ser_num)

    # @brief  Метод чтения  недели и года производства
    # @detail Подход little-endian
    # @param  None
    # @retval None
    def manuf_week_year(self):
        self._manuf_week = self._data[16]
        self._manuf_year = self._data[17] + 1990
        print('Week of manufacture:', self._manuf_week)
        print('Year of manufacture:', self._manuf_year)

    # @brief  Метод чтения версии и ревизии EDID
    # @detail 
    # @param  None
    # @retval None
        # определяем EDID version
        if (self._data[18] == 1):
            self._edid_version = '1.3 or 1.4'
        else:
            self._edid_version = 'unknown'
        print('EDID version:', self._edid_version)
        # определяем EDID revision
        if (self._data[19] == 3):
            self._edid_revision = '1.3'
        elif (self._data[19] == 4):
            self._edid_revision = '1.4'
        else:
            self._edid_revision = 'unknown'
        print('EDID revision:', self._edid_revision)