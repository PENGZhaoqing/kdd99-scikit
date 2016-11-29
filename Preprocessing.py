from io import open
from Variable import *
from Mongo_Con import *


def transform_type(input_file, output_file):
    with open(output_file, "w") as text_file:
        with open(input_file) as f:
            lines = f.readlines()
            for line in lines:
                columns = line.split(',')
                for raw_type in category:
                    flag = False
                    if raw_type == columns[-1].replace("\n", ""):
                        str = ','.join(columns[0:attr_list.index('type')])
                        text_file.write("%s,%d\n" % (str, category[raw_type]))
                        flag = True
                        break
                if not flag:
                    text_file.write(line)
                    print(line)

transform_type("raw/kddcup.data_10_percent.txt", "data/kddcup.data_10_percent.txt")
transform_type("raw/corrected.txt", "data/corrected.txt")

DB_manager().import_training_data("data/kddcup.data_10_percent.txt")
DB_manager().import_test_data('data/corrected.txt')
