import subprocess
import json
import re

def exec_slither(uri, workspace):
    try:
        process = subprocess.Popen(
            ["slither", uri, "--json", "result.json"],
            cwd=workspace,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        print(f"Failed to start Slither: {e}")
        return None

def parse_slither_out(uri, workspace):
    results = []

    process = exec_slither(uri, workspace)
    if not process:
        return results

    stdout, stderr = process.communicate()


    if process.returncode != 0:
        handle_slither_error(uri, workspace, stderr)
        return stderr

    # Parse the terminal output directly
    vulnerabilities = parse_terminal_output(stdout)
    results.extend(vulnerabilities)

    return results

def parse_terminal_output(output):
    results = []
    lines = output.splitlines()
    for line in lines:
        if "sends eth to arbitrary user" in line or \
           "incorrect ERC20 function interface" in line or \
           "ignores return value" in line or \
           "lacks a zero-check on" in line or \
           "Low level call" in line:
            results.append(line)
    return results

def handle_slither_error(uri, workspace, err_output):
    print(f"Vulnerabilities found: {err_output}")

def main():
    # uri = "contract.vy"  # without vulnerabilities
    uri = "vulnerable_contract.vy" # with vulnerabilities
    workspace = "/home/enzobonato/EIP/osmium-vyper/vscode/src/slither_test"
    vulnerabilities = parse_slither_out(uri, workspace)
    if not vulnerabilities:
        print("No Vulnerabilities found")

if __name__ == "__main__":
    main()
