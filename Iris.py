from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

import loaddata as ld

train_csv = 'iris_training.csv'
test_f_csv = 'iris_test_f.csv'
test_t_csv = 'iris_test_t.csv'

# The 'filename' of an Excel or Access file SHOULD be the FULL path
excel_file = r'D:\Dropbox\PycharmProjects\untitled\iris_data.xlsx'
access_file = r'D:\Dropbox\PycharmProjects\untitled\iris_data.accdb'
train_data = 'train_data'
test_features = 'test_features'
test_targets = 'test_targets'

# Load datasets from Excel
training_set = ld.load_excel_sworksheet(filename=excel_file, sheetname=train_data, feature_columns_count=4,
                                        feature_data_type=np.float32, target_data_type=np.int)
test_set = ld.load_excel_mworksheet(filename=excel_file, feature_sheet=test_features, target_sheet=test_targets,
                                    feature_data_type=np.float32, target_data_type=np.int)


'''
# Load datasets from Access
training_set = ld.load_access_stable(filename=access_file, tablename=train_data, feature_columns_count=4,
                                     feature_data_type=np.float32, target_data_type=np.int, key=True)
test_set = ld.load_access_mtable(filename=access_file, feature_table=test_features, target_table=test_targets,
                                 feature_data_type=np.float32, target_data_type=np.int)
'''

'''
# Load datasets from CSV files
training_set = ld.load_scsv(filename=train_csv, feature_columns_count=4,
                            feature_data_type=np.float32, target_data_type=np.int, read_header=1)
test_set = ld.load_mcsv(feature_filename=test_f_csv, target_filename=test_t_csv,
                        feature_data_type=np.float32, target_data_type=np.int, read_header=0)
'''
'''
# Load dataset from SQL Server
training_set = ld.load_sqlserver_stable(database='Python_Test', uid='sa', pwd='gaoyun2109933',
                                        tablename=train_data, server='Localhost', feature_columns_count=4,
                                        feature_data_type=np.float32,target_data_type=np.int)
test_set = ld.load_sqlserver_mtable(database='Python_Test', uid='sa', pwd='gaoyun2109933',
                                    feature_table=test_features, target_table=test_targets,
                                    feature_data_type=np.float32, target_data_type=np.int)
'''

# Specify that all features have real-value data
feature_columns = [tf.contrib.layers.real_valued_column("", dimension=4)]

# Build 3 layer DNN with 10, 20, 10 units respectively.
classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10],
                                            n_classes=3,
                                            model_dir="/tmp/iris_model")


# Define the training inputs
def get_train_inputs():
    x = tf.constant(training_set.feature)
    y = tf.constant(training_set.target)

    return x, y

# Fit model.
classifier.fit(input_fn=get_train_inputs, steps=2000)


# Define the test inputs
def get_test_inputs():
    x = tf.constant(test_set.feature)
    y = tf.constant(test_set.target)

    return x, y

# Evaluate accuracy.
accuracy_score = classifier.evaluate(input_fn=get_test_inputs,
                                     steps=1)["accuracy"]

print("\nTest Accuracy: {0:f}\n".format(accuracy_score))

# Classify two new flower samples.
def new_samples():
    return np.array(
        [[6.4, 3.2, 4.5, 1.5],
         [5.8, 3.1, 5.0, 1.7]], dtype=np.float32)

predictions = list(classifier.predict(input_fn=new_samples))

print("New Samples, Class Predictions:    {}\n".format(predictions))