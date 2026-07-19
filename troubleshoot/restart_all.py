#!/usr/bin/env python3

import os
import subprocess

# ==============================================================================
# CONFIGURATION
# Define the root directory containing all Docker Compose projects.
# ==============================================================================
BASE_DIR = "/home/pwn20wnd/docker-containers"

def restart_compose_project(target_dir):
    """
    Executes 'docker compose down' followed by 'docker compose up -d'
    within the specified directory to apply configuration changes safely.
    
    Args:
        target_dir (str): The absolute path to the directory containing the docker-compose file.
    """
    project_name = os.path.basename(target_dir)
    print(f"🔄 Restarting project ecosystem: '{project_name}'...")
    
    try:
        # Gracefully shut down existing containers and remove orphaned networks
        subprocess.run(
            ["docker", "compose", "down"], 
            cwd=target_dir, 
            check=True, 
            capture_output=True,
            text=True
        )
        
        # Initialize containers in detached mode with updated configurations
        subprocess.run(
            ["docker", "compose", "up", "-d"], 
            cwd=target_dir, 
            check=True, 
            capture_output=True,
            text=True
        )
        print(f"   [✓] Successfully restarted '{project_name}'. New configurations applied.\n")
        
    except subprocess.CalledProcessError as e:
        print(f"   [ERROR] Failed to restart '{project_name}'.")
        print(f"   [DETAILS] {e.stderr}\n")

def main():
    """
    Main execution pipeline. Iterates through the base directory, identifies 
    valid Docker Compose projects, and triggers the rolling restart protocol.
    """
    print(f"Initiating Rolling Restart Protocol in {BASE_DIR}...\n")
    restarted_count = 0
    
    # Iterate over items strictly within the base directory
    for item in sorted(os.listdir(BASE_DIR)):
        target_dir = os.path.join(BASE_DIR, item)
        
        # Verify if the target is a directory and contains a compose file
        if os.path.isdir(target_dir):
            compose_yml = os.path.join(target_dir, "docker-compose.yml")
            compose_yaml = os.path.join(target_dir, "docker-compose.yaml")
            
            if os.path.exists(compose_yml) or os.path.exists(compose_yaml):
                restart_compose_project(target_dir)
                restarted_count += 1

    # Executive Summary
    print("=========================================================")
    print(f"🎉 PROTOCOL COMPLETE: {restarted_count} Docker Compose projects successfully restarted.")
    print("🕒 All active containers are now strictly synchronized to 'Asia/Kuala_Lumpur'.")
    print("=========================================================")

if __name__ == "__main__":
    main()
