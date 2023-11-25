import os.path

import utils


RES_DIR = os.path.join(utils.PROJECT_DIR, 'tests', 'res')


def test_read_config():
    new_config_path = os.path.join(RES_DIR, 'config.yaml')
    old_config_path = utils.Configuration.config_path

    try:
        utils.Configuration.config_path = new_config_path
        configuration = utils.Configuration()
        assert all(company in configuration.companies for company in ('name1', 'name2'))

    finally:
        utils.Configuration.config_path = old_config_path

