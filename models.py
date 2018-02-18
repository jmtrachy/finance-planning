from operator import attrgetter
import json


class FileLoader():
    @staticmethod
    def load_model(model_file_location):
        with open(model_file_location) as json_data:
            model = json.load(json_data)

        return model


class SavingYear():
    def __init__(self, j, savings_accounts):
        self.year = j
        self.savings_accounts = savings_accounts


class SavingsAccount():
    def __init__(self, id, amount, name=None, employee_match=None, savings_type=None):
        self.id = id
        self.amount = amount
        self.employee_match = employee_match
        self.name = name
        self.savings_type = savings_type


class Portfolio():
    def __init__(self, accounts):
        print('Creating portfolio')
        self.accounts = accounts

    def get_print_value(self):
        total_value = 0.0
        account_str = ''
        for account_key in self.accounts.keys():
            account = self.accounts.get(account_key)
            account_str += '{} is worth ${:.2f}; '.format(account.name, account.amount)
            total_value += account.amount

        return 'Total account value: ${:.2f}........{}'.format(total_value, account_str)

    def print_value(self):
        print(self.get_print_value())


class SavingsApproach():
    def __init__(self, portfolio, years):
        self.portfolio = portfolio
        self.years = years

    @staticmethod
    def load_savings_approach(model_file_location, saving_types):
        savings_approach_json = FileLoader.load_model(model_file_location)
        years = []

        for year_block in savings_approach_json.get('years'):
            year_tokens = year_block.get('years').split('-')
            start_year = int(year_tokens[0])
            end_year = int(year_tokens[1])

            for j in range(start_year, end_year + 1):
                loaded_accounts = year_block.get('accounts')
                accounts = []
                for account in loaded_accounts:
                    accounts.append(SavingsAccount(account.get('id'), account.get('amount'),
                                                   employee_match=account.get('employeeMatch')))
                years.append(SavingYear(j, accounts))

        years = sorted(years, key=attrgetter('year'))

        baseline_json = savings_approach_json.get('baseline')
        baseline_accounts = {}
        for account in baseline_json.get('accounts'):
            baseline_accounts[account.get('id')] = SavingsAccount(account.get('id'), account.get('amount'),
                                                                  name=account.get('name'),
                                                                  savings_type=saving_types.get(account.get('savingType')))

        portfolio = Portfolio(baseline_accounts)

        return SavingsApproach(portfolio, years)


class ReturnProfile():
    def __init__(self, id, name, annual_return):
        self.id = id
        self.name = name
        self.annual_return = annual_return

    @staticmethod
    def load_return_profiles(model_file_location):
        return_profiles_json = FileLoader.load_model(model_file_location)
        return_profiles = {}

        for rtp in return_profiles_json:
            return_profiles[rtp.get('id')] = (ReturnProfile(rtp.get('id'), rtp.get('name'), rtp.get('annualReturn')))

        return return_profiles


class SavingType():
    def __init__(self, id, name, max_contribution, max_emp_match, return_profile):
        self.id = id
        self.name = name
        self.max_contribution = max_contribution
        self.max_emp_match = max_emp_match
        self.return_profile = return_profile

    @staticmethod
    def load_saving_types(model_file_location, return_profiles):
        saving_types_json = FileLoader.load_model(model_file_location)
        saving_types = {}

        for saving_type in saving_types_json:
            print('loaded saving type {}'.format(saving_type.get('id')))
            saving_types[saving_type.get('id')] = (SavingType(saving_type.get('id'), saving_type.get('name'),
                                                   saving_type.get('maxContribution'), saving_type.get('maxEmployerMatch'),
                                                   return_profiles.get(saving_type.get('returnProfile'))))

        return saving_types
