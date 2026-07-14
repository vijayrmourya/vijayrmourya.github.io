#!/usr/bin/env python3
"""
Interactive Experience Addition Tool
Helps you add new work experience to the portfolio website
"""

import yaml
from pathlib import Path
from datetime import datetime


def load_experience_config():
    """Load current experience configuration"""
    config_path = Path(__file__).parent / 'experience.yaml'

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    return config, config_path


def save_experience_config(config, config_path):
    """Save updated experience configuration"""
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def get_input(prompt, default=None, required=True):
    """Get user input with optional default"""
    if default:
        prompt = f"{prompt} [{default}]"

    value = input(f"{prompt}: ").strip()

    if not value and default:
        return default

    if required and not value:
        print("❌ This field is required!")
        return get_input(prompt.split('[')[0].strip(), default, required)

    return value


def get_yes_no(prompt, default='y'):
    """Get yes/no input"""
    value = input(f"{prompt} (y/n) [{default}]: ").strip().lower()

    if not value:
        value = default

    return value in ['y', 'yes']


def add_new_experience():
    """Interactive flow to add a new experience"""
    print("\n" + "="*60)
    print("📝 ADD NEW WORK EXPERIENCE")
    print("="*60)

    # Load existing config
    config, config_path = load_experience_config()

    # Calculate next order
    max_order = max([exp['order'] for exp in config['experiences']], default=0)

    print("\n🏢 Company Information")
    print("-" * 40)

    experience = {
        'id': get_input("Company ID (lowercase, no spaces, e.g., 'google')"),
        'company': get_input("Company Name (e.g., 'Google LLC')"),
        'location': get_input("Location (e.g., 'Mountain View, USA')"),
        'role': get_input("Job Role/Title"),
        'start_date': get_input("Start Date (YYYY-MM format)", datetime.now().strftime('%Y-%m')),
        'end_date': get_input("End Date (YYYY-MM or 'present')", 'present'),
        'duration': get_input("Duration Display (e.g., '2 years 3 months')"),
        'color': get_input("Color (hex code)", '#60a5fa', required=False) or '#60a5fa',
        'order': max_order + 1,
        'projects': [],
        'tech_stack': ''
    }

    # Add projects
    print("\n🚀 Projects & Contributions")
    print("-" * 40)
    print("Add at least one project/contribution for this experience.")

    while True:
        print(f"\n📌 Project #{len(experience['projects']) + 1}")

        project_title = get_input("Project Title (with emoji, e.g., '🎯 CI/CD Pipeline Automation')")

        print("Add highlights (bullet points). Enter empty line when done:")
        highlights = []
        i = 1
        while True:
            highlight = input(f"  {i}. ").strip()
            if not highlight:
                break
            highlights.append(highlight)
            i += 1

        if highlights:
            experience['projects'].append({
                'title': project_title,
                'highlights': highlights
            })

        if not get_yes_no("\nAdd another project?", 'n'):
            break

    # Tech stack
    print("\n💻 Technical Stack")
    print("-" * 40)
    tech_stack = get_input("Tech Stack (comma-separated with bullets, e.g., 'AWS • Python • Terraform')")
    experience['tech_stack'] = tech_stack

    # Add to config
    config['experiences'].append(experience)

    # Save
    print("\n💾 Saving configuration...")
    save_experience_config(config, config_path)
    print("✅ Experience added successfully!")

    # Generate HTML
    print("\n🔨 Generating experience.html...")
    import generate_experience
    generate_experience.main()

    print("\n" + "="*60)
    print("✨ DONE! Your new experience has been added.")
    print("="*60)
    print("\n📋 Next Steps:")
    print("  1. Review the generated experience.html")
    print("  2. Refresh your browser to see the changes")
    print("  3. Commit and push to deploy")


def update_existing_experience():
    """Update an existing experience"""
    config, config_path = load_experience_config()

    print("\n📝 Existing Experiences:")
    for i, exp in enumerate(config['experiences'], 1):
        print(f"  {i}. {exp['company']} - {exp['role']}")

    choice = int(get_input("\nSelect experience to update (number)")) - 1

    if choice < 0 or choice >= len(config['experiences']):
        print("❌ Invalid selection!")
        return

    experience = config['experiences'][choice]

    print(f"\n✏️ Updating: {experience['company']}")
    print("\nPress Enter to keep current value, or enter new value:")

    # Update fields
    for field in ['company', 'location', 'role', 'start_date', 'end_date', 'duration', 'tech_stack']:
        current = experience.get(field, '')
        new_value = get_input(f"{field.replace('_', ' ').title()}", str(current), required=False)
        if new_value:
            experience[field] = new_value

    # Save and regenerate
    save_experience_config(config, config_path)

    print("\n🔨 Regenerating experience.html...")
    import generate_experience
    generate_experience.main()

    print("\n✅ Experience updated successfully!")


def main():
    """Main menu"""
    print("\n" + "="*60)
    print("🎯 EXPERIENCE MANAGEMENT TOOL")
    print("="*60)
    print("\nWhat would you like to do?")
    print("  1. Add new experience")
    print("  2. Update existing experience")
    print("  3. Regenerate experience.html from YAML")
    print("  4. Exit")

    choice = get_input("\nChoice (1-4)", "1")

    if choice == '1':
        add_new_experience()
    elif choice == '2':
        update_existing_experience()
    elif choice == '3':
        import generate_experience
        generate_experience.main()
    elif choice == '4':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice!")


if __name__ == '__main__':
    main()

