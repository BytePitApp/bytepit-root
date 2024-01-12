from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


URLS = {
    'login_page': 'https://bytepit.cloud/login',
    'login': 'https://bytepit.cloud/api/auth/login',
    'logout': 'https://bytepit.cloud/api/auth/logout'
}


def wait_for_ajax_complete(driver):
    return driver.execute_script("return (window.performance.getEntriesByType('resource').filter(resource => "
                                 "resource.name.includes('/api/admin/list-users')).length > 0)")


def wait_for_api_response(driver, request_url):
    return driver.execute_script(f"return (window.performance.getEntriesByType('resource').filter(resource => "
                                 f"resource.name.includes('{request_url}'))[0])")


def define_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)

    return driver


def login(driver, username='test', password='testtest'):
    driver.get(URLS['login_page'])

    username_input_field = driver.find_element('name', 'username')
    password_input_field = driver.find_element('name', 'password')
    submit_button = driver.find_element('xpath', '//span[text()="Submit"]')

    username_input_field.send_keys(username)
    password_input_field.send_keys(password)
    submit_button.click()


def test_login():
    driver = define_driver()
    login(driver)

    wait = WebDriverWait(driver, 60)
    element = wait.until(wait_for_ajax_complete)

    if element:
        print('TEST LOGIN: PASSED')
    else:
        print('TEST LOGIN: FAILED')

    driver.save_screenshot('screenshot_test_result.png')

    driver.quit()


def test_login_with_wrong_credentials():
    driver = define_driver()
    login(driver, username='test', password='test')

    wait = WebDriverWait(driver, 60)

    api_response = wait.until(lambda d: wait_for_api_response(d, URLS['login']))

    driver.save_screenshot('failed_login.png')

    response_code = api_response['responseStatus']

    if response_code == 401:
        print('TEST WRONG LOGIN CREDENTIALS: PASSED')
    else:
        print('TEST WRONG LOGIN CREDENTIALS: FAILED')

    driver.quit()


def test_logout():
    driver = define_driver()
    login(driver)

    wait = WebDriverWait(driver, 60)
    wait.until(wait_for_ajax_complete)

    logout_button = driver.find_element('xpath', '//span[text()="Logout"]')
    logout_button.click()

    api_response = wait.until(lambda d: wait_for_api_response(d, URLS['logout']))

    if api_response['responseStatus'] == 200:
        driver.save_screenshot('screen_after_logout.png')
    else:
        print('TEST LOGOUT: FAILED')

    if str(driver.current_url) == URLS['login_page']:
        print('TEST LOGOUT: PASSED')
    else:
        print('TEST LOGOUT: FAILED')

    driver.quit()


def main():
    test_login()
    test_login_with_wrong_credentials()
    test_logout()


if __name__ == '__main__':
    main()
