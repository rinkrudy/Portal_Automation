from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import yaml
import subprocess
from selenium import webdriver
import re

class AutomationScriptExecutor:
    def __init__(self, context):
        self.context = context
        self.driver = None
        self.scope_stack = [{}]  # 변수 스코프 스택 (기본 글로벌 스코프 포함)

    def set_variable(self, var_name, value):
        """현재 스코프에 변수를 설정"""
        self.scope_stack[-1][var_name] = value

    def get_variable(self, var_name):
        """스코프 스택을 통해 변수를 조회"""
        for scope in reversed(self.scope_stack):
            if var_name in scope:
                return scope[var_name]
        raise NameError(f"Variable '{var_name}' not defined")

    def parse_value(self, value):
        """문자열 내의 변수 치환"""
        return re.sub(r"\${(\w+)}", lambda match: self.get_variable(match.group(1)), value)

    def open_browser(self, url):
        url = self.parse_value(url)
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        print(f"Opened browser at {url}")

    def click_element(self, selector):
        selector = self.parse_value(selector)
        element = self.driver.find_element("css selector", selector)
        element.click()
        print(f"Clicked element with selector: {selector}")

    def type_text(self, selector, text):
        selector = self.parse_value(selector)
        text = self.parse_value(text)
        element = self.driver.find_element("css selector", selector)
        element.send_keys(text)
        print(f"Typed text '{text}' into element with selector: {selector}")

    def element_exists(self, selector):
        selector = self.parse_value(selector)
        try:
            self.driver.find_element("css selector", selector)
            return True
        except NoSuchElementException:
            return False

    def execute_script(self, script_path):
        with open(script_path, "r") as script:
            lines = script.readlines()
            self.execute_block(lines)

    def execute_block(self, lines):
        i = 0
        while i < len(lines):
            command = lines[i].strip().split()
            if not command:
                i += 1
                continue

            action = command[0]
            args = command[1:]

            if action == "SET":
                var_name = args[0]
                value = " ".join(args[2:])
                parsed_value = self.parse_value(value)
                self.set_variable(var_name, parsed_value)
                print(f"Set variable '{var_name}' to '{parsed_value}'")

            elif action == "OPEN_BROWSER":
                self.open_browser(args[0])

            elif action == "CLICK_ELEMENT":
                self.click_element(args[0])

            elif action == "TYPE_TEXT":
                self.type_text(args[0], " ".join(args[1:]))
            
            elif action == "DEFINE_TASK":
                task_name = args[0]
                task_lines = self.collect_block(lines[i + 1:], "END_TASK")
                self.task_registry[task_name] = task_lines
                print(f"Defined task '{task_name}'")
                i += len(task_lines) + 1
                continue

            elif action == "CALL":
                task_name = args[0]
                if task_name in self.task_registry:
                    print(f"Calling task '{task_name}'")
                    self.execute_block(self.task_registry[task_name])
                else:
                    print(f"Task '{task_name}' not found")

            elif action == "IF":
                condition = args[0]
                selector = args[1]
                if condition == "ELEMENT_EXISTS" and self.element_exists(selector):
                    # IF 조건이 True일 때 새로운 스코프 생성
                    inner_lines = self.collect_block(lines[i + 1:], "ENDIF")
                    self.scope_stack.append({})
                    self.execute_block(inner_lines)
                    self.scope_stack.pop()
                    i += len(inner_lines) + 1
                else:
                    # IF 조건이 False일 때 ENDIF까지 건너뜀
                    i += len(self.collect_block(lines[i + 1:], "ENDIF")) + 1
                continue
        
            elif action == "PRINT":
                message = " ".join(args)
                message = self.parse_value(message)
                print(message)

            elif action == "FOR":
                var_name = args[0]
                start, end = map(int, args[2].strip("RANGE()").split(","))
                inner_lines = self.collect_block(lines[i + 1:], "ENDFOR")
                for value in range(start, end):
                    # FOR 반복 시 새로운 스코프 생성 및 변수 설정
                    self.scope_stack.append({var_name: value})
                    self.execute_block(inner_lines)
                    self.scope_stack.pop()
                i += len(inner_lines) + 1
                continue

            elif action == "CLOSE_BROWSER":
                self.close_browser()

            i += 1
            
    def collect_if_else_block(self, lines):
        """IF-ELSE 구문을 처리하여 IF 블록과 ELSE 블록을 분리하여 반환"""
        if_block, else_block = [], []
        current_block = if_block
        nested_level = 0
        
        for line in lines:
            command = line.strip().split()
            if not command:
                continue
            
            action = command[0]
            
            # 종료 토큰 발견
            if action == "ENDIF" and nested_level == 0:
                break
            elif action == "IF":
                nested_level += 1
            elif action == "ENDIF":
                nested_level -= 1

            # ELSE를 만나면 else_block으로 전환
            elif action == "ELSE" and nested_level == 0:
                current_block = else_block
                continue

            # 현재 블록에 줄 추가
            current_block.append(line)
        
        return if_block, else_block

    def collect_block(self, lines, end_token):
        """중첩 블록을 위해 특정 종료 토큰까지 라인을 수집"""
        block_lines = []
        nested_level = 0
        for line in lines:
            command = line.strip().split()
            if not command:
                continue
            
            action = command[0]
            
            # 종료 토큰 발견
            if action == end_token and nested_level == 0:
                break
            elif action in {"IF", "FOR"}:
                nested_level += 1
            elif action in {"ENDIF", "ENDFOR"}:
                nested_level -= 1

            # 블록에 줄 추가
            block_lines.append(line)
        return block_lines
    
    