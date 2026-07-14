#!/usr/bin/env python3
"""
Generate experience.html from YAML configuration
Reads experience.yaml and generates a complete HTML page
"""

import yaml
from pathlib import Path
from datetime import datetime


def load_experience_config():
    """Load experience configuration from YAML file"""
    config_path = Path(__file__).parent / 'experience.yaml'

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    return config


def generate_achievements_html(achievements):
    """Generate achievements section HTML"""
    html_parts = []

    for achievement in achievements:
        html_parts.append(f'''
                <div class="card" style="padding:16px;">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                        <span style="font-size:1.8rem;">{achievement['icon']}</span>
                        <strong style="font-size:0.95rem;">{achievement['title']}</strong>
                    </div>
                    <p class="small" style="margin:0;">{achievement['description']}</p>
                </div>
''')

    return ''.join(html_parts)


def generate_conferences_html(conferences):
    """Generate conferences section HTML"""
    html_parts = []

    for conference in conferences:
        html_parts.append(f'''
                <div class="card" style="padding:16px; text-align:center;">
                    <div style="font-size:2rem; margin-bottom:8px;">{conference['icon']}</div>
                    <strong style="font-size:0.95rem;">{conference['name']}</strong>
                    <div class="small" style="margin-top:4px; color:var(--muted);">{conference['location']}</div>
                </div>
''')

    return ''.join(html_parts)


def generate_project_html(project):
    """Generate a single project HTML"""
    highlights_html = '\n'.join([f'                        <li>{highlight}</li>' for highlight in project['highlights']])

    return f'''
                <div style="margin-bottom:16px;">
                    <strong class="small" style="color:#4fd1c5; font-size:0.95rem;">{project['title']}</strong>
                    <ul class="small" style="margin:8px 0 0 20px; line-height:1.7;">
{highlights_html}
                    </ul>
                </div>
'''


def generate_experience_card_html(experience):
    """Generate a single experience card HTML"""
    projects_html = ''.join([generate_project_html(project) for project in experience['projects']])

    # Format date range
    end_date_display = experience['end_date'] if experience['end_date'] != 'present' else 'Present'
    start_month_year = datetime.strptime(experience['start_date'], '%Y-%m').strftime('%b %Y')
    end_month_year = end_date_display if end_date_display == 'Present' else datetime.strptime(experience['end_date'], '%Y-%m').strftime('%b %Y')
    date_range = f"{start_month_year} – {end_month_year}"

    return f'''
            <!-- {experience['company']} -->
            <div class="card company-card" style="padding:24px; margin-bottom:20px;">
                <div style="display:flex; justify-content:space-between; align-items:start; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
                    <div>
                        <h3 style="margin:0; color:{experience['color']}; font-size:1.3rem;">{experience['company']}</h3>
                        <div class="small" style="margin-top:4px; color:var(--muted);">{experience['location']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="label" style="display:inline-block; padding:4px 12px; background:rgba(96,165,250,0.15); border-radius:20px;">{date_range}</div>
                        <div class="small" style="margin-top:4px; color:var(--muted);">{experience['duration']}</div>
                    </div>
                </div>

                <strong style="display:block; margin-bottom:16px; color:#e6eef8; font-size:1.05rem;">{experience['role']}</strong>

{projects_html}
                <div style="padding-top:12px; border-top:1px solid rgba(255,255,255,0.1);">
                    <strong class="small">Tech Stack:</strong>
                    <div class="small" style="margin-top:6px; color:#94a3b8;">
                        {experience['tech_stack']}
                    </div>
                </div>
            </div>
'''


def generate_skills_html(skills):
    """Generate skills section HTML"""
    html_parts = []

    for skill in skills:
        items_html = '\n'.join([f'                        <li>{item}</li>' for item in skill['items']])

        html_parts.append(f'''
                <div class="card" style="padding:20px;">
                    <h3 style="margin:0 0 12px 0; font-size:1.1rem;">{skill['category']}</h3>
                    <ul class="small" style="margin:0; padding-left:20px; line-height:1.8;">
{items_html}
                    </ul>
                </div>
''')

    return ''.join(html_parts)


def generate_career_stats_html(stats):
    """Generate career stats section HTML"""
    html_parts = []

    for stat in stats:
        html_parts.append(f'''
                <div class="card" style="padding:20px; text-align:center;">
                    <div style="font-size:2.5rem; font-weight:700; color:{stat['color']};">{stat['value']}</div>
                    <div class="small">{stat['label']}</div>
                </div>
''')

    return ''.join(html_parts)


def generate_experience_html(config):
    """Generate complete experience.html from config"""

    # Sort experiences by order
    experiences = sorted(config['experiences'], key=lambda x: x['order'])

    # Generate sections
    achievements_html = generate_achievements_html(config['achievements'])
    conferences_html = generate_conferences_html(config['conferences'])
    experience_cards_html = ''.join([generate_experience_card_html(exp) for exp in experiences])
    skills_html = generate_skills_html(config['skills'])
    stats_html = generate_career_stats_html(config['career_stats'])

    # Generate complete HTML
    html = f'''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width,initial-scale=1"/>
    <title>{config['metadata']['page_title']}</title>
    <meta name="description" content="Detailed professional experience and career history of Vijay Mourya - Senior DevOps & Infrastructure Reliability Engineer">
    <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
<div class="container">
    <header class="header">
        <div class="brand">
            <img src="assets/DP/ProfilePicture.png" alt="VM" class="logo" style="width:56px;height:56px;border-radius:12px;">
            <div>
                <div class="title">Vijay Mourya</div>
                <div class="small">Senior DevOps & Infrastructure Reliability Engineer</div>
            </div>
        </div>

        <nav class="nav" aria-label="Main navigation">
            <a href="index.html">Home</a>
            <a href="services.html">Services</a>
            <a href="experience.html" class="active">Experience</a>
            <a href="projects.html">Projects</a>
            <a href="certifications.html">Certifications</a>
            <a href="study.html">Writing</a>
            <a href="contact.html">Contact</a>
        </nav>

        <div class="mobile-menu">
            <select id="mobile-nav">
                <option value="index.html">Home</option>
                <option value="services.html">Services</option>
                <option selected value="experience.html">Experience</option>
                <option value="projects.html">Projects</option>
                <option value="certifications.html">Certifications</option>
                <option value="study.html">Writing</option>
                <option value="contact.html">Contact</option>
            </select>
        </div>
    </header>

    <main>
        <section class="card" style="padding:20px; margin-bottom:24px;">
            <h1 style="margin:0 0 8px 0; font-size:1.8rem;">{config['metadata']['hero_title']}</h1>
            <p class="small" style="margin:0;">{config['metadata']['hero_subtitle']}</p>
        </section>

        <!-- ============================================ -->
        <!-- ACHIEVEMENTS & RECOGNITION -->
        <!-- ============================================ -->
        <section class="section">
            <h2>Key Achievements</h2>

            <div class="grid" style="gap:12px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));">
{achievements_html}
            </div>
        </section>

        <!-- ============================================ -->
        <!-- CONFERENCE ATTENDANCE & LEARNING -->
        <!-- ============================================ -->
        <section class="section">
            <h2>Conference Attendance</h2>

            <div class="grid" style="gap:12px; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));">
{conferences_html}
            </div>
        </section>

        <!-- ============================================ -->
        <!-- DETAILED WORK EXPERIENCE - VERTICAL TIMELINE -->
        <!-- ============================================ -->
        <section class="section" style="margin-top:32px;">
            <h2>Career Timeline</h2>
            <p class="small" style="margin-bottom:24px; color:var(--muted);">Detailed work experience in chronological order (most recent first)</p>

{experience_cards_html}
        </section>

        <!-- ============================================ -->
        <!-- SKILLS BREAKDOWN -->
        <!-- ============================================ -->
        <section class="section" style="margin-top:40px;">
            <h2>Complete Technical Skillset</h2>

            <div class="grid" style="gap:16px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
{skills_html}
            </div>
        </section>

        <!-- ============================================ -->
        <!-- CAREER SUMMARY STATS -->
        <!-- ============================================ -->
        <section class="section" style="margin-top:40px;">
            <h2>Career Highlights</h2>
            <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:16px;">
{stats_html}
            </div>
        </section>

        <footer class="footer">
            <div class="small">© Vijay Mourya — Built with GitHub Pages</div>
        </footer>
    </main>
</div>
<script src="scripts.js"></script>
</body>
</html>
'''

    return html


def main():
    """Main function"""
    # Load config
    config = load_experience_config()
    print(f"Loaded configuration with {len(config['experiences'])} experiences")

    # Generate HTML
    html = generate_experience_html(config)

    # Write to file
    output_path = Path(__file__).parent.parent / 'experience.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated experience.html successfully!")
    print(f"Output: {output_path}")
    print("\nExperience page updated! Refresh your browser to see changes.")


if __name__ == '__main__':
    main()

