import numpy as np
import collections
import csv
import pyodbc


def load_scsv(filename, feature_columns_count=0,
              feature_data_type=np.float32, target_data_type=np.float32, read_header=1):
    csv_file = open(filename)
    data_file = csv.reader(csv_file)

    header = []

    if read_header != 0:
        header = next(data_file)
        if feature_columns_count == 0:
            feature_columns_count = int(header[1])

    data_rows = []
    for row in data_file:
        data_rows.append(row)

    if read_header == 2:
        return split_to_set(data_rows, feature_columns_count, feature_data_type, target_data_type), header
    else:
        return split_to_set(data_rows, feature_columns_count, feature_data_type, target_data_type)


def load_mcsv(feature_filename, target_filename,
              feature_data_type=np.float32, target_data_type=np.float32, read_header=0):

    f_csv_file = open(feature_filename)
    f_data_file = csv.reader(f_csv_file)

    t_csv_file = open(target_filename)
    t_data_file = csv.reader(t_csv_file)

    f_header = []
    t_header = []

    if read_header != 0:
        f_header = next(f_data_file)
        t_header = next(t_data_file)

    feature = []
    target = []

    for f_row in f_data_file:
        feature.append(f_row)

    for t_row in t_data_file:
        target.append(t_row)

    if read_header == 2:
        return rows_to_set(feature, target, feature_data_type, target_data_type), f_header, t_header
    else:
        return rows_to_set(feature, target, feature_data_type, target_data_type)


def load_excel_sworksheet(filename, sheetname, feature_columns_count,
                          feature_data_type=np.float32, target_data_type=np.float32):
    conn_str = (
        r'DRIVER={Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)};'
        r'DBQ=' + filename + ';'
    )
    cnxn = pyodbc.connect(conn_str, autocommit=True)
    crsr = cnxn.cursor()

    data_rows = crsr.execute('select * from [' + sheetname + '$]').fetchall()

    return split_to_set(data_rows, feature_columns_count, feature_data_type, target_data_type)


def load_excel_mworksheet(filename, feature_sheet, target_sheet,
                          feature_data_type=np.float32, target_data_type=np.float32):
    conn_str = (
        r'DRIVER={Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)};'
        r'DBQ=' + filename + ';'
    )
    cnxn = pyodbc.connect(conn_str, autocommit=True)
    crsr = cnxn.cursor()

    feature = crsr.execute('select * from [' + feature_sheet + '$]').fetchall()
    target = crsr.execute('select * from [' + target_sheet + '$]').fetchall()

    return rows_to_set(feature, target, feature_data_type, target_data_type)


def load_access_stable(filename, tablename, feature_columns_count,
                       feature_data_type=np.float32, target_data_type=np.float32, key=False):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + filename + ';'
    )
    cnxn = pyodbc.connect(conn_str, autocommit=True)
    crsr = cnxn.cursor()

    data_rows = crsr.execute('select * from ' + tablename).fetchall()

    if key:
        data_rows = split_data_rows(data_rows, 1)[1]

    return split_to_set(data_rows, feature_columns_count, feature_data_type, target_data_type)


def load_access_mtable(filename, feature_table, target_table,
                       feature_data_type=np.float32, target_data_type=np.float32, key=False):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + filename + ';'
    )
    cnxn = pyodbc.connect(conn_str, autocommit=True)
    crsr = cnxn.cursor()

    feature = crsr.execute('select * from ' + feature_table).fetchall()
    target = crsr.execute('select * from ' + target_table).fetchall()

    if key:
        feature = split_data_rows(feature, 1)[1]
        target = split_data_rows(target, 1)[1]

    return rows_to_set(feature, target, feature_data_type, target_data_type)


def load_sqlserver_stable(database, uid, pwd, tablename, feature_columns_count, server='Localhost',
                       feature_data_type=np.float32, target_data_type=np.float32, key=False):
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server};'
        r'SERVER='+server+';'
        r'DATABASE='+database+';'
        r'UID='+uid+';'
        r'PWD='+pwd
    )
    crsr = conn.cursor()

    data_rows = crsr.execute('select * from ' + tablename).fetchall()

    if key:
        data_rows = split_data_rows(data_rows, 1)[1]

    return split_to_set(data_rows, feature_columns_count, feature_data_type, target_data_type)


def load_sqlserver_mtable(database, uid, pwd, feature_table, target_table, server='Localhost',
                       feature_data_type=np.float32, target_data_type=np.float32, key=False):
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server};'
        r'SERVER='+server+';'
        r'DATABASE='+database+';'
        r'UID='+uid+';'
        r'PWD='+pwd
    )
    crsr = conn.cursor()

    feature = crsr.execute('select * from ' + feature_table).fetchall()
    target = crsr.execute('select * from ' + target_table).fetchall()

    if key:
        feature = split_data_rows(feature, 1)[1]
        target = split_data_rows(target, 1)[1]

    return rows_to_set(feature, target, feature_data_type, target_data_type)


# Common fuctions


def split_data_rows(data_rows, sp_index):
    return np.split(np.asanyarray(data_rows), [sp_index], 1)


def rows_to_set(feature_rows, target_rows, fdt, tdt):
    Dataset = collections.namedtuple('Dataset', ['feature', 'target'])
    return Dataset(feature=np.asanyarray(feature_rows, dtype=fdt), target=np.asanyarray(target_rows, dtype=tdt))


def split_to_set(data_rows, sp_index,  fdt, tdt):
    f, t = split_data_rows(data_rows, sp_index)
    return rows_to_set(f, t, fdt, tdt)