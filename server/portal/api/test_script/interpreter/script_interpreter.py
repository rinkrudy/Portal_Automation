import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import time
import json
import openpyxl

# Define EdgeDriver and ChromeDriver classes
class BrowserDriver:
    def get_options(self, background_mode=False, window_size="1920,1080"):
        options = self.create_options()
        if background_mode:
            options.add_argument('--headless')
        options.add_argument(f'--window-size={window_size}')
        return options

class EdgeDriver(BrowserDriver):
    def create_options(self):
        return EdgeOptions()

    def start_driver(self, background_mode=False, window_size="1920,1080"):
        options = self.get_options(background_mode=background_mode, window_size=window_size)
        edge_service = EdgeService()
        driver = webdriver.Edge(service=edge_service, options=options)
        print("Edge 브라우저 드라이버 시작됨")
        return driver

class ChromeDriver(BrowserDriver):
    def create_options(self):
        return ChromeOptions()

    def start_driver(self, background_mode=False, window_size="1920,1080"):
        options = self.get_options(background_mode=background_mode, window_size=window_size)
        chrome_service = ChromeService()
        driver = webdriver.Chrome(service=chrome_service, options=options)
        print("Chrome 브라우저 드라이버 시작됨")
        return driver

def read_excel(filepath, sheet_name):
    return pd.read_excel(filepath, sheet_name=sheet_name)

def parse_selectors(selector_data_path):
    with open(selector_data_path, 'r', encoding='utf-8') as json_file:
        selector_data = json.load(json_file)
    parsed_selectors = {}
    
    def flatten_selectors(prefix, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'ui':
                    for ui_key, ui_value in value.items():
                        print(ui_key)
                        combined_key = f"{prefix}_{ui_key}"
                        by_type = ui_value['type'].lower() == 'xpath'
                        by = By.XPATH
                        if by_type == "css":
                            by = By.CSS_SELECTOR
                        elif by_type == "name":
                            by = By.NAME
                        elif by_type == "id":
                            by = By.ID
                        parsed_selectors[combined_key.lower()] = (by, ui_value['selector'])
                else:
                    flatten_selectors(f"{prefix}_{key}", value)
    
    for key, value in selector_data.items():
        flatten_selectors(key.lower(), value)
    
    return parsed_selectors

# Interpreter function
def interpret_script(script_path, selector_data_path):
    selectors = parse_selectors(selector_data_path)
    
    with open(script_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    drivers = {}
    variables = {}
    imported_scripts = {}

    def resolve_variable(expression):
        if expression.startswith('${') and expression.endswith('}'):
            # Extract variable name from expression like ${variable_name}
            key, subkey = expression[2:-1].split(':')
            return selectors.get(f"{key}_{subkey}".lower())
        elif expression.startswith('"') and expression.endswith('"'):
            return expression[1:-1]
        else:
            return variables.get(expression, expression)

    def execute_script(script_path, args, output_var):
        with open(script_path, 'r') as script_file:
            script_lines = script_file.readlines()
            local_vars = {}
            for line in script_lines:
                line = line.strip()
                if line.startswith('ARGUMENTS'):
                    # Extract arguments
                    continue
                elif line.startswith('ON_BROWSER'):
                    driver = args.get('driver')
                    if driver is None:
                        raise ValueError("Driver not provided in arguments")
                    local_vars['driver'] = driver
                elif line.startswith('DELAY'):
                    delay_time = line.split(' ')[1]
                    minutes, seconds = map(int, delay_time.split(':'))
                    time.sleep(minutes * 60 + seconds)
                elif line.startswith('CLICK_ELEMENT'):
                    by, selector = resolve_variable(line.split(' ')[1])
                    driver.find_element(by, selector).click()
                elif line.startswith('NAVIGATE'):
                    site_url = resolve_variable(line.split(' ')[1])
                    print(site_url)
                    driver.get(site_url)
                elif line.startswith('TYPE_INTO'):
                    by, selector = resolve_variable(line.split(' ')[1])
                    text = args.get('id', '')
                    driver.find_element(by, selector).send_keys(text)
                elif line.startswith('TYPE_PASSWORD'):
                    by, selector = resolve_variable(line.split(' ')[1])
                    password = args.get('pw', '')
                    driver.find_element(by, selector).send_keys(password)
                elif '=' in line:
                    var_name, value = line.split('=', 1)
                    local_vars[var_name.strip()] = resolve_variable(value.strip())
            variables[output_var] = local_vars.get('successful', True)

    for line in lines:
        line = line.strip()
        if line.startswith('IMPORT'):
            # Handle imports
            match_import = re.match(r'IMPORT "(.+)" AS (.+)', line)
            if match_import:
                script_path, alias = match_import.groups()
                imported_scripts[alias] = script_path

        # Match commands like SET or ON_BROWSER
        match_set = re.match(r'SET (\w+) = (.+)', line)
        match_on_browser = re.match(r'ON_BROWSER (\w+)', line)
        match_function_call = re.match(r'(\w+)\((.*)\s*\|\s*(\w+)\)', line)

        if match_set:
            var_name, expression = match_set.groups()
            if expression.startswith('BROWSER_EDGE') or expression.startswith('BROWSER_CHROME'):
                # Handle browser setup commands
                browser_command = expression.split('(')[0]
                args_str = expression.split('(')[1].replace(')', '')
                args = {}
                for arg in args_str.split(', '):
                    key, value = arg.split('=')
                    args[key.strip()] = value.strip() == 'TRUE'
                if browser_command == 'BROWSER_EDGE':
                    driver = EdgeDriver().start_driver(background_mode=args.get('BACKGROUND', False), window_size="1920,1080" if args.get('MAXIMIZE', False) else "")
                elif browser_command == 'BROWSER_CHROME':
                    driver = ChromeDriver().start_driver(background_mode=args.get('BACKGROUND', False), window_size="1920,1080" if args.get('MAXIMIZE', False) else "")
                drivers[var_name] = driver
            elif expression.startswith('READ_EXCEL'):
                # Handle read excel command
                filepath_match = re.search(r'READ_EXCEL\("(.*?)"', expression)
                sheet_name_match = re.search(r'SHEET_NAME\s*=\s*(.*)\)', expression)
                if filepath_match and sheet_name_match:
                    filepath = filepath_match.group(1)
                    sheet_name = sheet_name_match.group(1).strip()
                    if sheet_name.startswith('"') and sheet_name.endswith('"'):
                        sheet_name = sheet_name[1:-1]
                    else:
                        sheet_name = variables.get(sheet_name, sheet_name)
                    variables[var_name] = read_excel(filepath, sheet_name)
            else:
                # Handle simple variable assignments
                variables[var_name] = resolve_variable(expression)
        elif match_on_browser:
            driver_name = match_on_browser.groups()[0]
            driver = drivers.get(driver_name)
            if driver:
                # Use driver for automation (no specific action in script, placeholder)
                pass
        elif match_function_call:
            func_name, args_str, output_var = match_function_call.groups()
            if func_name in imported_scripts:
                script_path = imported_scripts[func_name]
                args = dict(arg.split('=') for arg in args_str.split(', '))
                args = {k.strip(): resolve_variable(v.strip()) for k, v in args.items()}
                args['driver'] = drivers.get(args['driver'])
                execute_script(script_path, args, output_var)

    # Cleanup
    for driver in drivers.values():
        driver.quit()

if __name__ == "__main__":
    interpret_script("../test_ui_script/test_ui_script_copy.as", "C:/Users/User/Documents/Code/Projects/RPA/Portal/server/portal/api/test_script/resource/ui_info.json")
