import subprocess
from tabulate import tabulate  # Install this library using `pip install tabulate`

def get_regulator_details():
    try:
        # List all subdirectories in /sys/kernel/debug/regulator/
        result = subprocess.run(
            ["adb", "shell", "ls /sys/kernel/debug/regulator"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print("Error listing regulator directories:", result.stderr)
            return

        regulators = result.stdout.splitlines()
        print("Found regulators:\n", "\n".join(regulators))

        # Iterate through each regulator and fetch details
        for regulator in regulators:
            print(f"\n--- Regulator: {regulator} ---")

            # Fetch and parse the consumers file
            consumers_path = f"/sys/kernel/debug/regulator/{regulator}/consumers"
            consumers_result = subprocess.run(
                ["adb", "shell", f"cat {consumers_path}"],
                capture_output=True,
                text=True
            )
            if consumers_result.returncode == 0:
                consumers = consumers_result.stdout.strip()
                print("\nConsumers:")
                if "Device-Supply" in consumers:  # Parse consumer details if present
                    lines = consumers.splitlines()
                    headers = lines[0].split()  # Extract column headers
                    rows = [line.split() for line in lines[1:]]  # Extract data rows
                    print(tabulate(rows, headers=headers, tablefmt="grid"))
                else:
                    print(consumers)  # If no structured data, just print raw output
            else:
                print(f"Error reading consumers: {consumers_result.stderr}")

            # Fetch and display other subfiles
            for subfile in ["enable", "force_disable", "open_count", "use_count", "voltage"]:
                file_path = f"/sys/kernel/debug/regulator/{regulator}/{subfile}"
                file_result = subprocess.run(
                    ["adb", "shell", f"cat {file_path}"],
                    capture_output=True,
                    text=True
                )
                if file_result.returncode == 0:
                    content = file_result.stdout.strip()
                    print(f"{subfile.capitalize()}: {content}")
                else:
                    print(f"Error reading {subfile}: {file_result.stderr}")

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    get_regulator_details()

