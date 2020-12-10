import pytest
import time
import yaml
import random
from sentry_sdk import set_tag

@pytest.mark.usefixtures("driver")
def test_add_to_cart(driver):
    set_tag("test", "test_add_to_cart")
    with open('endpoints.yaml', 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        endpoints = data_loaded['react_endpoints']

    for endpoint in endpoints:
        for i in range(random.randrange(20)):
            driver.get(endpoint)

            buy_button = driver.find_element_by_css_selector('.item button')
            for i in range(random.randrange(3) + 3):
                buy_button.click()

            driver.find_element_by_css_selector('.sidebar button').click()
            time.sleep(random.randrange(3) + 3)
