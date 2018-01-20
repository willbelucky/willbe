# -*- coding: utf-8 -*-
"""
:Author: Jaekyoung Kim
:Date: 2018. 1. 20.
"""
import os

from keras.callbacks import ModelCheckpoint

from util.logging_supporter import get_logger, INFO

# Set the root directory to your working directory.
# For example, /Users/willbe/PycharmProjects/willbe
MODEL_CHECK_POINT_DIR = os.getcwd().replace(chr(92), '/') + '/model_check_points/'


class SupervisedData:

    def __init__(self, job_name, x_train, y_train, x_test, y_test, input_shape):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.input_shape = input_shape
        self.job_name = job_name
        self.logger = get_logger('InfoLogger', job_name, INFO)

    def evaluate_model(self, model, batch_size, epochs):
        # checkpoint
        file_name = 'weights-improvement-{epoch:02d}-{val_acc:.2f}.h5'
        checkpoint = ModelCheckpoint(MODEL_CHECK_POINT_DIR + file_name, monitor='val_acc', verbose=1,
                                     save_best_only=True, mode='max')
        callbacks_list = [checkpoint]

        model.fit(self.x_train, self.y_train,
                  batch_size=batch_size,
                  epochs=epochs,
                  callbacks=callbacks_list,
                  verbose=1,
                  validation_data=(self.x_test, self.y_test))
        score = model.evaluate(self.x_test, self.y_test, verbose=0)
        self.logger.info('{} Test loss:{}'.format(self.job_name, score[0]))
        self.logger.info('{} Test accuracy:{}'.format(self.job_name, score[1]))
