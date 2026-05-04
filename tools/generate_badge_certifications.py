#!/usr/bin/env python3
"""
Generate badge certifications metadata JSON from YAML configuration.
This script reads badge_certifications.yaml and generates badge_certifications.json for the website.
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
        print("Please create tools/badge_certifications.yaml with your certification data")
        return None
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML file: {e}")
        return None

def validate_certification(cert, badges_dir, category_metadata):
    """Validate a certification entry"""
    errors = []
    warnings = []

    # Required fields
    required_fields = ['title', 'provider', 'category', 'badge_image']
    for field in required_fields:
        if not cert.get(field):
            errors.append(f"Missing required field: {field}")

    if errors:
        return errors, warnings

    # Validate category exists
    category = cert['category']
    if category not in category_metadata:
        errors.append(f"Invalid category: {category}")

    # Check if badge image exists
    badge_image = cert['badge_image']
    badge_path = badges_dir / badge_image
    if not badge_path.exists():
        warnings.append(f"Badge image not found: {badge_path}")

    # Validate date formats if provided
    for date_field in ['issue_date', 'expiry_date']:
        if cert.get(date_field):
            try:
                datetime.strptime(cert[date_field], '%Y-%m-%d')
            except ValueError:
                errors.append(f"Invalid date format for {date_field}. Use YYYY-MM-DD")

    # Validate verification URL
    if not cert.get('verification_url') or 'YOUR-' in cert.get('verification_url', ''):
        warnings.append(f"Verification URL not configured for: {cert.get('title')}")

    return errors, warnings

def generate_fallback_svg(provider, title):
    """Generate a fallback SVG placeholder based on provider"""
    provider_colors = {
        'Amazon Web Services': {'bg': '#232f3e', 'text': '#ff9900', 'short': 'AWS'},
        'Google Cloud': {'bg': '#4285f4', 'text': 'white', 'short': 'GCP'},
        'Coursera': {'bg': '#0056d2', 'text': 'white', 'short': 'Coursera'},
        'Linux Foundation': {'bg': '#003366', 'text': '#ffffff', 'short': 'LF'},
        'HashiCorp': {'bg': '#7B42BC', 'text': 'white', 'short': 'HC'},
    }

    config = provider_colors.get(provider, {'bg': '#4A90E2', 'text': 'white', 'short': 'CERT'})

    svg = f"""data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Crect fill='{config['bg']}' width='140' height='140' rx='10'/%3E%3Ctext x='70' y='75' font-family='Arial' font-size='16' fill='{config['text']}' text-anchor='middle'%3E{config['short']}%3C/text%3E%3C/svg%3E"""

    return svg

def generate_badge_certifications_json(config, badges_dir, project_root):
    """Generate badge_certifications.json from YAML config"""

    certifications = config.get('certifications', [])
    category_metadata = config.get('categories', {})

    if not certifications:
        print("⚠️  Warning: No certifications found in YAML config")
        return {'categories': {}, 'total_count': 0}, 0

    # Initialize output structure
    output = {
        'last_updated': datetime.now().isoformat(),
        'total_count': 0,
        'categories': {}
    }

    # Validation tracking
    total_errors = 0
    total_warnings = 0

    # Process each certification
    for idx, cert in enumerate(certifications, 1):
        # Validate certification
        errors, warnings = validate_certification(cert, badges_dir, category_metadata)

        if errors:
            print(f"\n❌ Certification #{idx} ({cert.get('title', 'Unknown')}) has errors:")
            for error in errors:
                print(f"   - {error}")
            total_errors += len(errors)
            continue  # Skip invalid entries

        if warnings:
            print(f"\n⚠️  Certification #{idx} ({cert.get('title', 'Unknown')}) warnings:")
            for warning in warnings:
                print(f"   - {warning}")
            total_warnings += len(warnings)

        # Extract certification data
        category = cert['category']

        # Initialize category if not exists
        if category not in output['categories']:
            cat_meta = category_metadata.get(category, {})
            output['categories'][category] = {
                'display_name': cat_meta.get('display_name', category.title()),
                'icon': cat_meta.get('icon', '📄'),
                'color': cat_meta.get('color', '#60A5FA'),
                'description': cat_meta.get('description', ''),
                'sort_order': cat_meta.get('sort_order', 999),
                'count': 0,
                'certifications': []
            }

        # Build certification entry
        cert_entry = {
            'title': cert['title'],
            'provider': cert['provider'],
            'badge_image': cert['badge_image'],
            'badge_path': f'assets/badges/{cert["badge_image"]}',
            'verification_url': cert.get('verification_url', ''),
            'fallback_svg': generate_fallback_svg(cert['provider'], cert['title']),
            'category': category
        }

        # Add optional fields if present and not empty
        if cert.get('issue_date'):
            cert_entry['issue_date'] = cert['issue_date']
        if cert.get('expiry_date'):
            cert_entry['expiry_date'] = cert['expiry_date']
        if cert.get('credential_id'):
            cert_entry['credential_id'] = cert['credential_id']
        if cert.get('description'):
            cert_entry['description'] = cert['description']

        output['categories'][category]['certifications'].append(cert_entry)
        output['categories'][category]['count'] += 1
        output['total_count'] += 1

    # Sort categories by sort_order
    sorted_categories = dict(sorted(
        output['categories'].items(),
        key=lambda x: x[1]['sort_order']
    ))
    output['categories'] = sorted_categories

    # Sort certifications within each category by issue_date (newest first)
    for category in output['categories'].values():
        category['certifications'].sort(
            key=lambda x: x.get('issue_date', '1970-01-01'),
            reverse=True
        )

    # Print summary
    print("\n" + "="*60)
    print("🏆 Badge Certification Generation Summary")
    print("="*60)
    print(f"✅ Total Certifications: {output['total_count']}")
    print(f"📁 Categories: {len(output['categories'])}")

    if total_errors > 0:
        print(f"❌ Errors: {total_errors}")
    if total_warnings > 0:
        print(f"⚠️  Warnings: {total_warnings}")

    print("\nCertifications by Category:")
    for category, data in output['categories'].items():
        print(f"  {data['icon']} {data['display_name']}: {data['count']} certifications")

    return output, total_errors

def main():
    # Get paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    yaml_path = script_dir / 'badge_certifications.yaml'
    badges_dir = project_root / 'assets' / 'badges'
    output_file = project_root / 'assets' / 'badge_certifications.json'

    print("🔄 Generating badge certifications metadata from YAML...")
    print(f"📄 Reading config: {yaml_path}")

    # Ensure badges directory exists
    badges_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Badge images directory: {badges_dir}")

    # Load YAML configuration
    config = load_yaml_config(yaml_path)
    if not config:
        return 1

    # Generate badge_certifications.json
    output, error_count = generate_badge_certifications_json(config, badges_dir, project_root)

    if error_count > 0:
        print(f"\n❌ Generation completed with {error_count} errors")
        print("⚠️  Fix the errors above and run again")
        return 1

    # Write JSON output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Successfully generated: {output_file}")
    print("\n📝 Next Steps:")
    print("   1. Add your actual badge images to assets/badges/")
    print("   2. Update verification URLs in badge_certifications.yaml")
    print("   3. Run this script again to regenerate the JSON")
    print("   4. The certifications.html page will auto-load the data")
    print("="*60)

    return 0

if __name__ == '__main__':
    exit(main())

