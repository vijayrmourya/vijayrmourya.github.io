#!/usr/bin/env python3
"""
Generate certificates metadata JSON from YAML configuration.
This script reads certificates.yaml and generates certificates.json for the website.
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime

def load_yaml_config(yaml_path):
    """Load the YAML configuration file"""
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ Error: YAML config file not found: {yaml_path}")
        print("Please create tools/certificates.yaml with your certificate data")
        return None
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML file: {e}")
        return None

def validate_certificate(cert, certificates_dir, category_metadata):
    """Validate a certificate entry"""
    errors = []
    warnings = []

    # Required fields
    required_fields = ['title', 'provider', 'category', 'filename']
    for field in required_fields:
        if not cert.get(field):
            errors.append(f"Missing required field: {field}")

    if errors:
        return errors, warnings

    # Validate category exists
    category = cert['category']
    if category not in category_metadata:
        errors.append(f"Invalid category: {category}")

    # Check if PDF file exists
    filename = cert['filename']
    pdf_path = certificates_dir / category / filename
    if not pdf_path.exists():
        warnings.append(f"PDF file not found: {pdf_path}")

    # Validate completion_date format if provided
    if 'completion_date' in cert and cert['completion_date']:
        try:
            datetime.strptime(cert['completion_date'], '%Y-%m-%d')
        except ValueError:
            errors.append(f"Invalid date format for completion_date. Use YYYY-MM-DD")

    return errors, warnings

def generate_certificates_json(config, certificates_dir, project_root):
    """Generate certificates.json from YAML config"""

    certificates = config.get('certificates', [])
    category_metadata = config.get('categories', {})

    if not certificates:
        print("⚠️  Warning: No certificates found in YAML config")

    # Initialize output structure
    output = {
        'last_updated': datetime.now().isoformat(),
        'total_count': 0,
        'categories': {}
    }

    # Validation tracking
    total_errors = 0
    total_warnings = 0

    # Process each certificate
    for idx, cert in enumerate(certificates, 1):
        # Validate certificate
        errors, warnings = validate_certificate(cert, certificates_dir, category_metadata)

        if errors:
            print(f"\n❌ Certificate #{idx} has errors:")
            for error in errors:
                print(f"   - {error}")
            total_errors += len(errors)
            continue  # Skip invalid entries

        if warnings:
            print(f"\n⚠️  Certificate #{idx} warnings:")
            for warning in warnings:
                print(f"   - {warning}")
            total_warnings += len(warnings)

        # Extract certificate data
        category = cert['category']
        title = cert['title']
        provider = cert['provider']
        filename = cert['filename']
        completion_date = cert.get('completion_date', '')
        verification_url = cert.get('verification_url', '')

        # Initialize category if not exists
        if category not in output['categories']:
            cat_meta = category_metadata.get(category, {})
            output['categories'][category] = {
                'display_name': cat_meta.get('display_name', category),
                'icon': cat_meta.get('icon', '📄'),
                'color': cat_meta.get('color', '#60A5FA'),
                'description': cat_meta.get('description', ''),
                'count': 0,
                'certificates': []
            }

        # Add certificate to category
        cert_entry = {
            'title': title,
            'provider': provider,
            'filename': filename,
            'path': f'assets/certificates/{category}/{filename}',
            'category': category
        }

        # Add optional fields if present
        if completion_date:
            cert_entry['completion_date'] = completion_date
        if verification_url:
            cert_entry['verification_url'] = verification_url

        output['categories'][category]['certificates'].append(cert_entry)
        output['categories'][category]['count'] += 1
        output['total_count'] += 1

    # Sort certificates within each category by completion_date (newest first)
    for category in output['categories'].values():
        category['certificates'].sort(
            key=lambda x: x.get('completion_date', '1970-01-01'),
            reverse=True
        )

    # Print summary
    print("\n" + "="*60)
    print("📊 Certificate Generation Summary")
    print("="*60)
    print(f"✅ Total Certificates: {output['total_count']}")
    print(f"📁 Categories: {len(output['categories'])}")

    if total_errors > 0:
        print(f"❌ Errors: {total_errors}")
    if total_warnings > 0:
        print(f"⚠️  Warnings: {total_warnings}")

    print("\nCertificates by Category:")
    for category, data in output['categories'].items():
        print(f"  {data['icon']} {data['display_name']}: {data['count']} certificates")

    return output, total_errors

def main():
    # Get paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    yaml_path = script_dir / 'certificates.yaml'
    certificates_dir = project_root / 'assets' / 'certificates'
    output_file = project_root / 'assets' / 'certificates.json'

    print("🔄 Generating certificates metadata from YAML...")
    print(f"📄 Reading config: {yaml_path}")

    # Load YAML configuration
    config = load_yaml_config(yaml_path)
    if not config:
        return 1

    # Generate certificates.json
    output, error_count = generate_certificates_json(config, certificates_dir, project_root)

    if error_count > 0:
        print(f"\n❌ Generation completed with {error_count} errors")
        print("⚠️  Fix the errors above and run again")
        return 1

    # Write JSON output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Successfully generated: {output_file}")
    print("="*60)

    return 0

if __name__ == '__main__':
    exit(main())

