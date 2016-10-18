from scenario import Scenario

import sys
import csv
import copy

from create_firms import create_firms
from match import match
from distribute_funds import distribute_funding

import pandas
import random

def main(argv):

    args = argv
    firm_config = str(args[0])
    start_seed = int(args[1])
    end_seed = int(args[2])
    output = str(args[3])

    print(firm_config)
    print(start_seed)
    print(end_seed)
    print(output)



    datafile = "poland.csv"
    history = pandas.read_csv(datafile, sep = ";", decimal = ",")

    steps = 34

    #firm_configurations = ["firm_info_1.csv", "firm_info_10000_1000_100_10.csv", "firm_info_200000.csv"]

    regressions = ['bayes', 'linear']
    regression_types = ["average", "total"]

    distribute_subsidies = [True, False]
    disturb_results = [True, False]
    disturb_coefficients = [True, False]

    with open(output, "w", newline='') as output_file:
        writer = csv.DictWriter(output_file, delimiter=';',
                                fieldnames=["seed", "firm_configuration", "regression_type", "regression", "distribute_subsidies",
                                        "disturb_result", "disturb_coefficients", "step", "mape", "r2_score"])
        writer.writeheader()
        output_file.close()

#    for firm_config in firm_configurations:
    for seed in range(start_seed, end_seed):
        random.seed(seed)
        firm_info = create_firms(pandas.read_csv(firm_config, sep = ";", decimal = ","), history['employees'][0])
        match_info = [[] for i in range(steps)]
        match_info[0] = copy.deepcopy(firm_info)
        for step in range(steps):
            if step != 0:
                match_info[step] = match(match_info[step - 1], history['employees'][step] - history['employees'][step - 1])
                match_info[step] = [firm for firm in match_info[step] if firm.workers > 0]
        for distribute_subsidy in distribute_subsidies:
            if distribute_subsidy:
                random.seed(seed)
                distribute_subsidies_info = []
                for step in range(steps):
                    distribute_subsidies_info.append(distribute_funding(history, history['budget'][step], len(match_info[step])))
            for regression in regressions:
                for regression_type in regression_types:
                    for disturb_result in disturb_results:
                        for disturb_coefficient in disturb_coefficients:
                            Scenario("poland.csv", firm_info, match_info, distribute_subsidies_info, firm_config, regression_type,
                                             distribute_subsidy, disturb_result, disturb_coefficient, regression, seed, output).run(steps)



if __name__ == "__main__":
   main(sys.argv[1:])