import subprocess
import json

def exec_slither(uri, workspace):
    try:
        process = subprocess.Popen(
            ["slither", uri, "--exclude", "naming-convention", "--json", "-"],
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
    output_dict = {"stdout": "", "stderr": ""}
    
    process = exec_slither(uri, workspace)
    if not process:
        return output_dict

    stdout, stderr = process.communicate()
    output_dict["stdout"] = stdout
    output_dict["stderr"] = stderr  

    if not stdout.strip():
        return []

    filtered_data = parse_json_output(stdout)
    return filtered_data

def parse_json_output(output):
    vulnerabilities = []

    try:
        vulnerabilities_json = json.loads(output)
        detectors = vulnerabilities_json.get("results", {}).get("detectors", [])
        
        for detector in detectors:
            if isinstance(detector, dict):
                impact = detector.get("impact", "Unknown")
                description = detector.get("description", "Unknown")
                for element in detector.get("elements", []):
                    if element.get("type") == "node":
                        filtered_element = {
                            "message": description,
                            "start": element.get("source_mapping", {}).get("start"),
                            "length": element.get("source_mapping", {}).get("length"),
                            "severity": impact
                        }
                        vulnerabilities.append(filtered_element)
            else:
                print(f"Unexpected detector type: {type(detector)}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

    return vulnerabilities

def main():
    # uri = "Contract.vy"  # without vulnerabilities
    uri = "vulnerable_contract.vy"  # with vulnerabilities
    workspace = "/home/enzobonato/EIP/osmium-vyper/vscode/src/slither_test"
    
    filtered_data = parse_slither_out(uri, workspace)
    
    # DEBUG TO CHECK IF THERE ARE VULNERABILITIES
    if not filtered_data:
        print("No vulnerabilities found")
    else:
        print("Vulnerabilities found")
    print(json.dumps(filtered_data, indent=2))
    # END OF DEBUG

if __name__ == "__main__":
    main()
