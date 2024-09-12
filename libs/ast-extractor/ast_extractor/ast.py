import json
import subprocess

def filepath_vyper_to_ast(file_path):
    try:
        result = subprocess.run(
            ['vyper', '-f', 'ast', file_path],
            capture_output=True,
            text=True,
            check=True
        )
        ast = json.loads(result.stdout)
        return ast
    except subprocess.CalledProcessError as e:
        print(f"Error compiling Vyper code: {e.stderr}")
        return None