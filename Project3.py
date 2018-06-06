import copy


class BayesianNetwork:
    def __init__(self, micro_loan):
        self.micro_loan = micro_loan
        if self.micro_loan:
            self.business = .8
            self.debt = 1 - self.business + .01

        else:
            self.debt = .001
            self.business = .1

        self.job_giv_b = .7
        self.job_giv_not_b = .001
        self.w_dict = {'TrueTrueTrue':      .6,
                       'TrueTrueFalse':     .95,
                       'TrueFalseTrue':     .005,
                       'TrueFalseFalse':    .6,
                       'FalseTrueTrue':     .7,
                       'FalseTrueFalse':    .95,
                       'FalseFalseTrue':    .0001,
                       'FalseFalseFalse':   .01}

    def get_prob_w(self, debt, biz, job):
        return_string = str(debt) + str(biz) + str(job)
        return self.w_dict.get(return_string, -1)

    def get_business(self, biz):
        if biz:
            return self.business
        else:
            return 1 - self.business

    def set_business(self, new_bus):
        self.business = new_bus

    def set_debt(self, new_debt):
        self.debt = new_debt

    def set_job_giv_b(self, new_val):
        self.job_giv_b = new_val

    def set_job_giv_not_b(self, new_val):
        self.job_giv_not_b = new_val

    def get_debt(self, debt):
        if debt:
            return self.debt
        else:
            return 1 - self.debt

    def get_job(self, biz, job):
        if biz:
            if job:
                return self.job_giv_b
            else:
                return 1 - self.job_giv_b
        else:
            if job:
                return self.job_giv_not_b
            else:
                return 1 - self.job_giv_not_b

    def prob_given_vars(self, debt, biz, job):
        to_mult = 1
        to_mult *= self.get_business(biz)
        to_mult *= self.get_debt(debt)
        to_mult *= self.get_job(biz, job)
        prob_w = self.get_prob_w(debt, biz, job)
        if prob_w == -1:
            print('Catastrophic Error!')
            exit(-1)
        to_mult *= prob_w
        return to_mult

    def print_network_param(self):
        print('Microloan Received: ' + str(self.micro_loan))
        print('P(B | M) =  ' + str(self.business))
        print('P(D | M) = ' + str(self.debt))
        print('P(J | B) = ' + str(self.job_giv_b))
        print('P(J | !B) = ' + str(self.job_giv_not_b))


def calc_prob_poverty(bayes_net):
    prob_of_poverty = 0
    for i in range(2):
        debt = bool(i)
        for j in range(2):
            biz = bool(j)
            for k in range(2):
                job = bool(k)
                prob_of_poverty += bayes_net.prob_given_vars(debt, biz, job)
    return prob_of_poverty


def local_search(loan, no_loan):
    prob_pov_no_loan = calc_prob_poverty(no_loan)
    rate_of_change = .001
    max_count = 1200
    altered = True
    list_of_var = ['debt', 'job_giv_b', 'job_giv_not_b']
    count = 0
    while altered and count < max_count:
        count += 1
        for var in list_of_var:
            response = calc_new_var(loan, prob_pov_no_loan, rate_of_change, var)
            if response:
                altered = response

    print('search finished')


def calc_new_var(loan, prob_pov_no_loan, rate_of_change, attr):
    altered = False

    old_var = loan.__getattribute__(attr)

    higher_var = old_var + rate_of_change
    lower_var = old_var - rate_of_change

    old_dif = calc_prob_poverty(loan) - prob_pov_no_loan

    if higher_var < 1:

        loan_copy = copy.deepcopy(loan)
        loan_copy.__setattr__(attr, higher_var)
        dif = calc_prob_poverty(loan_copy) - prob_pov_no_loan
        if abs(dif) < abs(old_dif):
            loan.__setattr__(attr, higher_var)
            old_dif = dif
            altered = True

    if lower_var > 0:
        loan_copy = copy.deepcopy(loan)
        loan_copy.__setattr__(attr, lower_var)
        dif = calc_prob_poverty(loan_copy) - prob_pov_no_loan
        if abs(dif) < abs(old_dif):
            loan.__setattr__(attr, lower_var)
            altered = True
    return altered


def main():
    loan = BayesianNetwork(True)
    no_loan = BayesianNetwork(False)
    print('Prob of P(W | M) = ' + str(calc_prob_poverty(loan)))
    print('Prob of P(W |!M) = ' + str(calc_prob_poverty(no_loan)))
    local_search(loan, no_loan)
    print('Prob of P(W | M) = ' + str(calc_prob_poverty(loan)))
    print('Prob of P(W |!M) = ' + str(calc_prob_poverty(no_loan)))
    loan.print_network_param()
    no_loan.print_network_param()


main()
