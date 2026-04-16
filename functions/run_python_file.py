import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    if not file_path.startswith(working_directory):
        return f'Cannot execute "{file_path}" as it is outside'

    if not os.path.isfile(file_path):
        return f'"{os.path.basename(file_path)}" does not exist'

    if not file_path.endswith(".py"):
        return f'"{os.path.basename(file_path)}" is not a Python file'

    try:
        command = ["python", file_path]
        if args:
            command.extend(args)

        result = subprocess.run(
            command, cwd=working_directory, capture_output=True, text=True, timeout=30
        )

        output_parts = []

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT: {result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR: {result.stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
