import random
import sys
import queue


class Villager:
    def __init__(self):
        self.id = None
        self.well_3_prior = None
        self.well_2_prior = None
        self.well_1_prior = None
        self.well_1_lik = None
        self.well_2_lik = None
        self.well_3_lik = None
        self.neighbor_set = None
        self.stag = None

    def create_map(self, new_id, well, priv_conf, trust_level):

        self.id = new_id
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
        self.well_1_lik = dict()
        self.well_1_lik[1] = trust_level
        self.well_1_lik[2] = remaining_prob
        self.well_1_lik[3] = remaining_prob

        self.well_2_lik = dict()
        self.well_2_lik[2] = trust_level
        self.well_2_lik[1] = remaining_prob
        self.well_2_lik[3] = remaining_prob

        self.well_3_lik = dict()
        self.well_3_lik[3] = trust_level
        self.well_3_lik[2] = remaining_prob
        self.well_3_lik[1] = remaining_prob

        return self

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

    def set_neighbors(self, neighbor_set):
        self.neighbor_set = set(neighbor_set)

    def get_neighbors(self):
        return self.neighbor_set

    def print_priors(self):
        print("Villager # " + str(self.id) + " priors:")
        print("\twell 1 prior: " + str(self.well_1_prior))
        print("\twell 2 prior: " + str(self.well_2_prior))
        print("\twell 3 prior: " + str(self.well_3_prior))

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash((self.id, self.well_1_prior, self.well_2_prior, self.well_3_prior))

    def create_stag_hare(self, new_id):
        self.id = new_id
        self.set_stag(False)
        return self

    def set_stag(self, to_set):
        self.stag = to_set

    def get_stag(self):
        return self.stag

    def innovate(self):
        num_stag = 0

        for neighbor in self.neighbor_set:
            if neighbor.get_stag():
                num_stag += 1
        cur_val = len(self.neighbor_set)
        innovate_val = (num_stag * 2)
        if innovate_val >= cur_val:
            self.set_stag(True)
        return self.get_stag()

    def print_stag(self):
        if self.get_stag():
            print("villager #" + str(self.id) + " is stag")
        else:
            print("villager #" + str(self.id) + " is hare")



def get_adhoc_network(argv):
    network_graph = {1: [2, 3],
                     2: [1, 3],
                     3: [1, 2, 4],
                     4: [3, 5, 9],
                     5: [4, 6, 10],
                     6: [5, 10, 7],
                     7: [6, 10, 8, 14],
                     8: [7, 9, 10, 12],
                     9: [4, 8, 10, 11],
                     10: [5, 6, 7, 8, 9],
                     11: [9, 12, 17],
                     12: [8, 11, 13, 16, 17],
                     13: [12, 14, 15, 16],
                     14: [7, 13, 15],
                     15: [13, 14, 16],
                     16: [12, 13, 15, 17],
                     17: [11, 12, 16]}
    villager_list = list()
    villager_dict = dict()
    num_villagers = 17
    private_confidence = float(argv[2])
    neighbor_trust = float(argv[3])
    for i in range(num_villagers):
        temp = Villager().create_map(i + 1, random.randint(1, 3), private_confidence, neighbor_trust)
        villager_list.append(temp)
        villager_dict[temp.id] = temp

    for villager in villager_list:
        neighbor_set = set()
        network_connections = network_graph[villager.id]
        for connection in network_connections:
            temp_node =  villager_dict[connection]
            if temp_node.id != connection:
                print("fatal error\n this should not happen")
                exit(1)
            else:
                neighbor_set.add(temp_node)
        villager.set_neighbors(neighbor_set)
    return villager_list


def init_network(argv, stag):
    villager_list = list()
    num_villagers = int(argv[1])
    private_confidence = float(argv[2])
    neighbor_trust = float(argv[3])
    first_prior = float(argv[4])
    number_to_direct = int(argv[5])
    type_of_network = str(argv[0])

    if stag:
        for i in range(num_villagers):
            temp = Villager().create_stag_hare(i + 1)
            villager_list.append(temp)
    else:
        for i in range(num_villagers):
            temp = Villager().create_map(i + 1, random.randint(1, 3), private_confidence, neighbor_trust)
            villager_list.append(temp)

    # initialize neighbors
    if type_of_network == 'complete':
        for villager in villager_list:
            neighbor_set = set(villager_list)
            neighbor_set.remove(villager)
            villager.set_neighbors(neighbor_set)

    elif type_of_network == 'one' or type_of_network == 'two':
        if type_of_network == 'one':
            num_neighbors = 1
        else:
            num_neighbors = 2
        for i in range(num_villagers):
            neighbor_set = set()
            for j in range(num_neighbors):
                up_neighbor = (1 + j + i) % num_villagers
                down_neighbor = (i - j - 1) % num_villagers
                neighbor_set.add(villager_list[up_neighbor])
                neighbor_set.add(villager_list[down_neighbor])
            villager_list[i].set_neighbors(neighbor_set)

    elif type_of_network == 'adhoc':
        return get_adhoc_network(argv)

    '''for i in range(number_to_direct):
        villager_list[i].well_1_prior = first_prior
        villager_list[i].well_2_prior = (1 - first_prior) / 2
        villager_list[i].well_3_prior = (1 - first_prior) / 2'''

    return villager_list


def incomplete(argv):
    villager_list = init_network(argv, False)
    rand_int = random.randint(0, len(villager_list) - 1)
    next_q = queue.Queue()
    next_q.put(villager_list[rand_int])
    visited = list()
    visited.append(villager_list[rand_int])
    count = 0
    while not next_q.empty():
        count += 1
        to_visit = next_q.get()
        choice = to_visit.get_choice()
        print("villager " + str(to_visit.id) + " chose well: " + str(choice))
        for neighbor in to_visit.neighbor_set:
            neighbor.bayes_round(choice)
            if neighbor not in visited:
                next_q.put(neighbor)
                visited.append(neighbor)
    print("total count: " + str(count))


def complete_cycle(argv):
    count = 0
    villager_list = init_network(argv, False)

    while villager_list.__len__() > 0:
        count += 1
        popped = villager_list.pop(0)
        choice = popped.get_choice()
        print("villager " + str(count) + " chose well: " + str(choice))
        for villager in villager_list:
            villager.bayes_round(choice)


def main_map():
    type_of_network = sys.argv[1]
    argv = sys.argv[1:]
    if type_of_network == 'complete':
        complete_cycle(argv)
    else:
        incomplete(argv)


def run_stag():
    villager_list = init_network(sys.argv[1:], True)
    two_start = True

    start_index = random.randint(0, len(villager_list) - 1)
    next_q = queue.Queue()
    #start_index = 15
    second_index = random.randint(0, len(villager_list) - 1)
    while second_index == start_index:
        random.randint(0, len(villager_list) - 1)

    start_index = 10
    second_index = 11
    first = villager_list[start_index]
    second = villager_list[second_index]

    print('First Villager: #' + str(first.id))
    print('Second Villager: #' + str(second.id))
    first.set_stag(True)
    #second.set_stag(True)

    in_queue = list()
    for neighbor in first.get_neighbors():
        if not neighbor.get_stag() and neighbor not in in_queue:
            next_q.put(neighbor)
            in_queue.append(neighbor)
    if two_start:
        second.set_stag(True)
        for neighbor in second.get_neighbors():
            if not neighbor.get_stag() and neighbor not in in_queue:
                next_q.put(neighbor)
                in_queue.append(neighbor)

    while not next_q.empty():
        to_visit = next_q.get()
        in_queue.remove(to_visit)
        innovation = to_visit.innovate()
        to_visit.print_stag()
        if innovation:
            for neighbor in to_visit.get_neighbors():
                if not neighbor.get_stag() and neighbor not in in_queue:
                    next_q.put(neighbor)
                    in_queue.append(neighbor)

    print('\n\nResults: ')
    for villager in villager_list:
        villager.print_stag()




def main_stag():
    type_of_network = sys.argv[1]
    argv = sys.argv[1:]
    run_stag()


# main_map()

main_stag()

'''temp = Villager().create_stag_hare(1)
temp2 = Villager().create_stag_hare(2)
set1 = set()
set2 = set()
set1.add(temp2)
set2.add(temp)
temp.set_neighbors(set1)
temp2.set_neighbors(set2)
temp2.set_stag(True)
temp.innovate()

print()'''