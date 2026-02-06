import subprocess
import os
from unittest import result


def run_python_file(working_directory, file_path, args=None):
    try:
        # 1. Path Validation
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(file_path)
        # Check if the file is outside the permitted directory
        if os.path.commonpath([abs_working_dir]) != os.path.commonpath([abs_working_dir, abs_file_path]):
            return f'Error: Cannot run "{file_path}" as it is outside the permitted working directory'

        # 2. Directory Check
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not abs_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", abs_file_path]

        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = []
        

        return f'Successfully ran "{file_path}" with arguments: {args if args else "None"}'
    except Exception as e:
        return f"Error: {str(e)}"

run_python_file("calculator", "calculator/main.py")