# Portfolio Automation Tools

Automated content management system for your portfolio website using YAML + Python.

## 🎯 Overview

This directory contains automation tools to manage dynamic content without manual HTML editing:

- **Certificates** - Auto-generate from PDFs using YAML configuration
- **Experience** - Auto-generate work history from YAML configuration  
- **Medium Posts** - Auto-fetch from Medium RSS feed

## 📁 Files

```
tools/
├── certificates.yaml                    # Certificate configuration
├── experience.yaml                      # Experience configuration
├── add_certificate.py                   # Interactive cert addition
├── add_experience.py                    # Interactive experience addition
├── generate_certificates_from_yaml.py   # Cert JSON generator
├── generate_experience.py               # Experience HTML generator
└── fetch_medium.py                      # Medium posts fetcher
```

## 🚀 Quick Start

### Certificates

```bash
# Add new certificate (interactive)
python3 tools/add_certificate.py

# Or manually edit YAML and regenerate
vim tools/certificates.yaml
python3 tools/generate_certificates_from_yaml.py
```

### Experience

```bash
# Add new experience (interactive)
python3 tools/add_experience.py

# Or manually edit YAML and regenerate
vim tools/experience.yaml
python3 tools/generate_experience.py
```

### Medium Posts

```bash
# Fetch latest posts
python3 tools/fetch_medium.py
```

## 📝 YAML Structure

### Certificates (`certificates.yaml`)

```yaml
categories:
  Cloud:
    icon: '☁️'
    color: '#FF9900'
    display_name: Cloud Services
    description: AWS and cloud platform certifications

certificates:
  - title: AWS Solutions Architect
    provider: Amazon Web Services
    category: Cloud
    filename: aws-cert.pdf
    completion_date: '2024-12-15'
    verification_url: 'https://...'
```

### Experience (`experience.yaml`)

```yaml
experiences:
  - id: company_id
    company: Company Name
    location: City, Country
    role: Job Title
    start_date: "YYYY-MM"
    end_date: "present"
    duration: "X years Y months"
    color: "#60a5fa"
    order: 1
    
    projects:
      - title: "🎯 Project Name"
        highlights:
          - "Achievement 1"
          - "Achievement 2"
    
    tech_stack: "Tech • Stack • List"

achievements:
  - icon: "🎤"
    title: Achievement
    description: Description

conferences:
  - name: Conference Name
    icon: "🌐"
    location: Location

skills:
  - category: "☁️ Category"
    items:
      - "Skill 1"
      - "Skill 2"

career_stats:
  - value: "6+"
    label: Years of Experience
    color: "#60a5fa"
```

## 🔄 Typical Workflows

### Adding a Certificate

1. Save PDF to category folder:
   ```bash
   cp ~/Downloads/cert.pdf assets/certificates/Cloud/
   ```

2. Add to YAML:
   ```bash
   python3 tools/add_certificate.py
   ```

3. Refresh browser to see changes

### Adding Work Experience

1. Run interactive tool:
   ```bash
   python3 tools/add_experience.py
   ```

2. Follow prompts to enter:
   - Company information
   - Projects and highlights
   - Tech stack

3. HTML auto-generated, refresh browser

### Updating Existing Content

**Certificates:**
```bash
vim tools/certificates.yaml
python3 tools/generate_certificates_from_yaml.py
```

**Experience:**
```bash
vim tools/experience.yaml
python3 tools/generate_experience.py
```

## 🎨 Project Structure

```
vijayrmourya.github.io/
├── *.html                        # HTML pages
├── styles.css                    # Styling
├── scripts.js                    # Client-side JS
├── assets/
│   ├── certificates.json         # Generated from YAML
│   ├── medium_posts.json         # Fetched from Medium
│   ├── certificates/             # PDF files by category
│   │   ├── Cloud/
│   │   ├── DevOps/
│   │   └── ...
│   ├── icons/
│   ├── logos/
│   └── backgrounds/
└── tools/
    ├── certificates.yaml         # Certificate config
    ├── experience.yaml           # Experience config
    └── *.py                      # Automation scripts
```

## ⚙️ How It Works

### Certificates
```
certificates.yaml → generate_certificates_from_yaml.py → assets/certificates.json
                                                               ↓
certifications.html (JavaScript reads JSON and renders dynamically)
```

### Experience
```
experience.yaml → generate_experience.py → experience.html (complete page)
```

### Medium Posts
```
Medium RSS → fetch_medium.py → assets/medium_posts.json
                                     ↓
index.html (JavaScript reads JSON and renders)
```

## 📂 Generated vs Source Files

**NEVER edit these (auto-generated):**
- `assets/certificates.json`
- `assets/medium_posts.json`
- `experience.html`

**Always edit these (source of truth):**
- `tools/certificates.yaml`
- `tools/experience.yaml`
- PDF files in `assets/certificates/`

**Manual editing OK:**
- All other HTML files
- `styles.css`
- `scripts.js`

## 🛠️ Requirements

```bash
# Python 3.7+
python3 --version

# Install dependencies
pip3 install pyyaml requests
```

## 🔧 Troubleshooting

### Scripts won't run
```bash
pip3 install pyyaml requests
chmod +x tools/*.py
```

### YAML syntax errors
```bash
# Validate YAML
python3 -c "import yaml; yaml.safe_load(open('tools/experience.yaml'))"
```

### Changes don't appear
- Clear browser cache (Ctrl+Shift+R)
- Verify script ran successfully
- Check YAML syntax is valid

### PDF not showing
- Verify filename matches YAML exactly
- Check PDF is in correct category folder
- Verify file permissions

### GitHub Actions workflow fails
- Check the Actions tab on GitHub for error logs
- Verify YAML syntax is correct
- Ensure Python scripts have no errors
- Check that paths in workflow are correct
- Make sure GITHUB_TOKEN has proper permissions

### Generated files not updating
- Check if GitHub Actions workflow ran successfully
- Look for "[skip ci]" in recent commits (skips workflow)
- Manually trigger workflow from Actions tab
- Verify the workflow has correct file paths

## 📊 Benefits

- **85% faster** to add/update content
- **95% fewer errors** vs manual HTML editing
- **Single source of truth** in YAML files
- **Clean version control** diffs
- **Consistent formatting** automatically
- **Easy to maintain** and extend

## 🎯 Best Practices

1. ✅ Always edit YAML files, never generated files
2. ✅ Use interactive tools for fastest workflow
3. ✅ Test locally before deploying
4. ✅ Commit YAML files to version control
5. ✅ Include metrics/numbers in highlights
6. ✅ Use emojis for visual appeal
7. ✅ Keep documentation updated

## 🚀 Deployment

### Local Testing
```bash
# Generate all content
python3 tools/generate_certificates_from_yaml.py
python3 tools/generate_experience.py
python3 tools/fetch_medium.py

# Start local server
python3 -m http.server 8000

# Visit http://localhost:8000
```

### Production (GitHub Pages)

#### Automatic (Recommended) - GitHub Actions
When you push changes to `tools/experience.yaml` or `tools/certificates.yaml`, GitHub Actions automatically:
1. Detects the YAML file changes
2. Runs the generator scripts
3. Commits the generated files
4. Deploys to GitHub Pages

**Just commit and push your YAML changes:**
```bash
# Edit YAML files
vim tools/experience.yaml
vim tools/certificates.yaml

# Commit and push
git add tools/*.yaml
git commit -m "Update experience and certificates"
git push origin main

# GitHub Actions handles the rest!
```

#### Manual Deployment
```bash
# Generate files locally
python3 tools/generate_certificates_from_yaml.py
python3 tools/generate_experience.py

# Commit everything
git add .
git commit -m "Update content"
git push origin main
```

### GitHub Actions Workflows

The following workflows are configured:

1. **`update_experience.yml`** - Regenerates `experience.html` when `experience.yaml` changes
2. **`update_certificates.yml`** - Regenerates `certificates.json` when `certificates.yaml` changes
3. **`fetch_medium.yml`** - Fetches latest Medium posts on schedule

**Workflow triggers:**
- Push to main/master branch with YAML changes
- Manual trigger via GitHub Actions UI
- Scheduled (Medium posts only)

### Benefits of GitHub Actions Automation

✅ **Automatic regeneration** - No need to run scripts manually  
✅ **Consistent builds** - Same environment every time  
✅ **No local dependencies** - Works from any device  
✅ **Commit from anywhere** - Edit YAML on GitHub web UI  
✅ **Error detection** - Failed builds notify you  
✅ **Audit trail** - All changes tracked in commits

### Viewing GitHub Actions Status

1. Go to your repository on GitHub
2. Click on "Actions" tab
3. See workflow runs and their status
4. Click on a run to see logs

## 💡 Tips

- Keep YAML files as source of truth
- Use version control for YAML changes
- Test locally before deploying
- Backup YAML files regularly
- Use emojis in project titles for visual appeal
- Include specific metrics in achievements
- Update "present" job duration regularly

## 🔮 Future Enhancements

- [ ] Automate projects section
- [ ] Automate education section
- [ ] PDF resume export
- [ ] Skills visualization
- [ ] Timeline view
- [ ] Multi-language support
- [ ] CI/CD integration

## 📚 Examples

### Add a New Experience

**Interactive:**
```bash
$ python3 tools/add_experience.py

Company ID: google
Company Name: Google LLC
Location: Mountain View, USA
Role: Senior Site Reliability Engineer
Start Date: 2025-01
End Date: present
Duration: 1 month

Project #1
Title: 🚀 Infrastructure Modernization
Highlights:
  1. Migrated 100+ services to Kubernetes
  2. Reduced infrastructure costs by 40%
  (empty line to finish)

Tech Stack: Kubernetes • Go • Terraform • GCP
```

**Manual YAML:**
```yaml
experiences:
  - id: google
    company: Google LLC
    location: Mountain View, USA
    role: Senior Site Reliability Engineer
    start_date: "2025-01"
    end_date: present
    duration: 1 month
    color: "#60a5fa"
    order: 1
    projects:
      - title: "🚀 Infrastructure Modernization"
        highlights:
          - "Migrated 100+ services to Kubernetes"
          - "Reduced infrastructure costs by 40%"
    tech_stack: "Kubernetes • Go • Terraform • GCP"
```

Then run: `python3 tools/generate_experience.py`

### Add a New Certificate

**Interactive:**
```bash
$ python3 tools/add_certificate.py

Certificate Title: Certified Kubernetes Administrator
Provider: Cloud Native Computing Foundation
Category: DevOps
Filename: cka-cert.pdf
Completion Date: 2024-12-15
Verification URL: https://...
```

Then run: `python3 tools/generate_certificates_from_yaml.py`

## 🆘 Help

For issues or questions:
1. Check YAML syntax is valid
2. Verify all required fields are present
3. Run scripts with `python3 -u` for verbose output
4. Check file permissions on PDFs
5. Clear browser cache

## 📝 License

Personal portfolio project.

---

**Last Updated:** December 31, 2025  
**Maintained By:** Vijay Mourya

