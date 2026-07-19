#!/usr/bin/env python3

import os
import yaml

# ==============================================================================
# CONFIGURATION
# Define the root directory to scan and the target timezone to validate.
# ==============================================================================
BASE_DIR = os.path.expanduser("~/docker-containers")
TARGET_TZ = "Asia/Kuala_Lumpur"

def validate_timezone_in_compose(file_path):
    """
    Parses a docker-compose file and validates if the target timezone 
    is configured correctly for every service defined within.
    
    Args:
        file_path (str): The absolute path to the docker-compose file.
        
    Returns:
        list: A list of service names lacking the required timezone configuration.
    """
    missing_services = []
    
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            
        # Verify if the parsed YAML structure contains the 'services' block
        if not data or 'services' not in data:
            return []
            
        for service_name, service_config in data['services'].items():
            has_timezone = False
            
            # Step 1: Evaluate the 'environment' configuration block
            if 'environment' in service_config:
                env = service_config['environment']
                
                # Handle dictionary format (e.g., TZ: Asia/Kuala_Lumpur)
                if isinstance(env, dict):
                    if env.get('TZ') == TARGET_TZ:
                        has_timezone = True
                
                # Handle list format (e.g., - TZ=Asia/Kuala_Lumpur)
                elif isinstance(env, list):
                    if any(f"TZ={TARGET_TZ}" in str(e) for e in env):
                        has_timezone = True
                        
            # Step 2: Evaluate the 'volumes' block for localtime mappings 
            # (Alternative method for timezone synchronization)
            if not has_timezone and 'volumes' in service_config:
                vols = service_config['volumes']
                if vols and any('/etc/localtime:/etc/localtime' in str(v) for v in vols):
                    has_timezone = True
                    
            # Log the service if no valid timezone configuration is detected
            if not has_timezone:
                missing_services.append(service_name)
                
    except Exception as e:
        print(f"[ERROR] Failed to parse {file_path}: {e}")
        
    return missing_services

def main():
    """
    Main execution function. Traverses the target directory, locates 
    docker-compose files, and triggers the validation process.
    """
    print(f"Scanning for docker-compose files in {BASE_DIR}...\n")
    all_compliant = True
    
    # Traverse the directory tree
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file in ['docker-compose.yml', 'docker-compose.yaml']:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, BASE_DIR)
                
                missing = validate_timezone_in_compose(full_path)
                
                # Output the validation results for the current file
                if missing:
                    all_compliant = False
                    print(f"[WARNING] ❌ {relative_path}")
                    for m in missing:
                        print(f"   └── Service '{m}' is missing TZ configuration.")
                else:
                    print(f"[OK] ✅ {relative_path} (All services compliant)")

    # Final summary report
    if all_compliant:
        print("\n🎉 EXCELLENT! All services have the correct Malaysia timezone configured.")
    else:
        print(f"\n⚠️ ACTION REQUIRED: Please add 'TZ={TARGET_TZ}' to the environment block for the flagged services.")

if __name__ == "__main__":
    main()
