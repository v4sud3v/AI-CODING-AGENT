import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        # 1. Path Validation
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(file_path)
        
        # Check if the file is outside the permitted directory
        if os.path.commonpath([abs_working_dir]) != os.path.commonpath([abs_working_dir, abs_file_path]):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # 2. Directory Check
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # 3. Ensure parent directories exist
        parent_dir = os.path.dirname(abs_file_path)
        os.makedirs(parent_dir, exist_ok=True)

        # 4. Write the file
        with open(abs_file_path, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file inside the working directory (creates parent directories as needed)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file",
            ),
        },
    ),
)