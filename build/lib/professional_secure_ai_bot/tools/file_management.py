import os
import subprocess
from langchain.agents import tool
from werkzeug.utils import safe_join


@tool
def get_filenames_in_directory() -> list:
    """
    Retrieves a list of filenames in the files directory.
    :return: A list of filenames found in the directory.
    """
    file_path = "./textfiles"
    try:
        entries = os.listdir(file_path)
        return entries
    except Exception as e:
        return f"An error occurred: {str(e)}"


@tool
def get_file_content(filename: str) -> str:
    """
    Retrieves the content of a text file given its filename.

    :param filename: The name of the file to read.
    :return: The content of the file as a string, or None if the file cannot be read.
    """
    FILE_DIR = "./textfiles"

    filepath = safe_join(FILE_DIR, filename)

    if not os.path.exists(filepath):
        return "File does not exist."

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except (
        Exception
    ) as e:  # Catch any exception, e.g., permission issues, and handle it
        return f"An error occurred while reading the file: {str(e)}"

@tool
def delete_file(filename: str) -> str:
    """
    Deletes a specified file from the files directory.
    
    :param filename: The name of the file to delete.
    :return: Success message or error information.
    """
    from werkzeug.utils import safe_join
    
    FILE_DIR = "./textfiles"
    filepath = safe_join(FILE_DIR, filename)
    
    if not os.path.exists(filepath):
        return f"Error: File '{filename}' does not exist."
    
    try:
        os.remove(filepath)
        return f"File '{filename}' has been successfully deleted."
    except PermissionError:
        return f"Error: Permission denied when deleting file '{filename}'."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    
@tool
def create_file(filename: str, content: str) -> str:
    """
    Creates a new file with specified content in the files directory.
    
    :param filename: The name of the file to create.
    :param content: The content to write into the file.
    :return: Success message or error information.
    """
    from werkzeug.utils import safe_join
    
    FILE_DIR = "./textfiles"
    filepath = safe_join(FILE_DIR, filename)
    
    # 检查文件是否存在
    if os.path.exists(filepath):
        return f"Error: File '{filename}' already exists."
    
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        return f"File '{filename}' has been successfully created."
    except PermissionError:
        return f"Error: Permission denied when creating file '{filename}'."
    except FileNotFoundError:
        # 处理目录不存在的情况
        return f"Error: Directory not found. Please ensure '{FILE_DIR}' exists."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

@tool
def execute_linux_command(command: str) -> str:
    """
    Executes a Linux shell command and returns the output.

    :param command: The Linux command to execute.
    :return: The output of the command as a string, or an error message if execution fails.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Command failed with error: {e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"