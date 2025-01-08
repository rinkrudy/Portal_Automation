import subprocess
from automation_script_executor import AutomationScriptExecutor
import yaml

class WorkflowExecutor:
    def __init__(self, workflow_file):
        self.workflow_file = workflow_file
        self.context = {}  # 공유 컨텍스트

    def execute_python_script(self, file_path, output_vars):
        # Python 스크립트 실행 (여기서는 subprocess로 실행하여 출력을 context에 저장)
        result = subprocess.run(["python", file_path], capture_output=True, text=True)
        print(f"Executed Python script: {file_path}")

        # Python 스크립트에서 반환한 출력 값을 context에 저장
        for var in output_vars:
            self.context[var] = result.stdout.strip()
            print(f"Stored in context: {var} = {self.context[var]}")

    def execute_ui_script(self, file_path):
        # UI 스크립트를 처리할 AutomationScriptExecutor 인스턴스를 생성하고 실행
        ui_executor = AutomationScriptExecutor(self.context)
        ui_executor.execute_script(file_path)

    def execute_workflow(self):
        # YAML 파일을 읽고 단계별로 실행
        with open(self.workflow_file, "r") as f:
            workflow = yaml.safe_load(f)

            for step in workflow["steps"]:
                step_type = step["type"]
                file_path = step["file"]

                if step_type == "python_script":
                    output_vars = step.get("output", [])
                    self.execute_python_script(file_path, output_vars)

                elif step_type == "ui_script":
                    # UI 스크립트에 input 변수를 전달
                    input_vars = step.get("input", [])
                    for var in input_vars:
                        if var in self.context:
                            print(f"Passing context variable '{var}' to UI script")
                    self.execute_ui_script(file_path)
                else:
                    print(f"Unknown step type: {step_type}")


