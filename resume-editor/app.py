"""
Resume Data Editor - Flask Application
A simple web-based editor for managing your resume JSON file.
"""

import os
import json
import shutil
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, redirect, url_for

app = Flask(__name__)

# Configuration
RESUME_FILE = 'resume-data.json'
ARCHIVE_DIR = 'archive'

# Ensure archive directory exists
os.makedirs(ARCHIVE_DIR, exist_ok=True)

def load_resume():
    """Load resume data from JSON file"""
    if os.path.exists(RESUME_FILE):
        with open(RESUME_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return get_empty_resume()

def save_resume(data):
    """Save resume data to JSON file with backup"""
    # Create backup first
    if os.path.exists(RESUME_FILE):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(ARCHIVE_DIR, f'resume-data_{timestamp}.json')
        shutil.copy2(RESUME_FILE, backup_file)
    
    # Save new data
    with open(RESUME_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_empty_resume():
    """Return empty resume structure"""
    return {
        "profile": {
            "name": "",
            "title": "",
            "email": "",
            "phone": "",
            "linkedin": "",
            "location": "",
            "summary": ""
        },
        "skills": [],
        "experience": [],
        "achievements": []
    }

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Editor</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #f1f5f9; min-height: 100vh; }
        
        .header {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 { font-size: 1.5em; font-weight: 600; }
        .header-actions { display: flex; gap: 10px; }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        .btn-primary { background: #fff; color: #2563eb; }
        .btn-primary:hover { background: #f0f9ff; }
        .btn-success { background: #10b981; color: white; }
        .btn-success:hover { background: #059669; }
        .btn-danger { background: #ef4444; color: white; }
        .btn-danger:hover { background: #dc2626; }
        .btn-secondary { background: #64748b; color: white; }
        .btn-secondary:hover { background: #475569; }
        
        .container { max-width: 900px; margin: 0 auto; padding: 30px 20px; }
        
        .card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 20px;
            overflow: hidden;
        }
        
        .card-header {
            background: #f8fafc;
            padding: 15px 20px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .card-header h2 {
            font-size: 1.1em;
            color: #1e293b;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .card-body { padding: 20px; }
        
        .form-group { margin-bottom: 15px; }
        .form-group label {
            display: block;
            font-size: 0.85em;
            font-weight: 600;
            color: #475569;
            margin-bottom: 5px;
        }
        
        .form-control {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.2s;
        }
        
        .form-control:focus {
            outline: none;
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
        
        textarea.form-control { min-height: 100px; resize: vertical; }
        
        .form-row {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        
        .item-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            position: relative;
        }
        
        .item-card:hover { border-color: #cbd5e1; }
        
        .item-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        
        .item-number {
            background: #2563eb;
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 600;
        }
        
        .delete-btn {
            background: none;
            border: none;
            color: #ef4444;
            cursor: pointer;
            padding: 5px;
            font-size: 18px;
            opacity: 0.6;
            transition: opacity 0.2s;
        }
        
        .delete-btn:hover { opacity: 1; }
        
        .add-btn {
            width: 100%;
            padding: 12px;
            border: 2px dashed #cbd5e1;
            background: transparent;
            color: #64748b;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
        }
        
        .add-btn:hover {
            border-color: #2563eb;
            color: #2563eb;
            background: #f0f9ff;
        }
        
        .list-items { margin-top: 10px; }
        
        .list-item {
            display: flex;
            gap: 10px;
            margin-bottom: 8px;
        }
        
        .list-item input { flex: 1; }
        
        .list-item .delete-btn {
            padding: 8px;
            font-size: 16px;
        }
        
        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s;
            z-index: 1000;
        }
        
        .toast.show {
            opacity: 1;
            transform: translateY(0);
        }
        
        .toast.success { background: #10b981; }
        .toast.error { background: #ef4444; }
        
        .backup-info {
            font-size: 0.8em;
            color: #64748b;
            margin-top: 5px;
        }
        
        @media (max-width: 768px) {
            .form-row { grid-template-columns: 1fr; }
            .header { padding: 15px 20px; flex-direction: column; gap: 15px; }
            .container { padding: 20px 15px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📝 Resume Editor</h1>
        <div class="header-actions">
            <button class="btn btn-primary" onclick="previewResume()">👁️ Preview</button>
            <button class="btn btn-success" onclick="saveResume()">💾 Save</button>
        </div>
    </div>

    <div class="container">
        <!-- Profile Section -->
        <div class="card">
            <div class="card-header">
                <h2>👤 Profile Information</h2>
            </div>
            <div class="card-body">
                <div class="form-row">
                    <div class="form-group">
                        <label>Full Name</label>
                        <input type="text" class="form-control" id="profile-name" placeholder="e.g., ABHINAV">
                    </div>
                    <div class="form-group">
                        <label>Professional Title</label>
                        <input type="text" class="form-control" id="profile-title" placeholder="e.g., Technical Lead | Solutions Architect">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" class="form-control" id="profile-email" placeholder="e.g., you@example.com">
                    </div>
                    <div class="form-group">
                        <label>Phone</label>
                        <input type="tel" class="form-control" id="profile-phone" placeholder="e.g., +91-XXXXX-XXXXX">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>LinkedIn (without https://)</label>
                        <input type="text" class="form-control" id="profile-linkedin" placeholder="e.g., linkedin.com/in/yourprofile">
                    </div>
                    <div class="form-group">
                        <label>Location</label>
                        <input type="text" class="form-control" id="profile-location" placeholder="e.g., Nagpur, India">
                    </div>
                </div>
                <div class="form-group">
                    <label>Professional Summary</label>
                    <textarea class="form-control" id="profile-summary" placeholder="Write a compelling summary of your professional background..."></textarea>
                </div>
            </div>
        </div>

        <!-- Skills Section -->
        <div class="card">
            <div class="card-header">
                <h2>🛠️ Skills</h2>
            </div>
            <div class="card-body">
                <div id="skills-container"></div>
                <button class="add-btn" onclick="addSkill()">+ Add Skill Category</button>
            </div>
        </div>

        <!-- Experience Section -->
        <div class="card">
            <div class="card-header">
                <h2>💼 Experience</h2>
            </div>
            <div class="card-body">
                <div id="experience-container"></div>
                <button class="add-btn" onclick="addExperience()">+ Add Experience</button>
            </div>
        </div>

        <!-- Achievements Section -->
        <div class="card">
            <div class="card-header">
                <h2>🏆 Achievements</h2>
            </div>
            <div class="card-body">
                <div id="achievements-container"></div>
                <button class="add-btn" onclick="addAchievement()">+ Add Achievement</button>
            </div>
        </div>

        <p class="backup-info">💡 Each save creates a backup in the <code>archive/</code> folder</p>
    </div>

    <div id="toast" class="toast"></div>

    <script>
        let resumeData = {{ resume_data | tojson }};

        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {
            loadFormData();
        });

        function loadFormData() {
            // Profile
            document.getElementById('profile-name').value = resumeData.profile.name || '';
            document.getElementById('profile-title').value = resumeData.profile.title || '';
            document.getElementById('profile-email').value = resumeData.profile.email || '';
            document.getElementById('profile-phone').value = resumeData.profile.phone || '';
            document.getElementById('profile-linkedin').value = resumeData.profile.linkedin || '';
            document.getElementById('profile-location').value = resumeData.profile.location || '';
            document.getElementById('profile-summary').value = resumeData.profile.summary || '';

            // Skills
            renderSkills();

            // Experience
            renderExperience();

            // Achievements
            renderAchievements();
        }

        // ===== SKILLS =====
        function renderSkills() {
            const container = document.getElementById('skills-container');
            container.innerHTML = resumeData.skills.map((skill, idx) => `
                <div class="item-card" data-idx="${idx}">
                    <div class="item-header">
                        <span class="item-number">${idx + 1}</span>
                        <button class="delete-btn" onclick="deleteSkill(${idx})">🗑️</button>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Category</label>
                            <input type="text" class="form-control skill-category" value="${escapeHtml(skill.category)}" placeholder="e.g., Languages & Frameworks">
                        </div>
                        <div class="form-group">
                            <label>Skills (comma-separated)</label>
                            <input type="text" class="form-control skill-items" value="${escapeHtml(skill.items)}" placeholder="e.g., Java, Spring Boot, Microservices">
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function addSkill() {
            collectSkillsData(); // Collect current form data first
            resumeData.skills.push({ category: '', items: '' });
            renderSkills();
        }

        function deleteSkill(idx) {
            collectSkillsData(); // Collect current form data first
            resumeData.skills.splice(idx, 1);
            renderSkills();
        }

        function collectSkillsData() {
            const skillCards = document.querySelectorAll('#skills-container .item-card');
            resumeData.skills = Array.from(skillCards).map(card => ({
                category: card.querySelector('.skill-category')?.value || '',
                items: card.querySelector('.skill-items')?.value || ''
            }));
        }

        // ===== EXPERIENCE =====
        function renderExperience() {
            const container = document.getElementById('experience-container');
            container.innerHTML = resumeData.experience.map((exp, idx) => `
                <div class="item-card" data-idx="${idx}">
                    <div class="item-header">
                        <span class="item-number">${idx + 1}</span>
                        <button class="delete-btn" onclick="deleteExperience(${idx})">🗑️</button>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Job Title</label>
                            <input type="text" class="form-control exp-title" value="${escapeHtml(exp.title)}" placeholder="e.g., Technical Lead">
                        </div>
                        <div class="form-group">
                            <label>Company</label>
                            <input type="text" class="form-control exp-company" value="${escapeHtml(exp.company)}" placeholder="e.g., Tech Corp">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Period</label>
                        <input type="text" class="form-control exp-period" value="${escapeHtml(exp.period)}" placeholder="e.g., 2020 - Present">
                    </div>
                    <div class="form-group">
                        <label>Responsibilities</label>
                        <div class="list-items" id="exp-resp-${idx}">
                            ${(exp.responsibilities || []).map((resp, rIdx) => `
                                <div class="list-item">
                                    <input type="text" class="form-control exp-resp-item" value="${escapeHtml(resp)}" placeholder="Describe a responsibility...">
                                    <button class="delete-btn" onclick="deleteResponsibility(${idx}, ${rIdx})">×</button>
                                </div>
                            `).join('')}
                        </div>
                        <button class="add-btn" style="margin-top:10px" onclick="addResponsibility(${idx})">+ Add Responsibility</button>
                    </div>
                </div>
            `).join('');
        }

        function addExperience() {
            collectExperienceData(); // Collect current form data first
            resumeData.experience.push({ title: '', company: '', period: '', responsibilities: [''] });
            renderExperience();
        }

        function deleteExperience(idx) {
            collectExperienceData(); // Collect current form data first
            resumeData.experience.splice(idx, 1);
            renderExperience();
        }

        function addResponsibility(expIdx) {
            collectExperienceData(); // Collect current form data first
            resumeData.experience[expIdx].responsibilities.push('');
            renderExperience();
        }

        function deleteResponsibility(expIdx, respIdx) {
            collectExperienceData(); // Collect current form data first
            resumeData.experience[expIdx].responsibilities.splice(respIdx, 1);
            renderExperience();
        }

        function collectExperienceData() {
            const expCards = document.querySelectorAll('#experience-container .item-card');
            resumeData.experience = Array.from(expCards).map(card => ({
                title: card.querySelector('.exp-title')?.value || '',
                company: card.querySelector('.exp-company')?.value || '',
                period: card.querySelector('.exp-period')?.value || '',
                responsibilities: Array.from(card.querySelectorAll('.exp-resp-item')).map(input => input.value)
            }));
        }

        // ===== ACHIEVEMENTS =====
        function renderAchievements() {
            const container = document.getElementById('achievements-container');
            container.innerHTML = resumeData.achievements.map((ach, idx) => `
                <div class="item-card" data-idx="${idx}">
                    <div class="item-header">
                        <span class="item-number">${idx + 1}</span>
                        <button class="delete-btn" onclick="deleteAchievement(${idx})">🗑️</button>
                    </div>
                    <div class="form-group">
                        <label>Achievement Title</label>
                        <input type="text" class="form-control ach-title" value="${escapeHtml(ach.title)}" placeholder="e.g., Database Migration Leadership">
                    </div>
                    <div class="form-group">
                        <label>Points</label>
                        <div class="list-items" id="ach-points-${idx}">
                            ${(ach.points || []).map((point, pIdx) => `
                                <div class="list-item">
                                    <input type="text" class="form-control ach-point-item" value="${escapeHtml(point)}" placeholder="Describe an achievement point...">
                                    <button class="delete-btn" onclick="deleteAchievementPoint(${idx}, ${pIdx})">×</button>
                                </div>
                            `).join('')}
                        </div>
                        <button class="add-btn" style="margin-top:10px" onclick="addAchievementPoint(${idx})">+ Add Point</button>
                    </div>
                </div>
            `).join('');
        }

        function addAchievement() {
            collectAchievementsData(); // Collect current form data first
            resumeData.achievements.push({ title: '', points: [''] });
            renderAchievements();
        }

        function deleteAchievement(idx) {
            collectAchievementsData(); // Collect current form data first
            resumeData.achievements.splice(idx, 1);
            renderAchievements();
        }

        function addAchievementPoint(achIdx) {
            collectAchievementsData(); // Collect current form data first
            resumeData.achievements[achIdx].points.push('');
            renderAchievements();
        }

        function deleteAchievementPoint(achIdx, pointIdx) {
            collectAchievementsData(); // Collect current form data first
            resumeData.achievements[achIdx].points.splice(pointIdx, 1);
            renderAchievements();
        }

        function collectAchievementsData() {
            const achCards = document.querySelectorAll('#achievements-container .item-card');
            resumeData.achievements = Array.from(achCards).map(card => ({
                title: card.querySelector('.ach-title')?.value || '',
                points: Array.from(card.querySelectorAll('.ach-point-item')).map(input => input.value)
            }));
        }

        // ===== COLLECT & SAVE =====
        function collectFormData() {
            // Profile
            resumeData.profile = {
                name: document.getElementById('profile-name').value,
                title: document.getElementById('profile-title').value,
                email: document.getElementById('profile-email').value,
                phone: document.getElementById('profile-phone').value,
                linkedin: document.getElementById('profile-linkedin').value,
                location: document.getElementById('profile-location').value,
                summary: document.getElementById('profile-summary').value
            };

            // Skills
            const skillCards = document.querySelectorAll('#skills-container .item-card');
            resumeData.skills = Array.from(skillCards).map(card => ({
                category: card.querySelector('.skill-category').value,
                items: card.querySelector('.skill-items').value
            }));

            // Experience
            const expCards = document.querySelectorAll('#experience-container .item-card');
            resumeData.experience = Array.from(expCards).map(card => ({
                title: card.querySelector('.exp-title').value,
                company: card.querySelector('.exp-company').value,
                period: card.querySelector('.exp-period').value,
                responsibilities: Array.from(card.querySelectorAll('.exp-resp-item')).map(input => input.value).filter(v => v.trim())
            }));

            // Achievements
            const achCards = document.querySelectorAll('#achievements-container .item-card');
            resumeData.achievements = Array.from(achCards).map(card => ({
                title: card.querySelector('.ach-title').value,
                points: Array.from(card.querySelectorAll('.ach-point-item')).map(input => input.value).filter(v => v.trim())
            }));

            return resumeData;
        }

        async function saveResume() {
            const data = collectFormData();
            
            try {
                const response = await fetch('/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showToast('✅ Resume saved successfully!', 'success');
                } else {
                    showToast('❌ Error: ' + result.error, 'error');
                }
            } catch (err) {
                showToast('❌ Error saving resume', 'error');
            }
        }

        function previewResume() {
            window.open('/preview', '_blank');
        }

        function showToast(message, type) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.className = 'toast ' + type + ' show';
            setTimeout(() => {
                toast.className = 'toast';
            }, 3000);
        }

        function escapeHtml(str) {
            if (!str) return '';
            return str.replace(/&/g, '&amp;')
                      .replace(/</g, '&lt;')
                      .replace(/>/g, '&gt;')
                      .replace(/"/g, '&quot;');
        }
    </script>
</body>
</html>
'''

# Preview Template (same as resume.html but embedded)
PREVIEW_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Preview</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Segoe UI',Arial,sans-serif;line-height:1.6;color:#333;background:#f5f5f5;padding:20px}
        .controls{max-width:850px;margin:0 auto 20px;display:flex;gap:10px;justify-content:flex-end}
        .btn{background:#2563eb;color:#fff;border:none;padding:12px 24px;font-size:14px;border-radius:6px;cursor:pointer;font-weight:600}
        .btn:hover{background:#1d4ed8}
        .btn-secondary{background:#64748b}
        .btn-secondary:hover{background:#475569}
        .container{max-width:850px;margin:0 auto;background:#fff;padding:50px 60px;box-shadow:0 2px 10px rgba(0,0,0,.1)}
        .header{border-bottom:3px solid #2563eb;padding-bottom:20px;margin-bottom:30px}
        .header h1{font-size:2.4em;color:#1e293b;margin-bottom:8px;letter-spacing:-0.5px}
        .header .title{font-size:1.25em;color:#2563eb;margin-bottom:15px;font-weight:600}
        .contact-info{display:flex;flex-wrap:wrap;gap:8px 20px;font-size:.9em;color:#64748b}
        .contact-info a{color:#2563eb;text-decoration:none}
        .section{margin-bottom:28px}
        .section h2{font-size:1.2em;color:#1e293b;margin-bottom:12px;text-transform:uppercase;letter-spacing:1px;border-bottom:2px solid #e2e8f0;padding-bottom:6px}
        .summary{font-size:.95em;line-height:1.7;color:#475569;text-align:justify}
        .skills-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
        .skill-item{display:flex;font-size:.9em;line-height:1.5}
        .skill-item strong{min-width:160px;color:#1e293b;flex-shrink:0}
        .skill-item span{color:#475569}
        .experience-item,.achievement-item{margin-bottom:20px}
        .experience-item h3,.achievement-item h3{font-size:1.05em;color:#1e293b;margin-bottom:4px}
        .experience-item .meta{color:#64748b;font-size:.85em;margin-bottom:8px;font-style:italic}
        .experience-item ul,.achievement-item ul{margin-left:18px;margin-top:6px}
        .experience-item li,.achievement-item li{margin-bottom:5px;color:#475569;font-size:.9em;line-height:1.55}
        @media print{
            @page{size:A4;margin:15mm}
            body{background:#fff;padding:0;font-size:11pt}
            .controls{display:none!important}
            .container{box-shadow:none;padding:0;max-width:100%;margin:0}
        }
    </style>
</head>
<body>
    <div class="controls">
        <button class="btn" onclick="window.print()">📥 Download PDF</button>
        <button class="btn btn-secondary" onclick="window.close()">✕ Close</button>
    </div>
    <div class="container">
        <div class="header">
            <h1>{{ d.profile.name }}</h1>
            <div class="title">{{ d.profile.title }}</div>
            <div class="contact-info">
                <span>📧 <a href="mailto:{{ d.profile.email }}">{{ d.profile.email }}</a></span>
                <span>📱 {{ d.profile.phone }}</span>
                <span>💼 <a href="https://{{ d.profile.linkedin }}" target="_blank">LinkedIn</a></span>
                <span>📍 {{ d.profile.location }}</span>
            </div>
        </div>
        <div class="section">
            <h2>Professional Summary</h2>
            <p class="summary">{{ d.profile.summary }}</p>
        </div>
        <div class="section">
            <h2>Core Competencies</h2>
            <div class="skills-grid">
                {% for skill in d.skills %}
                <div class="skill-item"><strong>{{ skill['category'] }}:</strong><span>{{ skill['items'] }}</span></div>
                {% endfor %}
            </div>
        </div>
        <div class="section">
            <h2>Professional Experience</h2>
            {% for exp in d.experience %}
            <div class="experience-item">
                <h3>{{ exp['title'] }}</h3>
                <div class="meta">{{ exp['company'] }} | {{ exp['period'] }}</div>
                <ul>
                    {% for resp in exp['responsibilities'] %}
                    <li>{{ resp }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endfor %}
        </div>
        <div class="section">
            <h2>Key Achievements</h2>
            {% for ach in d.achievements %}
            <div class="achievement-item">
                <h3>{{ ach['title'] }}</h3>
                <ul>
                    {% for point in ach['points'] %}
                    <li>{{ point }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    """Main editor page"""
    resume_data = load_resume()
    return render_template_string(HTML_TEMPLATE, resume_data=resume_data)

@app.route('/save', methods=['POST'])
def save():
    """Save resume data"""
    try:
        data = request.get_json()
        save_resume(data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/preview')
def preview():
    """Preview resume"""
    resume_data = load_resume()
    return render_template_string(PREVIEW_TEMPLATE, d=resume_data)

@app.route('/backups')
def backups():
    """List backup files"""
    files = []
    if os.path.exists(ARCHIVE_DIR):
        files = sorted(os.listdir(ARCHIVE_DIR), reverse=True)
    return jsonify(files)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("📝 Resume Editor")
    print("="*60)
    print(f"\n🌐 Open in browser: http://localhost:5000")
    print(f"📄 Editing file: {RESUME_FILE}")
    print(f"📁 Backups saved to: {ARCHIVE_DIR}/")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
    