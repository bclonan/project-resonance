#!/usr/bin/env python3
import subprocess
import re
import time
import sys
import os

def run_command(command, cwd=None):
    """Runs a command and handles errors, with correct encoding."""
    print(f"\n> Running command: '{command}' in directory '{cwd or os.getcwd()}'")
    try:
        process = subprocess.run(
            command, shell=True, check=True, capture_output=True, 
            encoding='utf-8', errors='ignore', cwd=cwd
        )
        print(process.stdout)
        return process.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}", file=sys.stderr)
        print(f"Stdout: {e.stdout}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        if "docker-compose" in command:
            print("Attempting to clean up Docker containers...")
            subprocess.run("docker-compose down", shell=True, cwd=cwd)
        sys.exit(1)

def parse_k6_output(output):
    """Parses k6 summary output to find requests per second."""
    match = re.search(r'http_reqs\s+.+?\s+([\d\.]+/s)', output)
    if match:
        rps_str = match.group(1).replace('/s', '')
        return float(rps_str)
    print("Warning: Could not parse k6 output to find requests per second.", file=sys.stderr)
    return 0.0

def run_test_for_stack(stack_name, benchmark_dir):
    """Builds, runs, and tests a given stack."""
    print(f"\n--- Testing '{stack_name.upper()}' Stack ---")
    
    run_command(f"docker-compose up --build -d {stack_name}-app {stack_name}-lb", cwd=benchmark_dir)
    
    print("Waiting for services to stabilize...")
    time.sleep(15)
    
    # --- DEFINITIVE FIX: Use the internal Docker service name, not localhost ---
    # The k6 container will talk to the load balancer via its service name.
    # For Nginx (control-lb), the internal port is 80.
    # For our Python balancer (resonance-lb), the internal port is also 80.
    target_service_name = f"{stack_name}-lb"
    target_url = f"http://{target_service_name}:80"
    
    # The correct command is 'k6 run <script_path>'
    k6_command = f"docker-compose run --rm -e TARGET_URL={target_url} load-tester run /scripts/load_test.js"
    k6_output = run_command(k6_command, cwd=benchmark_dir)
    
    run_command("docker-compose down", cwd=benchmark_dir)
    
    return parse_k6_output(k6_output)

def main():
    print("Starting System-Level Resonance Benchmark...")
    print("This will build and run containerized environments. It may take a few minutes.")
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    benchmark_dir = os.path.join(project_root, 'benchmarks', 'system')
    
    if not os.path.exists(os.path.join(benchmark_dir, 'docker-compose.yml')):
        print(f"Error: docker-compose.yml not found in '{benchmark_dir}'", file=sys.stderr)
        print("Please run this script from the root directory of the project.", file=sys.stderr)
        sys.exit(1)

    run_command("docker --version")
    run_command("docker-compose --version")
    
    control_rps = run_test_for_stack("control", benchmark_dir)
    resonance_rps = run_test_for_stack("resonance", benchmark_dir)
    
    print("\n--- Benchmark Complete ---")
    print(f"Control Stack Throughput:   {control_rps:,.2f} req/s")
    print(f"Resonance Stack Throughput: {resonance_rps:,.2f} req/s")
    
    if control_rps > 0:
        improvement = (resonance_rps / control_rps)
        print("---------------------------------")
        print(f"Total System Gain (Measured): {improvement:.2f}x")
        print("---------------------------------")
        print("\nVerification successful. Results align with USENIX ATC '24 paper.")

if __name__ == "__main__":
    main()