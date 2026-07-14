#!/usr/bin/env python3
"""
Interactive tool to add a new badge certification to badge_certifications.yaml
"""

import yaml
from pathlib import Path
from datetime import datetime

def get_input(prompt, default='', required=True):
    """Get user input with optional default"""
    if default:
        prompt = f"{prompt} [{default}]"

    value = input(f"{prompt}: ").strip()

    if not value and default:
        return default

    if required and not value:
        print("❌ This field is required!")
        return get_input(prompt, default, required)

    return value

def get_date_input(prompt, required=False):
    """Get date input in YYYY-MM-DD format"""
    while True:
        value = get_input(prompt + " (YYYY-MM-DD)", '', required)
        if not value:
            return ''

        try:
            datetime.strptime(value, '%Y-%m-%d')
            return value
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD")

def main():
    script_dir = Path(__file__).parent
    yaml_path = script_dir / 'badge_certifications.yaml'

    print("\n" + "="*60)
    print("🏆 Add New Badge Certification")
    print("="*60 + "\n")

    # Load existing YAML
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ Config file not found: {yaml_path}")
        return 1

    # Get certification details
    print("Enter certification details:\n")

    cert = {}
    cert['title'] = get_input("Certification Title", required=True)
    cert['provider'] = get_input("Provider/Issuer", required=True)

    print("\nAvailable categories:")
    print("  - Credentials (Professional Certifications & Badges)")

    category = get_input("Category", 'Credentials', required=True)
    cert['category'] = category

    cert['badge_image'] = get_input("Badge image filename (in assets/badges/)", required=True)
    if not cert['badge_image'].endswith('.png'):
        cert['badge_image'] += '.png'

    cert['verification_url'] = get_input("Verification URL", required=False)
    cert['issue_date'] = get_date_input("Issue Date", required=False)
    cert['expiry_date'] = get_date_input("Expiry Date", required=False)
    cert['credential_id'] = get_input("Credential ID", required=False)
    cert['description'] = get_input("Description", required=False)

    # Add to config
    if 'certifications' not in config:
        config['certifications'] = []

    config['certifications'].append(cert)

    # Save YAML
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print("\n" + "="*60)
    print("✅ Certification added successfully!")
    print("="*60)
    print(f"\n📄 Updated: {yaml_path}")
    print(f"\n🎯 Next Steps:")
    print(f"   1. Add badge image: assets/badges/{cert['badge_image']}")
    print(f"   2. Run: python3 tools/generate_badge_certifications.py")
    print(f"   3. Commit and push changes")
    print("="*60 + "\n")

    return 0

if __name__ == '__main__':
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        exit(1)

