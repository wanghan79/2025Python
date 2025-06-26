import csv
class CsvHelper:
    @classmethod
    def write(self,data,file_name):
        with open(file_name,'a',encoding='utf-8',newline='') as f:
            writer=csv.writer(f,delimiter=',')
            writer.writerow(data)