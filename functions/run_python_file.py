import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        wd_abs_path = os.path.abspath(working_directory)
        full_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([wd_abs_path, full_file_path]) != wd_abs_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_file_path) or not os.path.isfile(full_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path[-3:] != '.py':
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", full_file_path]

        if args is not None:
            command.extend(args)

        final_command = command

        result = subprocess.run(
            final_command,
            cwd=wd_abs_path,            # Sets the working directory
            capture_output=True,     # Captures stdout and stderr
            text=True,               # Decodes output to strings (not bytes)
            timeout=30               # Sets a 30-second timeout
        )

        output = []

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if result.stdout == "" and result.stderr == "":
            output.append(f"No output produced")
        elif result.stdout != "":
            output.append("STDOUT:" + result.stdout)
        elif result.stderr != "":
            output.append("STDERR:" + result.stderr)

        return "\n".join(output)

    except Exception as e:
        return f"Error: {e}"


# Create a schema using types.Function Declaration https://ai.google.dev/gemini-api/docs/function-calling?example=meeting#function-declarations, parameters is supposed to be a JSON object, that's why the type for it is OBJECT in the properties dictionary.
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="A function to run a python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that must be executed."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                # items expects a schema
                items=types.Schema(type=types.Type.STRING),
                description="The arguments to be passed into the running file.",
            )
        }
    )
)
