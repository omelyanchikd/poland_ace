from world import World

from sklearn import linear_model
from sklearn.metrics import r2_score

import pandas
import random
from mape import mape

import csv

class Scenario():
    def __init__(self, history, firm_info, match_info, distribute_subsidies_info, firm_config, regression_type = "total",
                 distribute_subsidies = False, disturb_result = False, disturb_coefficients = False, regression = "bayes",
                 seed = 1, output = "output.csv",):
        random.seed(seed)
        self.seed = seed
        self.history = pandas.read_csv(history, sep = ";", decimal = ",")
        #self.firm_info = pandas.read_csv(firm_info, sep = ";", decimal = ",")
        self.firm_info = firm_info
        self.firm_configuration = '_'.join(str.split(firm_config.strip(".csv"), "_")[2:])
        self.regression_type = regression_type
        self.disturb_result = disturb_result
        self.disturb_coefficients = disturb_coefficients
        self.regression = regression
        self.distribute_subsidies = distribute_subsidies
        if self.regression_type == 'average':
            self.model = World(self.history['employees'][0], firm_info, self.history[['workers', 'subsidies', 'sales']],
                               distribute_subsidies, disturb_result, disturb_coefficients, regression, regression_type, match_info,
                               distribute_subsidies_info)
        else:
            self.model = World(self.history['employees'][0], firm_info, self.history[['employees', 'budget', 'revenues']],
                               distribute_subsidies, disturb_result, disturb_coefficients, regression, regression_type, match_info,
                               distribute_subsidies_info)

        self.benchmark = self.history['revenues']
        self.workers_history = self.history['employees']
        self.budget_history = self.history['budget']
        self.output_file = open(output, "a", newline = '')
        self.output_writer = csv.writer(self.output_file, delimiter = ';')


    def run(self, steps):
        for step in range(steps):
            self.model.step(self.budget_history[step], self.workers_history[step])
            print("Step " + str(step + 1) + " finished.")
            self.output_writer.writerow((self.seed, self.firm_configuration, self.regression_type, self.regression,
                                         self.distribute_subsidies, self.disturb_result, self.disturb_coefficients, step + 1,
                                         mape(self.benchmark[:len(self.model.sales)], self.model.sales),
                                         r2_score(self.benchmark[:len(self.model.sales)], self.model.sales)))
#            sales_file.write("%.2f" % poland.sales[step] + '\n')
#            workers_file.write(str(poland.workers[step]) + '\n')
#            rscore_file.write("%.4f" % rscore + '\n')
#            mape_file.write("%.4f" % mape_score + '\n')


