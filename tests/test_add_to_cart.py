import pytest
import time
import yaml

@pytest.mark.usefixtures("driver")
def test_add_to_cart(driver):

    with open('endpoints.yaml', 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        endpoints = data_loaded['react_endpoints']

    for endpoint in endpoints:
        driver.get(endpoint)

        buy_button = driver.find_element_by_css_selector('.item button')
        for i in range(3):
            buy_button.click()

        driver.find_element_by_css_selector('.sidebar button').click()
        time.sleep(3)
