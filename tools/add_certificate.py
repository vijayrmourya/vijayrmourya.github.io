#!/usr/bin/env python3
"""
Interactive script to add a new certificate
Makes it easy to add certificates without manually editing YAML
"""

import os
import yaml
from pathlib import Path
from datetime import datetime

CATEGORIES = {
    '1': ('Cloud', 'Cloud Services - AWS, GCP, Azure'),
    '2': ('CloudArchitect', 'Cloud Architecture & Design Patterns'),
    '3': ('Serverless', 'Serverless Computing & Lambda'),
    '4': ('ArtificialIntellegence_MachineLearning', 'AI & Machine Learning'),
    '5': ('DevOps', 'DevOps Practices & Methodologies'),
    '6': ('Python', 'Python Programming'),
    '7': ('Terraform', 'Infrastructure as Code'),
    '8': ('Jenkins', 'CI/CD Automation'),
    '9': ('Linux', 'Linux System Administration'),
    '10': ('Ansible', 'Configuration Management'),
    '11': ('MachineLearning', 'Machine Learning Foundations'),
}

def select_category():
    """Interactive category selection"""
    print("\n📁 Select Certificate Category:")
    print("=" * 60)
    for key, (cat, desc) in CATEGORIES.items():
        print(f"  {key}. {desc}")
    print("=" * 60)

    while True:
        choice = input("\nEnter category number (1-11): ").strip()
        if choice in CATEGORIES:
            return CATEGORIES[choice][0]
        print("❌ Invalid choice. Please enter a number between 1 and 11.")

def get_input(prompt, required=True, default=''):
    """Get user input with validation"""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        if not required:
            return default
        print("❌ This field is required. Please enter a value.")

def validate_date(date_str):
    """Validate date format"""
    if not date_str:
        return True
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def main():
    # Get paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    yaml_path = script_dir / 'certificates.yaml'

    print("=" * 60)
    print("📚 Add New Certificate - Interactive Helper")
    print("=" * 60)

    # Load existing YAML
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ Error: {yaml_path} not found")
        print("Run: python3 tools/migrate_to_yaml.py first")
        return 1

    # Get certificate details
    print("\n📝 Enter Certificate Details:\n")

    title = get_input("Certificate Title: ")
    provider = get_input("Provider (e.g., AWS Skill Builder, Udacity): ")
    category = select_category()
    filename = get_input("PDF Filename (e.g., cert.pdf): ")

    # Validate PDF exists
    pdf_path = project_root / 'assets' / 'certificates' / category / filename
    if not pdf_path.exists():
        print(f"\n⚠️  Warning: PDF file not found at:")
        print(f"   {pdf_path}")
        confirm = input("\nContinue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Cancelled")
            return 1

    # Optional fields
    while True:
        completion_date = input("Completion Date (YYYY-MM-DD, or press Enter to skip): ").strip()
        if validate_date(completion_date):
            break
        print("❌ Invalid date format. Use YYYY-MM-DD (e.g., 2025-12-31)")

    verification_url = input("Verification URL (or press Enter to skip): ").strip()

    # Create certificate entry
    cert_entry = {
        'title': title,
        'provider': provider,
        'category': category,
        'filename': filename,
    }

    if completion_date:
        cert_entry['completion_date'] = completion_date
    if verification_url:
        cert_entry['verification_url'] = verification_url

    # Add to config
    if 'certificates' not in config:
        config['certificates'] = []

    config['certificates'].append(cert_entry)

    # Save YAML
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print("\n" + "=" * 60)
    print("✅ Certificate Added Successfully!")
    print("=" * 60)
    print(f"\n📄 Title: {title}")
    print(f"🏢 Provider: {provider}")
    print(f"📁 Category: {category}")
    print(f"📎 Filename: {filename}")
    if completion_date:
        print(f"📅 Date: {completion_date}")
    if verification_url:
        print(f"🔗 Verification: {verification_url}")

    print(f"\n✅ Updated: {yaml_path}")
    print("\n📝 Next Steps:")
    print("   1. Run: python3 tools/generate_certificates_from_yaml.py")
    print("   2. Review the generated certificates.json")
    print("   3. Commit and push your changes")
    print("\nQuick commit commands:")
    print(f"   git add assets/certificates/{category}/{filename}")
    print(f"   git add tools/certificates.yaml")
    print(f'   git commit -m "Add {title}"')
    print(f"   git push")

    return 0

if __name__ == '__main__':
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        exit(1)

