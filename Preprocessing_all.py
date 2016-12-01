# -------------preprocessing data------------------

from io import open

category = {}
category["back."] = 2
category["buffer_overflow."] = 3
category["ftp_write."] = 4
category["guess_passwd."] = 4
category["imap."] = 4
category["ipsweep."] = 1
category["land."] = 2
category["loadmodule."] = 3
category["multihop."] = 4
category["neptune."] = 2
category["nmap."] = 1
category["perl."] = 3
category["phf."] = 4
category["pod."] = 2
category["portsweep."] = 1
category["rootkit."] = 3
category["satan."] = 1
category["smurf."] = 2
category["spy."] = 4
category["teardrop."] = 2
category["warezclient."] = 4
category["warezmaster."] = 4

category["apache2."] = 2
category["back."] = 2
category["buffer_overflow."] = 3
category["ftp_write."] = 4
category["guess_passwd."] = 4
category["httptunnel."] = 4
category["httptunnel."] = 3
category["imap."] = 4
category["ipsweep."] = 1
category["land."] = 2
category["loadmodule."] = 3
category["mailbomb."] = 2
category["mscan."] = 1
category["multihop."] = 4
category["named."] = 4
category["neptune."] = 2
category["nmap."] = 1
category["perl."] = 3
category["phf."] = 4
category["pod."] = 2
category["portsweep."] = 1
category["processtable."] = 2
category["ps."] = 3
category["rootkit."] = 3
category["saint."] = 1
category["satan."] = 1
category["sendmail."] = 4
category["smurf."] = 2
category["snmpgetattack."] = 4
category["snmpguess."] = 4
category["sqlattack."] = 3
category["teardrop."] = 2
category["udpstorm."] = 2
category["warezmaster."] = 2
category["worm."] = 4
category["xlock."] = 4
category["xsnoop."] = 4
category["xterm."] = 3
category["normal."] = 0

attr_list = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
             'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
             'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files',
             'num_outbound_cmds',
             'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
             'rerror_rate',
             'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
             'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
             'dst_host_same_src_port_rate',
             'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
             'dst_host_rerror_rate',
             'dst_host_srv_rerror_rate', 'type']


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

# -------------import data------------------
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

db.training_data.delete_many({})
db.training_data.create_index("training_set.type")
with open("data/kddcup.data_10_percent.txt") as f:
    lines = f.readlines()
    for line in lines:
        columns = line.split(',')
        dic = {}
        for attr in attr_list:
            element = columns[attr_list.index(attr)]
            if element.isdigit():
                element = int(element)
            elif isfloat(element):
                element = float(element)
            dic[attr] = element
        db.training_data.insert_one({"training_set": dic})

db.test_data.delete_many({})
with open("data/corrected.txt") as f:
    lines = f.readlines()
    for line in lines:
        columns = line.split(',')
        dic = {}
        for attr in attr_list:
            element = columns[attr_list.index(attr)]
            if element.isdigit():
                element = int(element)
            elif isfloat(element):
                element = float(element)
            dic[attr] = element
        db.test_data.insert_one({"test_set": dic})


