import os
# Assuming config.py exists as requested by the prompt
# from config import MAX_CHARS 
MAX_CHARS = 10000 

def get_file_content(working_directory, file_path):
    try:
        # 1. Normalize paths for the security check
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        # 2. Security check: Must be inside working directory
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # 3. Validation: Must be a regular file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # 4. Read file with truncation logic
        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content

    except Exception as e:
        return f"Error: {str(e)}"