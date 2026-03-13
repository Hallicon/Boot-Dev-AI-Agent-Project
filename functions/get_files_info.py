from pathlib import Path
from google.genai import types
import os


def get_files_info(working_directory, directory="."):
    try:
        # Looks in current working directory
        absolute_path = os.path.abspath(working_directory)

        # If cwd is "super" and desired dir is "waffles" make /super/waffles
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))

        check = os.path.commonpath([absolute_path, target_dir]) == absolute_path
        if check is False:
            return f"\tError: Cannot list \"{directory}\" as it is outside the permitted working directory"

        if not Path(target_dir).is_dir():
            return f"Error: \"{directory}\" is not a directory"

        contents = os.listdir(target_dir)
        sought = []

        for item in contents:
            is_dir = Path(target_dir, item).is_dir()
            item_size = os.lstat(os.path.join(target_dir, item)).st_size
            entry = f"- {item}: file_size={item_size} bytes, is_dir={is_dir}"
            sought.append(entry)
        final_output = "\n".join(sought)

        # Debugging
        # print(f"{final_output}")

        return final_output
    except Exception as e:
        return f"Error: {e}"


# Create a schema using types.Function Declaration https://ai.google.dev/gemini-api/docs/function-calling?example=meeting#function-declarations, parameters is supposed to be a JSON object, that's why the type for it is OBJECT in the properties dictionary.
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
