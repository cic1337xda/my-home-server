#!/usr/bin/env python3

import os
import yaml
import shutil

# ==============================================================================
# CONFIGURATION & INITIALIZATION
# Define the root directory to scan and the target timezone to enforce.
# ==============================================================================
BASE_DIR = "/home/pwn20wnd/docker-containers"
TARGET_TZ = "Asia/Kuala_Lumpur"

def inject_timezone(file_path):
    """
    Parses a docker-compose file, validates the timezone configuration, 
    and systematically injects the required TZ variable if absent.
    Creates a backup of the original file prior to modification.
    
    Args:
        file_path (str): The absolute path to the docker-compose file.
        
    Returns:
        bool: True if modifications were made, False otherwise.
    """
    modified = False
    
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            
        if not data or 'services' not in data:
            return False
            
        for service_name, service_config in data['services'].items():
            has_timezone = False
            
            # Step 1: Evaluate existing environment variables
            if 'environment' in service_config:
                env = service_config['environment']
                if isinstance(env, dict) and env.get('TZ') == TARGET_TZ:
                    has_timezone = True
                elif isinstance(env, list) and any(f"TZ={TARGET_TZ}" in str(e) for e in env):
                    has_timezone = True
                    
            if not has_timezone and 'volumes' in service_config:
                vols = service_config['volumes']
                if vols and any('/etc/localtime:/etc/localtime' in str(v) for v in vols):
                    has_timezone = True

            # Step 2: Inject the timezone variable if missing
            if not has_timezone:
                if 'environment' not in service_config:
                    service_config['environment'] = []
                
                env = service_config['environment']
                if isinstance(env, list):
                    env.append(f"TZ={TARGET_TZ}")
                elif isinstance(env, dict):
                    env['TZ'] = TARGET_TZ
                
                modified = True
                print(f"   [+] Injected TZ into service: '{service_name}'")

        # Step 3: Write changes to disk with a safety backup
        if modified:
            backup_path = f"{file_path}.bak"
            shutil.copy2(file_path, backup_path)
            
            with open(file_path, 'w') as file:
                # Use default_flow_style=False to maintain clean YAML block formatting
                yaml.dump(data, file, default_flow_style=False, sort_keys=False)
                
    except Exception as e:
        print(f"[ERROR] Failed to process {file_path}: {e}")
        
    return modified

def main():
    """
    Main execution pipeline. Traverses the target directory, identifies 
    docker-compose files, and initiates the remediation protocol.
    """
    print(f"Initiating Automated Timezone Remediation Protocol in {BASE_DIR}...\n")
    fixed_count = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file in ['docker-compose.yml', 'docker-compose.yaml']:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, BASE_DIR)
                
                print(f"Scanning ➔ {relative_path}")
                if inject_timezone(full_path):
                    fixed_count += 1
                    print(f"   [✓] Successfully updated and backed up to .bak\n")

    # Executive Summary
    print("=========================================================")
    if fixed_count > 0:
        print(f"🎉 REMEDIATION COMPLETE: {fixed_count} Compose files were successfully patched.")
        print("ℹ️ Note: Original files were backed up with a '.bak' extension.")
        print("⚠️ ACTION REQUIRED: To apply changes, run: docker compose down && docker compose up -d")
    else:
        print("✅ NO ACTION REQUIRED: All services are already compliant.")
    print("=========================================================")

if __name__ == "__main__":
    main()
