import models

# Load all return profiles
return_profiles = models.ReturnProfile.load_return_profiles('./model/return_profiles.json')

# Load all saving types
saving_types = models.SavingType.load_saving_types('./model/saving_types.json', return_profiles)

# Load savings approach and baseline accounts
savings_approach = models.SavingsApproach.load_savings_approach('./savings_approach.json', saving_types)

# Loop through years and calculate return on each year
savings_approach.portfolio.print_value()

# Print out totals for each account every year
for year in savings_approach.years:
    y = year.year

    # Compute new total for year of growth in existing accounts
    for account_key in savings_approach.portfolio.accounts:
        account = savings_approach.portfolio.accounts.get(account_key)
        #print('Year {}) account id = {}; value = {}; saving type = {}; return = {}'.format(
        #    y, account.id, account.amount, account.savings_type.name, account.savings_type.return_profile.annual_return))

        account.amount = account.amount * account.savings_type.return_profile.annual_return

    # Add new savings into specific accounts
    for account in year.savings_accounts:
        port_account = savings_approach.portfolio.accounts.get(account.id)
        #print('adding {} to {}'.format(account.amount, port_account.name))
        port_account.amount += account.amount
        if account.employee_match is not None:
            port_account.amount += account.employee_match

    print('After year {}) {}'.format(y, savings_approach.portfolio.get_print_value()))

