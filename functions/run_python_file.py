import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        # 1. Security Check: Ensure path is within the working directory
        abs_working_dir = os.path.abspath(working_directory)
        absolute_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
        
        if not absolute_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # 2. File Check: Must exist and be a regular file
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # 3. Extension Check: Must be a .py file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # 4. Build the command
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)

        # 5. Execute via Subprocess
        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        # 6. Build Output String
        output_parts = []
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        
        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file located inside the working directory and return its combined stdout/stderr output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of string arguments to pass to the script",
            ),
        },
    ),
)