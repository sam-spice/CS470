import math
import random
import sys


class Villager:
    def __init__(self, well, priv_conf, trust_level):

        if well == 1:
            self.well_1_prior = priv_conf
            remaining_prob = (1 - priv_conf)/2
            self.well_2_prior = remaining_prob
            self.well_3_prior = remaining_prob
            pass
        elif well == 2:
            self.well_2_prior = priv_conf
            remaining_prob = (1 - priv_conf) / 2
            self.well_1_prior = remaining_prob
            self.well_3_prior = remaining_prob
        elif well == 3:
            self.well_3_prior = priv_conf
            remaining_prob = (1 - priv_conf) / 2
            self.well_2_prior = remaining_prob
            self.well_1_prior = remaining_prob
        else:
            print('invalid well number')

        remaining_prob = (1 - trust_level)/2
        self.well_1_lik = {}
        self.well_1_lik[1] = trust_level
        self.well_1_lik[2] = remaining_prob
        self.well_1_lik[3] = remaining_prob

        self.well_2_lik = {}
        self.well_2_lik[2] = trust_level
        self.well_2_lik[1] = remaining_prob
        self.well_2_lik[3] = remaining_prob

        self.well_3_lik = {}
        self.well_3_lik[3] = trust_level
        self.well_3_lik[2] = remaining_prob
        self.well_3_lik[1] = remaining_prob

    def bayes_round(self, observation):
        new_o = 0
        new_o += self.well_1_prior * self.well_1_lik[observation]
        new_o += self.well_2_prior * self.well_2_lik[observation]
        new_o += self.well_3_prior * self.well_3_lik[observation]

        new_well_1_prior = (self.well_1_prior * self.well_1_lik[observation])/new_o
        new_well_2_prior = (self.well_2_prior * self.well_2_lik[observation])/new_o
        new_well_3_prior = (self.well_3_prior * self.well_3_lik[observation])/new_o

        self.well_1_prior = new_well_1_prior
        self.well_2_prior = new_well_2_prior
        self.well_3_prior = new_well_3_prior

    def get_choice(self):
        max_val = max(self.well_1_prior, self.well_2_prior, self.well_3_prior)

        if max_val == self.well_1_prior:
            return 1
        if max_val == self.well_2_prior:
            return 2
        if max_val == self.well_3_prior:
            return 3
        return 0

def main():
    count = 0
    villager_list = list()
    num_villagers = int(sys.argv[1])
    private_confidence = float(sys.argv[2])
    neighbor_trust = float(sys.argv[3])
    first_prior = float(sys.argv[4])
    number_to_direct = int(sys.argv[5])

    for i in range(num_villagers):
        temp = Villager(random.randint(1,3),private_confidence, neighbor_trust)
        villager_list.append(temp)

    for i in range(number_to_direct):
        villager_list[i].well_1_prior = first_prior

    while villager_list.__len__() > 0:
        count += 1
        popped = villager_list.pop(0)
        choice = popped.get_choice()
        print("villager " + str(count) + " chose well" + str(choice))
        for villager in villager_list:
            villager.bayes_round(choice)

    #temp.bayes_round(1)
    #print(temp.get_choice())

main()