import json
import datetime as dt
from config import operations_path


class BankWidget:
    """Работает с банковскими транзакциями."""

    def __init__(self, file):
        self.file = file

    def read_file(self):
        """Считывает файл, указанный при инициализации."""
        with open(self.file, 'r', encoding='utf-8') as file:
            content = file.read()
            self.file_json = json.loads(content)
            json.dumps(self.file_json, indent=4, ensure_ascii=False)
        for operation in self.file_json:
            try:
                operation['date'] = dt.datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f')
            except KeyError:
                continue
        return self.file_json

    def find_smallest(self):
        """Находит наименьшее значение массива."""
        smallest = self.file_json[0]['date']
        smallest_index = 0
        # return smallest
        for i in range(1, len(self.file_json)):
            if self.file_json[i]:
                if self.file_json[i]['date'] > smallest:
                    smallest_index = i
                    smallest = self.file_json[i]['date']
        return smallest_index

    def selection_sort(self):
        """сортировка выбором"""
        self.new_arr = []

        for i in range(len(self.file_json)):
            # Добавляем наименьший элемент в массиве в новый список
            try:
                self.file_json[i]

            except IndexError:
                continue
            else:
                if self.file_json[i]:
                    smallest = self.find_smallest()
                    self.new_arr.append(self.file_json.pop(smallest))
        return self.new_arr

    def last_operetions(self):
        """Возвращает последние 5 операций."""
        last_five_operations = [self.new_arr[i] for i in range(len(self.new_arr))
                                if self.new_arr[i]['state'] == 'EXECUTED']
        last_five_operations = last_five_operations[:5]
        last_five_operations_in_format = []

        for execute in last_five_operations:
            execute[
                'date'] = f"{execute['date'].date().day}.{execute['date'].date().month}.{execute['date'].date().year}"
            if execute['to'][:5].lower().strip() == 'счет':
                mask_to = ''.join(['*' for i in range(len(execute['to'].split()[-1]) - 4)])
                execute['to'] = f"Счет {mask_to}{execute['to'].split()[-1][-4:]}"
            else:
                mask_to = ''.join(['*' for i in range(len(execute['to'].split()[-1]) - 10)])
                execute[
                    'to'] = f"{' '.join(execute['to'].split()[:-2])} {execute['to'].split()[-1][:6]} {mask_to} {execute['to'].split()[-1][-4:]}"
            try:
                execute['from']
            except KeyError:
                if execute['to'][:5].lower().strip() == 'счет':
                    # mask_score = ''.join(['*' for i in range(len(execute['to'].split()[-1]) - 4)])
                    last_five_operations_in_format.append(f"{execute['date']} - {execute['description']}\n"
                                                           f"кому - {execute['to']}\n\n"
                                                           )
                else:
                    mask = ''.join(['*' for i in range(len(execute['to'].split()[-1]) - 10)])
                    last_five_operations_in_format.append(f"{execute['date']} - {execute['description']}\n"
                          f"кому - {execute['to']}\n\n"
                          )
            else:
                if execute['from'][:5].lower().strip() == 'счет':
                    mask_from = ''.join(['*' for i in range(len(execute['from'].split()[-1]) - 4)])
                    execute['from'] = f"Счет {mask_from}{execute['from'].split()[-1][-4:]}"
                else:
                    mask_from = ''.join(['*' for i in range(len(execute['to'].split()[-1]) - 10)])
                    execute[
                        'from'] = f"{' '.join(execute['from'].split()[:-2])} {execute['from'].split()[-1][:6]} {mask_from} {execute['from'].split()[-1][-4:]}"

                last_five_operations_in_format.append(f"{execute['date']} - {execute['description']}\n"
                      f"от - {execute['from']}\n"
                      f"кому - {execute['to']}\n\n")
        last_five_operations_in_format = ''.join(last_five_operations_in_format)
        return last_five_operations_in_format
    # last_operetions(file_json)

# test_1 = BankWidget(operations_path)
# test_1.read_file()
# test_1.find_smallest()
# test_1.selection_sort()
# # print(test_1.last_operetions())
# print(test_1.last_operetions.last_five_operations_in_format)
