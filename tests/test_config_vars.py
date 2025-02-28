

def test_config_vars(config):
    # dev -->  pytest -v -s -k "config_vars"
    # dev -->  pytest -v -s --env=dev  -k "config_vars"
    # qa  -->  pytest -v -s --env=qa -k "config_vars"
    print('\nEnvironment --> ', config.env)
    print('GITHUB_API_TOKEN --> ', config.GITHUB_API_TOKEN)
    print('GITHUB_REPO -->', config.GITHUB_REPO)
    print('GITHUB_USER -->', config.GITHUB_USER)
    print('BASE_URL -->', config.BASE_URL)
