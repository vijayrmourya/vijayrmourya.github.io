#!/usr/bin/env python3
"""
Generate certificates metadata JSON for the portfolio website.
Scans the assets/certificates directory and creates a structured JSON file.
"""

import os
import json
from pathlib import Path
from datetime import datetime

# Certificate metadata mapping
CERTIFICATE_METADATA = {
    'Cloud': {
        'icon': '☁️',
        'color': '#FF9900',
        'display_name': 'Cloud Services',
        'description': 'AWS and cloud platform certifications'
    },
    'CloudArchitect': {
        'icon': '🏛️',
        'color': '#3B82F6',
        'display_name': 'Cloud Architecture',
        'description': 'Cloud architecture and design patterns'
    },
    'Serverless': {
        'icon': '⚡',
        'color': '#10B981',
        'display_name': 'Serverless',
        'description': 'Serverless computing and Lambda'
    },
    'ArtificialIntellegence_MachineLearning': {
        'icon': '🤖',
        'color': '#8B5CF6',
        'display_name': 'AI & Machine Learning',
        'description': 'Artificial Intelligence and Machine Learning'
    },
    'DevOps': {
        'icon': '🚀',
        'color': '#4A90E2',
        'display_name': 'DevOps',
        'description': 'DevOps practices and methodologies'
    },
    'Python': {
        'icon': '🐍',
        'color': '#3776AB',
        'display_name': 'Python',
        'description': 'Python programming and development'
    },
    'Terraform': {
        'icon': '🏗️',
        'color': '#7B42BC',
        'display_name': 'Terraform',
        'description': 'Infrastructure as Code with Terraform'
    },
    'Jenkins': {
        'icon': '⚙️',
        'color': '#D24939',
        'display_name': 'Jenkins',
        'description': 'CI/CD automation with Jenkins'
    },
    'Linux': {
        'icon': '🐧',
        'color': '#FCC624',
        'display_name': 'Linux',
        'description': 'Linux system administration'
    },
    'Ansible': {
        'icon': '🔧',
        'color': '#EE0000',
        'display_name': 'Ansible',
        'description': 'Configuration management and automation'
    },
    'MachineLearning': {
        'icon': '🧠',
        'color': '#00D9FF',
        'display_name': 'Machine Learning',
        'description': 'Machine Learning foundations'
    }
}

def clean_filename(filename):
    """Extract clean title from filename"""
    # Remove file extension
    name = filename.replace('.pdf', '')

    # Remove common prefixes
    prefixes = ['AWSSkillBuilder-', 'KodeKloud-', 'KodeKloud-Course-Certificate_',
                'ACloudGuru ', 'Udacity-']
    for prefix in prefixes:
        name = name.replace(prefix, '')

    # Remove trailing _AWS Course Completion Certificate, etc.
    suffixes = ['_AWS Course Completion Certificate', '_AWS Course Completion',
                ' - AWS Course Completion Certificate', ' - AWS Course Completion',
                ' - Course Completion Certificate', '_VIJAY-MOURYA.pdf',
                'Course Completion Certificate']
    for suffix in suffixes:
        name = name.replace(suffix, '')

    # Clean up underscores and extra spaces
    name = name.replace('_', ' ').replace('-', ' ')
    name = ' '.join(name.split())

    return name

def extract_provider(filename):
    """Extract the course provider from filename"""
    if 'AWSSkillBuilder' in filename:
        return 'AWS Skill Builder'
    elif 'KodeKloud' in filename:
        return 'KodeKloud'
    elif 'ACloudGuru' in filename or 'A Cloud Guru' in filename:
        return 'A Cloud Guru'
    elif 'Udacity' in filename:
        return 'Udacity'
    elif 'Udemy' in filename:
        return 'Udemy'
    elif 'Coursera' in filename:
        return 'Coursera'
    elif 'Introduction to' in filename:
        return 'Coursera'  # Most "Introduction to" courses are from Coursera
    else:
        return 'Professional Certification'

def scan_certificates(base_path):
    """Scan certificates directory and generate metadata"""
    certificates_data = {
        'last_updated': datetime.now().isoformat(),
        'total_count': 0,
        'categories': {}
    }

    for category, meta in CERTIFICATE_METADATA.items():
        category_path = base_path / category
        if not category_path.exists():
            continue

        pdf_files = list(category_path.glob('*.pdf'))

        if not pdf_files:
            continue

        certificates_data['categories'][category] = {
            'display_name': meta['display_name'],
            'icon': meta['icon'],
            'color': meta['color'],
            'description': meta['description'],
            'count': len(pdf_files),
            'certificates': []
        }

        for pdf_file in sorted(pdf_files):
            cert_info = {
                'title': clean_filename(pdf_file.name),
                'provider': extract_provider(pdf_file.name),
                'filename': pdf_file.name,
                'path': f'assets/certificates/{category}/{pdf_file.name}',
                'category': category
            }
            certificates_data['categories'][category]['certificates'].append(cert_info)
            certificates_data['total_count'] += 1

    return certificates_data

def main():
    # Get the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    certificates_dir = project_root / 'assets' / 'certificates'
    output_file = project_root / 'assets' / 'certificates.json'

    if not certificates_dir.exists():
        print(f"Error: Certificates directory not found: {certificates_dir}")
        return

    print(f"Scanning certificates in: {certificates_dir}")
    certificates_data = scan_certificates(certificates_dir)

    # Write JSON output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(certificates_data, f, indent=2, ensure_ascii=False)

    print(f"✓ Generated certificates metadata: {output_file}")
    print(f"✓ Total certificates: {certificates_data['total_count']}")
    print(f"\nCertificates by category:")
    for category, data in certificates_data['categories'].items():
        print(f"  • {data['icon']} {data['display_name']}: {data['count']} certificates")

if __name__ == '__main__':
    main()

