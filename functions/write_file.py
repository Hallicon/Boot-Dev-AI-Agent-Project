import os
import pathlib
import io
from google.genai import types


# content is expected to be a string
def write_file(working_directory, file_path, content):
    try:
        absolute_path_wd = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(absolute_path_wd, file_path))

        if os.path.commonpath([absolute_path_wd, target_path]) != absolute_path_wd:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # If the path doesn't exist make the subdirectories
        if not os.path.exists(target_path):
            # Split the file name from the target path
            target_dir = os.path.dirname(target_path)
            # Make the directories up to that point
            os.makedirs(target_dir, exist_ok=True)

        # Write the file
        with open(target_path, "w", encoding="utf-8") as new_file:
            new_file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


# Create a schema using types.Function Declaration https://ai.google.dev/gemini-api/docs/function-calling?example=meeting#function-declarations, parameters is supposed to be a JSON object, that's why the type for it is OBJECT in the properties dictionary.
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write on"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file",
            )
        }
    )
)
