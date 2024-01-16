import random
import string
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


URLS = {
    'login_page': 'https://bytepit.cloud/login',
    'login': 'https://bytepit.cloud/api/auth/login',
    'logout': 'https://bytepit.cloud/api/auth/logout',
    'register_page': 'https://bytepit.cloud/register',
    'register': 'https://bytepit.cloud/api/auth/register',
    'login_page_dev': 'https://dev.bytepit.cloud/login',
    'login_dev': 'https://dev.bytepit.cloud/api/auth/login',
    'create_problem': 'https://dev.bytepit.cloud/api/organiser/create-problem',
    'problems': 'https://dev.bytepit.cloud/api/problems'

}

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def generate_random_email():
    return f"{generate_random_string(7)}@example.com"

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


def login(driver, username='test', password='testtest', url=URLS['login_page']):
    driver.get(url)

    username_input_field = driver.find_element('name', 'username')
    password_input_field = driver.find_element('name', 'password')
    submit_button = driver.find_element('xpath', '//span[text()="Submit"]')

    username_input_field.send_keys(username)
    password_input_field.send_keys(password)

    submit_button.click()

def login_dev(driver, username='sipa', password='blablabla', url=URLS['login_page_dev']):
    driver.get(url)

    username_input_field = driver.find_element('name', 'username')
    password_input_field = driver.find_element('name', 'password')
    submit_button = driver.find_element('xpath', '//span[text()="Submit"]')

    username_input_field.send_keys(username)
    password_input_field.send_keys(password)

    submit_button.click()

def register(driver, email='test@test.com', name='Test', username='testuser', surname='User', password='testpass', role='Contestant'):
    driver.get(URLS['register_page'])

    dropdown = driver.find_element(By.ID, "role")
    dropdown.click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'dropdown') and .//div[text()='Contestant']]")))
    role_option = driver.find_element(By.XPATH, "//div[contains(@class, 'dropdown') and .//div[text()='Contestant']]")
    role_option.click()
    
    email_input_field = driver.find_element(By.NAME, 'email')
    name_input_field = driver.find_element(By.NAME, 'name')
    username_input_field = driver.find_element(By.NAME, 'username')
    surname_input_field = driver.find_element(By.NAME, 'surname')
    password_input_field = driver.find_element(By.NAME, 'password')
    
    submit_button = driver.find_element(By.XPATH, "//button[.//span[contains(text(), 'Submit')]]")
    
    email_input_field.send_keys(email)
    name_input_field.send_keys(name)
    username_input_field.send_keys(username)
    surname_input_field.send_keys(surname)
    password_input_field.send_keys(password)

    submit_button.click()

def set_points_value(driver, value):
    
    points_input_js = f"document.querySelector('input#minmaxfraction').value = '{value}';"
    driver.execute_script(points_input_js)

def create_problem(driver, name, description, points, runtime_limit, example_input, example_output, is_private, is_hidden, input_file_path, output_file_path):
    driver.get(URLS['login_page_dev'])  
    username_input_field = driver.find_element('name', 'username')
    password_input_field = driver.find_element('name', 'password')
    username_input_field.send_keys('sipa')
    password_input_field.send_keys('blablabla')
    
    submit_button = driver.find_element('xpath', '//span[text()="Submit"]')
    submit_button.click()
    
    time.sleep(10)
    
    driver.get('https://dev.bytepit.cloud/organiser/create-problem')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'name'))
    )

    
    name_input_field = driver.find_element(By.NAME, 'name')
    description_input_field = driver.find_element(By.NAME, 'description')
    all_minmaxfraction_inputs = driver.find_elements(By.ID, 'minmaxfraction')
    points_input_field = all_minmaxfraction_inputs[0]  
    runtime_limit_input_field = all_minmaxfraction_inputs[1]  

    
    points_input_field.clear()
    points_input_field.send_keys(int(points))
    
    runtime_limit_input_field.clear()
    runtime_limit_input_field.send_keys(runtime_limit)
    
    example_input_textarea = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, 'exampleInput'))
    )

    example_output_textarea = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, 'exampleOutput'))
    )   

    example_input_textarea.send_keys(example_input)
    example_output_textarea.send_keys(example_output)
    
    if is_private:
        
        private_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(text(),'Private')]/following-sibling::div//div[contains(@class,'radiobutton')]"))
        )
        
        private_option.click()
    else:
        
        public_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(text(),'Private')]/following-sibling::div//div[contains(@class,'radiobutton-checked')]"))
        )
        
        public_option.click()

   
    if is_hidden:
        hidden_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(text(),'Hidden')]/following-sibling::div//div[contains(@class,'radiobutton')]"))
        )
        hidden_option.click()
    else:
        visible_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(text(),'Hidden')]/following-sibling::div//div[contains(@class,'radiobutton-checked')]"))
        )
        visible_option.click()

    test_files_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "testFiles"))
    )
    test_files_input.send_keys(input_file_path + "\n" + output_file_path)

    name_input_field.send_keys(name)
    description_input_field.send_keys(description)

    submit_button = driver.find_element(By.XPATH, "//button[.//span[contains(text(), 'Submit')]]")
    driver.save_screenshot('test_screenshots/submit.png')
    submit_button.click()
    driver.save_screenshot('test_screenshots/submit2.png')

def test_login():
    driver = define_driver()
    login(driver)

    wait = WebDriverWait(driver, 60)
    element = wait.until(wait_for_ajax_complete)

    if element:
        print('TEST LOGIN: PASSED')
    else:
        print('TEST LOGIN: FAILED')

    driver.save_screenshot('test_screenshots/screenshot_test_result.png')

    driver.quit()


def test_login_with_wrong_credentials():
    driver = define_driver()
    login(driver, username='test', password='test')

    wait = WebDriverWait(driver, 60)

    api_response = wait.until(lambda d: wait_for_api_response(d, URLS['login']))

    driver.save_screenshot('test_screenshots/failed_login.png')

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
        driver.save_screenshot('test_screenshots/screen_after_logout.png')
    else:
        print('TEST LOGOUT: FAILED')

    if str(driver.current_url) == URLS['login_page']:
        print('TEST LOGOUT: PASSED')
    else:
        print('TEST LOGOUT: FAILED')

    driver.quit()



def test_register_already_exists():
    driver = define_driver()
    register(driver, email='existinguser@example.com', name='Test', username='existinguser', surname='User', password='testpassword', role='Contestant')
    wait = WebDriverWait(driver, 10)
    api_response = wait.until(lambda d: wait_for_api_response(d, URLS['register']))
    driver.save_screenshot('test_screenshots/registration_already_exists_test_result.png')
    
    if api_response['responseStatus'] == 400:
        print('TEST REGISTER ALREADY EXISTS: PASSED')
    else:
        print('TEST REGISTER ALREADY EXISTS: FAILED - Unexpected Response Status:', api_response['responseStatus'])
    
    driver.quit()

def test_register_new_user():
    driver = define_driver()
    attempt_count = 3 

    for attempt in range(attempt_count):
        try:
            random_username = generate_random_string(8)
            random_email = generate_random_email()
            register(driver, email=random_email, name='Test', username=random_username, surname='User', password='testpassword', role='Contestant')
            wait = WebDriverWait(driver, 20)  
            api_response = wait.until(lambda d: wait_for_api_response(d, URLS['register']))
            driver.save_screenshot('test_screenshots/registration_new_user_test_result.png')
            
            if api_response['responseStatus'] == 201:
                print('TEST REGISTER NEW USER: PASSED')
                break
            else:
                print(f'TEST REGISTER NEW USER: FAILED - Response Status: {api_response["responseStatus"]}')
                if attempt < attempt_count - 1:
                    print("Retrying registration...")
                else:
                    print("All attempts failed.")

        except TimeoutException as e:
            print(f'TEST REGISTER NEW USER: ATTEMPT {attempt + 1} - Timeout Exception: {e}')
            if attempt < attempt_count - 1:
                print("Retrying registration...")
            else:
                print("All attempts failed.")
        finally:
            driver.quit()

def test_create_problem():
    driver = define_driver()
    
    try:
        
        input_file_path = '/home/fran/Desktop/progi/bytepit-root/dokumentacija/test_input_files/1_in.txt'  
        output_file_path = '/home/fran/Desktop/progi/bytepit-root/dokumentacija/test_input_files/1_out.txt'  
        
        create_problem(
            driver,
            name='Test Problem',
            description='This is a test problem.',
            points=10,
            runtime_limit=1.0,
            example_input='1\n2\n',
            example_output='3\n',
            is_private=True,
            is_hidden=False,
            input_file_path=input_file_path,
            output_file_path=output_file_path
        )
        
        wait = WebDriverWait(driver, 30)
        api_response = wait.until(lambda d: wait_for_api_response(d, URLS['problems']))
        response_status = api_response.get('responseStatus', None)
        driver.save_screenshot('test_screenshots/create_problem_test1.png')

        if response_status == 422:
            print('TEST CREATE PROBLEM: PASSED')
        else:
            print(f"TEST CREATE PROBLEM: FAILED - Response Status: {response_status}")
        
            error_details = api_response.get('responseText', {}).get('errors', 'Unknown error')
            print(f"Error details: {error_details}")


        
    except TimeoutException as e:
        print(f'TEST CREATE PROBLEM: FAILED - Timeout Exception: {e}')
    except Exception as e:
        print(f'TEST CREATE PROBLEM: FAILED - {str(e)}')
    finally:
        driver.quit()


def main():
    test_login()
    test_login_with_wrong_credentials()
    test_logout()
    test_register_already_exists()
    test_register_new_user()
    test_create_problem()

if __name__ == '__main__':
    main()

