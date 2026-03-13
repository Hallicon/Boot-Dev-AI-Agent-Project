from pathlib import Path

import os
import io
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([target_path, working_directory]) != working_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isfile(target_path) is False:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path, "r", encoding="utf-8") as file_in_question:
            content = str(file_in_question.read(10000))

            if file_in_question.read(1):
                content += f'[...File "{file_path}" truncated at 10000 characters]'
            return content
    except Exception as e:
        return f"Error: {e}"


# Create a schema using types.Function Declaration https://ai.google.dev/gemini-api/docs/function-calling?example=meeting#function-declarations, parameters is supposed to be a JSON object, that's why the type for it is OBJECT in the properties dictionary.
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the contents inside of the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file."
            )
        }
    )
)
