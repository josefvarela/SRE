"""
Meeting Agenda & Note Manager - Streamlit Application
A comprehensive tool for creating, editing, and managing meeting agendas
with notes, to-dos, action items, and email distribution capabilities.
"""

import streamlit as st
import json
import base64
import uuid
from datetime import datetime, date, time
import calendar
from typing import Dict, List, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import io
import re
from pathlib import Path

# ============================================================================
# PERSISTENT STORAGE CONFIGURATION
# ============================================================================
DATA_FILE = Path('agendas_data.json')

def load_agendas_from_file() -> Dict:
    """Load all agendas from persistent storage"""
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_agendas_to_file(agendas: Dict) -> None:
    """Save all agendas to persistent storage"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(agendas, f, indent=2, default=str)
    except IOError as e:
        st.error(f"Error saving data: {e}")

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Meeting Agenda & Note Manager",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
    
    /* Root variables */
    :root {
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --secondary: #0891b2;
        --success: #059669;
        --warning: #d97706;
        --danger: #dc2626;
        --dark: #1e293b;
        --light: #f8fafc;
        --border: #e2e8f0;
        --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    /* Global styling */
    .stApp {
        font-family: 'DM Sans', sans-serif;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0fdf4 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'DM Sans', sans-serif;
        font-weight: 700;
        color: var(--dark);
    }
    
    /* Main title */
    .main-title {
        background: linear-gradient(135deg, #1e40af, #0891b2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    
    /* Cards */
    .agenda-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .agenda-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    /* Status badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-primary { background: #dbeafe; color: #1e40af; }
    .badge-success { background: #d1fae5; color: #065f46; }
    .badge-warning { background: #fef3c7; color: #92400e; }
    .badge-danger { background: #fee2e2; color: #991b1b; }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--dark);
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--primary);
    }
    
    /* Item lists */
    .item-card {
        background: #f8fafc;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid var(--primary);
    }
    
    .item-card.completed {
        border-left-color: var(--success);
        opacity: 0.7;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
    }
    
    /* Form inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 1px solid var(--border);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: white;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #eff6ff, #f0fdf4);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #bfdbfe;
        margin: 0.5rem 0;
    }
    
    /* Attachment display */
    .attachment-item {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: #f1f5f9;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.25rem;
        font-size: 0.875rem;
    }
    
    /* Topic image */
    .topic-image {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        max-width: 150px;
        max-height: 150px;
        object-fit: cover;
    }
    
    /* URL link styling */
    .url-link {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        color: var(--primary);
        text-decoration: none;
        font-weight: 500;
    }
    
    .url-link:hover {
        text-decoration: underline;
    }
    
    /* Priority colors */
    .priority-high { color: var(--danger); }
    .priority-medium { color: var(--warning); }
    .priority-low { color: var(--success); }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-in {
        animation: fadeIn 0.3s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA STRUCTURES & INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    if 'agendas' not in st.session_state:
        # Load agendas from persistent storage
        st.session_state.agendas = load_agendas_from_file()
    
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'list'
    
    if 'selected_agenda_id' not in st.session_state:
        st.session_state.selected_agenda_id = None
    
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    
    if 'email_settings' not in st.session_state:
        st.session_state.email_settings = {
            'smtp_server': '',
            'smtp_port': 587,
            'sender_email': '',
            'sender_password': '',
            'distribution_list': []
        }

def create_agenda(topic: str, presenter: str, meeting_date: date, meeting_time: time,
                  duration: int, topic_image: Optional[dict] = None,
                  urls: List[dict] = None, attachments: List[dict] = None) -> str:
    """Create a new meeting agenda and return its ID"""
    agenda_id = str(uuid.uuid4())[:8]
    
    st.session_state.agendas[agenda_id] = {
        'id': agenda_id,
        'topic': topic,
        'presenter': presenter,
        'date': meeting_date.isoformat(),
        'time': meeting_time.isoformat(),
        'duration': duration,
        'topic_image': topic_image,
        'urls': urls or [],
        'attachments': attachments or [],
        'notes': [],
        'todos': [],
        'action_items': [],
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'status': 'scheduled'
    }
    
    # Save to persistent storage
    save_agendas_to_file(st.session_state.agendas)
    
    return agenda_id

def update_agenda(agenda_id: str, **kwargs):
    """Update an existing agenda with provided fields"""
    if agenda_id in st.session_state.agendas:
        for key, value in kwargs.items():
            if key == 'date' and isinstance(value, date):
                value = value.isoformat()
            elif key == 'time' and isinstance(value, time):
                value = value.isoformat()
            st.session_state.agendas[agenda_id][key] = value
        st.session_state.agendas[agenda_id]['updated_at'] = datetime.now().isoformat()
        # Save to persistent storage
        save_agendas_to_file(st.session_state.agendas)

def delete_agenda(agenda_id: str):
    """Delete an agenda by ID"""
    if agenda_id in st.session_state.agendas:
        del st.session_state.agendas[agenda_id]
        # Save to file
        save_agendas_to_file(st.session_state.agendas)

def add_note(agenda_id: str, content: str):
    """Add a note to an agenda"""
    if agenda_id in st.session_state.agendas:
        note = {
            'id': str(uuid.uuid4())[:8],
            'content': content,
            'created_at': datetime.now().isoformat()
        }
        st.session_state.agendas[agenda_id]['notes'].append(note)
        # Save to persistent storage
        save_agendas_to_file(st.session_state.agendas)

def add_todo(agenda_id: str, task: str, priority: str = 'medium', assignee: str = ''):
    """Add a to-do item to an agenda"""
    if agenda_id in st.session_state.agendas:
        todo = {
            'id': str(uuid.uuid4())[:8],
            'task': task,
            'priority': priority,
            'assignee': assignee,
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        st.session_state.agendas[agenda_id]['todos'].append(todo)
        # Save to persistent storage
        save_agendas_to_file(st.session_state.agendas)

def add_action_item(agenda_id: str, action: str, owner: str, due_date: date, priority: str = 'medium'):
    """Add an action item to an agenda"""
    if agenda_id in st.session_state.agendas:
        action_item = {
            'id': str(uuid.uuid4())[:8],
            'action': action,
            'owner': owner,
            'due_date': due_date.isoformat(),
            'priority': priority,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        st.session_state.agendas[agenda_id]['action_items'].append(action_item)
        # Save to persistent storage
        save_agendas_to_file(st.session_state.agendas)

def toggle_todo(agenda_id: str, todo_id: str):
    """Toggle a to-do item's completion status"""
    if agenda_id in st.session_state.agendas:
        for todo in st.session_state.agendas[agenda_id]['todos']:
            if todo['id'] == todo_id:
                todo['completed'] = not todo['completed']
                # Save to persistent storage
                save_agendas_to_file(st.session_state.agendas)
                break

def update_action_status(agenda_id: str, action_id: str, status: str):
    """Update an action item's status"""
    if agenda_id in st.session_state.agendas:
        for action in st.session_state.agendas[agenda_id]['action_items']:
            if action['id'] == action_id:
                action['status'] = status
                # Save to persistent storage
                save_agendas_to_file(st.session_state.agendas)
                break

def delete_item(agenda_id: str, item_type: str, item_id: str):
    """Delete a note, todo, or action item"""
    if agenda_id in st.session_state.agendas:
        items = st.session_state.agendas[agenda_id][item_type]
        st.session_state.agendas[agenda_id][item_type] = [i for i in items if i['id'] != item_id]
        # Save to persistent storage
        save_agendas_to_file(st.session_state.agendas)

def file_to_base64(uploaded_file) -> dict:
    """Convert uploaded file to base64 encoded dict"""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        encoded = base64.b64encode(bytes_data).decode('utf-8')
        return {
            'name': uploaded_file.name,
            'type': uploaded_file.type,
            'data': encoded
        }
    return None

def base64_to_bytes(encoded_data: str) -> bytes:
    """Convert base64 string back to bytes"""
    return base64.b64decode(encoded_data)

# ============================================================================
# EMAIL FUNCTIONALITY
# ============================================================================

def generate_email_content(agenda: dict, include_items: dict) -> str:
    """Generate HTML email content from agenda"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #1e293b; }}
            .container {{ max-width: 700px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #1e40af, #0891b2); color: white; padding: 30px; border-radius: 12px 12px 0 0; }}
            .header h1 {{ margin: 0; font-size: 24px; }}
            .content {{ background: white; padding: 30px; border: 1px solid #e2e8f0; }}
            .section {{ margin: 20px 0; padding: 15px; background: #f8fafc; border-radius: 8px; }}
            .section h3 {{ margin: 0 0 10px 0; color: #1e40af; border-bottom: 2px solid #1e40af; padding-bottom: 5px; }}
            .item {{ padding: 8px 0; border-bottom: 1px solid #e2e8f0; }}
            .item:last-child {{ border-bottom: none; }}
            .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }}
            .badge-high {{ background: #fee2e2; color: #991b1b; }}
            .badge-medium {{ background: #fef3c7; color: #92400e; }}
            .badge-low {{ background: #d1fae5; color: #065f46; }}
            .badge-pending {{ background: #dbeafe; color: #1e40af; }}
            .badge-in-progress {{ background: #fef3c7; color: #92400e; }}
            .badge-completed {{ background: #d1fae5; color: #065f46; }}
            .meta {{ display: flex; gap: 20px; flex-wrap: wrap; margin-top: 15px; }}
            .meta-item {{ display: flex; align-items: center; gap: 5px; }}
            .footer {{ background: #f1f5f9; padding: 20px; text-align: center; border-radius: 0 0 12px 12px; font-size: 14px; color: #64748b; }}
            .url-link {{ color: #2563eb; text-decoration: none; }}
            .url-link:hover {{ text-decoration: underline; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
            th {{ background: #f1f5f9; font-weight: 600; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📋 {agenda['topic']}</h1>
                <div class="meta">
                    <div class="meta-item">👤 {agenda['presenter']}</div>
                    <div class="meta-item">📅 {agenda['date']}</div>
                    <div class="meta-item">🕐 {agenda['time']}</div>
                    <div class="meta-item">⏱️ {agenda['duration']} min</div>
                </div>
            </div>
            <div class="content">
    """
    
    # URLs
    if agenda.get('urls') and include_items.get('urls', True):
        html += '<div class="section"><h3>🔗 Related Links</h3>'
        for url in agenda['urls']:
            html += f'<div class="item"><a href="{url["url"]}" class="url-link">{url["name"]}</a></div>'
        html += '</div>'
    
    # Notes
    if agenda.get('notes') and include_items.get('notes', True):
        html += '<div class="section"><h3>📝 Notes</h3>'
        for note in agenda['notes']:
            html += f'<div class="item">{note["content"]}</div>'
        html += '</div>'
    
    # To-Dos
    if agenda.get('todos') and include_items.get('todos', True):
        html += '<div class="section"><h3>✅ To-Do Items</h3><table>'
        html += '<tr><th>Task</th><th>Priority</th><th>Assignee</th><th>Status</th></tr>'
        for todo in agenda['todos']:
            status = '✓ Done' if todo['completed'] else '○ Pending'
            priority_class = f"badge-{todo['priority']}"
            html += f'''<tr>
                <td>{todo['task']}</td>
                <td><span class="badge {priority_class}">{todo['priority'].upper()}</span></td>
                <td>{todo['assignee'] or '-'}</td>
                <td>{status}</td>
            </tr>'''
        html += '</table></div>'
    
    # Action Items
    if agenda.get('action_items') and include_items.get('action_items', True):
        html += '<div class="section"><h3>🎯 Action Items</h3><table>'
        html += '<tr><th>Action</th><th>Owner</th><th>Due Date</th><th>Priority</th><th>Status</th></tr>'
        for action in agenda['action_items']:
            priority_class = f"badge-{action['priority']}"
            status_class = f"badge-{action['status'].replace(' ', '-')}"
            html += f'''<tr>
                <td>{action['action']}</td>
                <td>{action['owner']}</td>
                <td>{action['due_date']}</td>
                <td><span class="badge {priority_class}">{action['priority'].upper()}</span></td>
                <td><span class="badge {status_class}">{action['status'].replace('_', ' ').title()}</span></td>
            </tr>'''
        html += '</table></div>'
    
    html += f"""
            </div>
            <div class="footer">
                <p>This meeting agenda was generated by Meeting Agenda & Note Manager</p>
                <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def send_email(agenda: dict, recipients: List[str], subject: str, include_items: dict, 
               smtp_server: str, smtp_port: int, sender_email: str, sender_password: str) -> tuple:
    """Send email with agenda content"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        
        # Generate HTML content
        html_content = generate_email_content(agenda, include_items)
        
        # Plain text version
        plain_text = f"""
Meeting Agenda: {agenda['topic']}
Presenter: {agenda['presenter']}
Date: {agenda['date']} at {agenda['time']}
Duration: {agenda['duration']} minutes

Please view this email in HTML format for the full content.
        """
        
        msg.attach(MIMEText(plain_text, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        # Add attachments if any
        if agenda.get('attachments'):
            for att in agenda['attachments']:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(base64_to_bytes(att['data']))
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', f"attachment; filename={att['name']}")
                msg.attach(attachment)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return True, "Email sent successfully!"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

# ============================================================================
# DATA IMPORT/EXPORT
# ============================================================================

def export_data() -> str:
    """Export all agendas to JSON string"""
    return json.dumps(st.session_state.agendas, indent=2)

def import_data(json_string: str) -> tuple:
    """Import agendas from JSON string"""
    try:
        data = json.loads(json_string)
        st.session_state.agendas.update(data)
        return True, f"Successfully imported {len(data)} agenda(s)"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON format: {str(e)}"

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_sidebar():
    """Render the sidebar navigation and controls"""
    with st.sidebar:
        st.markdown("## 🗂️ Navigation")
        
        # View selector
        view_options = {
            'list': '📋 All Agendas',
            'create': '➕ Create New',
            'settings': '⚙️ Email Settings',
            'import_export': '📁 Import/Export'
        }
        
        for key, label in view_options.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_view = key
                st.session_state.selected_agenda_id = None
                st.session_state.edit_mode = False
                st.rerun()
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        total_agendas = len(st.session_state.agendas)
        scheduled = sum(1 for a in st.session_state.agendas.values() if a['status'] == 'scheduled')
        completed = sum(1 for a in st.session_state.agendas.values() if a['status'] == 'completed')
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", total_agendas)
            st.metric("Scheduled", scheduled)
        with col2:
            st.metric("Completed", completed)
            pending_actions = sum(
                len([ai for ai in a['action_items'] if ai['status'] != 'completed'])
                for a in st.session_state.agendas.values()
            )
            st.metric("Pending Actions", pending_actions)
        
        st.markdown("---")
        
        # Recent agendas quick access
        if st.session_state.agendas:
            st.markdown("### 🕐 Recent Agendas")
            sorted_agendas = sorted(
                st.session_state.agendas.values(),
                key=lambda x: x['updated_at'],
                reverse=True
            )[:5]
            
            for agenda in sorted_agendas:
                if st.button(f"📌 {agenda['topic'][:25]}...", key=f"quick_{agenda['id']}", use_container_width=True):
                    st.session_state.current_view = 'detail'
                    st.session_state.selected_agenda_id = agenda['id']
                    st.rerun()

def render_agenda_form(agenda: dict = None):
    """Render the agenda creation/edit form"""
    is_edit = agenda is not None
    
    st.markdown(f"### {'✏️ Edit Agenda' if is_edit else '➕ Create New Agenda'}")
    
    with st.form(key="agenda_form", clear_on_submit=not is_edit):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            topic = st.text_input(
                "📌 Topic *",
                value=agenda['topic'] if is_edit else '',
                placeholder="Enter meeting topic"
            )
            
            presenter = st.text_input(
                "👤 Presenter Name *",
                value=agenda['presenter'] if is_edit else '',
                placeholder="Enter presenter's name"
            )
            
            col_date, col_time, col_duration = st.columns(3)
            
            with col_date:
                meeting_date = st.date_input(
                    "📅 Date *",
                    value=date.fromisoformat(agenda['date']) if is_edit else date.today()
                )
            
            with col_time:
                meeting_time = st.time_input(
                    "🕐 Time *",
                    value=time.fromisoformat(agenda['time']) if is_edit else time(9, 0)
                )
            
            with col_duration:
                duration = st.number_input(
                    "⏱️ Duration (min) *",
                    min_value=5,
                    max_value=480,
                    value=agenda['duration'] if is_edit else 60,
                    step=5
                )
        
        with col2:
            st.markdown("**🖼️ Topic Image**")
            topic_image = st.file_uploader(
                "Upload image",
                type=['jpg', 'jpeg', 'png', 'gif', 'webp'],
                key="topic_image_upload"
            )
            
            if is_edit and agenda.get('topic_image') and not topic_image:
                st.image(
                    base64_to_bytes(agenda['topic_image']['data']),
                    caption="Current image",
                    width=150
                )
        
        st.markdown("---")
        
        # URLs section
        st.markdown("**🔗 Related URLs**")
        
        url_col1, url_col2 = st.columns(2)
        with url_col1:
            url_name = st.text_input("Link Name", placeholder="e.g., Project Documentation", key="url_name")
        with url_col2:
            url_value = st.text_input("URL", placeholder="https://example.com", key="url_value")
        
        # Display existing URLs if editing
        existing_urls = agenda.get('urls', []) if is_edit else []
        if existing_urls:
            st.markdown("**Existing URLs:**")
            for i, url in enumerate(existing_urls):
                st.markdown(f"- [{url['name']}]({url['url']})")
        
        st.markdown("---")
        
        # Attachments section
        st.markdown("**📎 Attachments**")
        attachments = st.file_uploader(
            "Upload files",
            type=['jpg', 'jpeg', 'png', 'pdf', 'xlsx', 'xls', 'pptx', 'ppt', 'docx', 'doc'],
            accept_multiple_files=True,
            key="attachments_upload"
        )
        
        # Display existing attachments if editing
        if is_edit and agenda.get('attachments'):
            st.markdown("**Existing Attachments:**")
            for att in agenda['attachments']:
                st.markdown(f"- 📄 {att['name']}")
        
        st.markdown("---")
        
        col_submit, col_cancel = st.columns(2)
        with col_submit:
            submitted = st.form_submit_button(
                "💾 Save Agenda" if is_edit else "✨ Create Agenda",
                use_container_width=True,
                type="primary"
            )
        
        with col_cancel:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.session_state.current_view = 'list' if not is_edit else 'detail'
                st.session_state.edit_mode = False
                st.rerun()
        
        if submitted:
            if not topic or not presenter:
                st.error("Please fill in all required fields (Topic and Presenter)")
            else:
                # Process topic image
                processed_image = None
                if topic_image:
                    processed_image = file_to_base64(topic_image)
                elif is_edit and agenda.get('topic_image'):
                    processed_image = agenda['topic_image']
                
                # Process URLs
                urls_list = existing_urls.copy() if is_edit else []
                if url_name and url_value:
                    urls_list.append({'name': url_name, 'url': url_value})
                
                # Process attachments
                attachments_list = agenda.get('attachments', []).copy() if is_edit else []
                if attachments:
                    for att in attachments:
                        attachments_list.append(file_to_base64(att))
                
                if is_edit:
                    update_agenda(
                        agenda['id'],
                        topic=topic,
                        presenter=presenter,
                        date=meeting_date,
                        time=meeting_time,
                        duration=duration,
                        topic_image=processed_image,
                        urls=urls_list,
                        attachments=attachments_list
                    )
                    st.success("✅ Agenda updated successfully!")
                else:
                    new_id = create_agenda(
                        topic=topic,
                        presenter=presenter,
                        meeting_date=meeting_date,
                        meeting_time=meeting_time,
                        duration=duration,
                        topic_image=processed_image,
                        urls=urls_list,
                        attachments=attachments_list
                    )
                    st.success(f"✅ Agenda created successfully! ID: {new_id}")
                
                st.session_state.edit_mode = False
                st.session_state.current_view = 'list'
                st.rerun()

def render_agenda_list():
    """Render the list of all agendas"""
    st.markdown('<h2 class="main-title">🏢 AWM Community of Practice (CoP)</h2>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">📋 Meeting Agenda & Note Manager</h1>', unsafe_allow_html=True)
    
    # Search and filter
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search agendas", placeholder="Search by topic or presenter...")
    with col2:
        status_filter = st.selectbox("Status", ['All', 'Scheduled', 'In Progress', 'Completed'])
    with col3:
        sort_by = st.selectbox("Sort by", ['Date (newest)', 'Date (oldest)', 'Topic A-Z', 'Topic Z-A'])
    
    # Filter and sort agendas
    filtered_agendas = list(st.session_state.agendas.values())
    
    if search:
        search_lower = search.lower()
        filtered_agendas = [
            a for a in filtered_agendas
            if search_lower in a['topic'].lower() or search_lower in a['presenter'].lower()
        ]
    
    if status_filter != 'All':
        filtered_agendas = [
            a for a in filtered_agendas
            if a['status'].lower() == status_filter.lower().replace(' ', '_')
        ]
    
    # Sort
    if sort_by == 'Date (newest)':
        filtered_agendas.sort(key=lambda x: x['date'], reverse=True)
    elif sort_by == 'Date (oldest)':
        filtered_agendas.sort(key=lambda x: x['date'])
    elif sort_by == 'Topic A-Z':
        filtered_agendas.sort(key=lambda x: x['topic'].lower())
    elif sort_by == 'Topic Z-A':
        filtered_agendas.sort(key=lambda x: x['topic'].lower(), reverse=True)
    
    st.markdown("---")
    
    if not filtered_agendas:
        st.info("📭 No agendas found. Create your first agenda using the sidebar!")
    else:
        # Group agendas by month
        from datetime import datetime
        grouped_agendas = {}
        
        for agenda in filtered_agendas:
            agenda_date = datetime.fromisoformat(agenda['date'])
            month_key = agenda_date.strftime("%B %Y")  # e.g., "January 2026"
            
            if month_key not in grouped_agendas:
                grouped_agendas[month_key] = []
            grouped_agendas[month_key].append(agenda)
        
        # Display agendas organized by collapsible months
        for month in sorted(grouped_agendas.keys(), reverse=True):
            agendas_in_month = grouped_agendas[month]
            month_agenda_count = len(agendas_in_month)
            
            with st.expander(f"📅 {month} ({month_agenda_count} agenda{'s' if month_agenda_count != 1 else ''})"):
                for agenda in agendas_in_month:
                    with st.container():
                        st.markdown('<div class="agenda-card animate-in">', unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            # Title with image
                            title_col1, title_col2 = st.columns([4, 1])
                            with title_col1:
                                st.markdown(f"### {agenda['topic']}")
                                st.markdown(f"👤 **{agenda['presenter']}**")
                                st.markdown(f"📅 {agenda['date']} &nbsp;|&nbsp; 🕐 {agenda['time']} &nbsp;|&nbsp; ⏱️ {agenda['duration']} min")
                            
                            with title_col2:
                                if agenda.get('topic_image'):
                                    st.image(
                                        base64_to_bytes(agenda['topic_image']['data']),
                                        width=80
                                    )
                            
                            # Quick stats
                            notes_count = len(agenda.get('notes', []))
                            todos_count = len(agenda.get('todos', []))
                            actions_count = len(agenda.get('action_items', []))
                            
                            st.markdown(f"📝 {notes_count} notes &nbsp;|&nbsp; ✅ {todos_count} to-dos &nbsp;|&nbsp; 🎯 {actions_count} actions")
                        
                        with col2:
                            status_colors = {
                                'scheduled': 'badge-primary',
                                'in_progress': 'badge-warning',
                                'completed': 'badge-success'
                            }
                            status_class = status_colors.get(agenda['status'], 'badge-primary')
                            st.markdown(f'<span class="badge {status_class}">{agenda["status"].replace("_", " ").upper()}</span>', unsafe_allow_html=True)
                        
                        with col3:
                            if st.button("📖 View", key=f"view_{agenda['id']}", use_container_width=True):
                                st.session_state.current_view = 'detail'
                                st.session_state.selected_agenda_id = agenda['id']
                                st.rerun()
                        
                        st.markdown('</div>', unsafe_allow_html=True)

def render_agenda_detail(agenda_id: str):
    """Render detailed view of a single agenda"""
    if agenda_id not in st.session_state.agendas:
        st.error("Agenda not found!")
        return
    
    agenda = st.session_state.agendas[agenda_id]
    
    # Header with back button
    col_back, col_title = st.columns([1, 6])
    with col_back:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_view = 'list'
            st.session_state.selected_agenda_id = None
            st.rerun()
    
    with col_title:
        st.markdown(f'<h1 class="main-title">{agenda["topic"]}</h1>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("✏️ Edit", use_container_width=True):
            st.session_state.edit_mode = True
            st.rerun()
    with col2:
        status_options = ['scheduled', 'in_progress', 'completed']
        current_idx = status_options.index(agenda['status']) if agenda['status'] in status_options else 0
        new_status = st.selectbox("Status", status_options, index=current_idx, key="status_select", label_visibility="collapsed")
        if new_status != agenda['status']:
            update_agenda(agenda_id, status=new_status)
            st.rerun()
    with col3:
        if st.button("📧 Email", use_container_width=True):
            st.session_state.show_email_modal = True
            st.rerun()
    with col4:
        if st.button("📄 Export", use_container_width=True):
            html_content = generate_email_content(agenda, {'urls': True, 'notes': True, 'todos': True, 'action_items': True})
            st.download_button(
                "📥 Download HTML",
                html_content,
                file_name=f"agenda_{agenda['topic'][:20]}_{agenda['date']}.html",
                mime="text/html"
            )
    with col5:
        if st.button("🗑️ Delete", use_container_width=True, type="secondary"):
            st.session_state.confirm_delete = True
            st.rerun()
    
    # Confirm delete dialog
    if st.session_state.get('confirm_delete'):
        st.warning("⚠️ Are you sure you want to delete this agenda? This action cannot be undone.")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("Yes, Delete", use_container_width=True, type="primary"):
                delete_agenda(agenda_id)
                st.session_state.confirm_delete = False
                st.session_state.current_view = 'list'
                st.session_state.selected_agenda_id = None
                st.success("Agenda deleted!")
                st.rerun()
        with col_no:
            if st.button("Cancel", use_container_width=True):
                st.session_state.confirm_delete = False
                st.rerun()
    
    # Edit mode
    if st.session_state.edit_mode:
        render_agenda_form(agenda)
        return
    
    st.markdown("---")
    
    # Agenda details
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown(f"**👤 Presenter:** {agenda['presenter']}")
        st.markdown(f"**📅 Date:** {agenda['date']}")
        st.markdown(f"**🕐 Time:** {agenda['time']}")
        st.markdown(f"**⏱️ Duration:** {agenda['duration']} minutes")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # URLs
        if agenda.get('urls'):
            st.markdown('<div class="section-header">🔗 Related Links</div>', unsafe_allow_html=True)
            for url in agenda['urls']:
                st.markdown(f"🔗 [{url['name']}]({url['url']})")
        
        # Attachments
        if agenda.get('attachments'):
            st.markdown('<div class="section-header">📎 Attachments</div>', unsafe_allow_html=True)
            for att in agenda['attachments']:
                st.download_button(
                    f"📄 {att['name']}",
                    base64_to_bytes(att['data']),
                    file_name=att['name'],
                    mime=att['type'],
                    key=f"download_{att['name']}"
                )
    
    with col2:
        if agenda.get('topic_image'):
            st.image(
                base64_to_bytes(agenda['topic_image']['data']),
                caption="Topic Image",
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Tabs for Notes, To-Dos, and Action Items
    tab1, tab2, tab3 = st.tabs(["📝 Notes", "✅ To-Do Items", "🎯 Action Items"])
    
    with tab1:
        render_notes_section(agenda_id, agenda)
    
    with tab2:
        render_todos_section(agenda_id, agenda)
    
    with tab3:
        render_action_items_section(agenda_id, agenda)
    
    # Email modal
    if st.session_state.get('show_email_modal'):
        render_email_modal(agenda)

def render_notes_section(agenda_id: str, agenda: dict):
    """Render the notes section"""
    st.markdown("### 📝 Meeting Notes")
    
    # Add new note
    with st.expander("➕ Add New Note", expanded=False):
        new_note = st.text_area("Note content", key="new_note", placeholder="Enter your note here...")
        if st.button("💾 Save Note", key="save_note"):
            if new_note.strip():
                add_note(agenda_id, new_note.strip())
                st.success("Note added!")
                st.rerun()
            else:
                st.warning("Please enter some content")
    
    # Display existing notes
    if agenda.get('notes'):
        for note in reversed(agenda['notes']):
            st.markdown('<div class="item-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(note['content'])
                st.caption(f"Added: {note['created_at'][:16]}")
            with col2:
                if st.button("🗑️", key=f"del_note_{note['id']}", help="Delete note"):
                    delete_item(agenda_id, 'notes', note['id'])
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No notes yet. Add your first note above!")

def render_todos_section(agenda_id: str, agenda: dict):
    """Render the to-do items section"""
    st.markdown("### ✅ To-Do Items")
    
    # Add new to-do
    with st.expander("➕ Add New To-Do", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            task = st.text_input("Task", key="new_todo_task", placeholder="Enter task...")
        with col2:
            priority = st.selectbox("Priority", ['low', 'medium', 'high'], index=1, key="new_todo_priority")
        with col3:
            assignee = st.text_input("Assignee", key="new_todo_assignee", placeholder="Who is responsible?")
        
        if st.button("💾 Save To-Do", key="save_todo"):
            if task.strip():
                add_todo(agenda_id, task.strip(), priority, assignee)
                st.success("To-do added!")
                st.rerun()
            else:
                st.warning("Please enter a task")
    
    # Display existing to-dos
    if agenda.get('todos'):
        for todo in agenda['todos']:
            completed_class = "completed" if todo['completed'] else ""
            st.markdown(f'<div class="item-card {completed_class}">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
            with col1:
                status_icon = "✅" if todo['completed'] else "⬜"
                text_style = "~~" if todo['completed'] else ""
                st.markdown(f"{status_icon} {text_style}{todo['task']}{text_style}")
                if todo['assignee']:
                    st.caption(f"👤 {todo['assignee']}")
            with col2:
                priority_colors = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
                st.markdown(f"{priority_colors.get(todo['priority'], '⚪')} {todo['priority'].upper()}")
            with col3:
                if st.button("✓/✗", key=f"toggle_{todo['id']}", help="Toggle completion"):
                    toggle_todo(agenda_id, todo['id'])
                    st.rerun()
            with col4:
                if st.button("🗑️", key=f"del_todo_{todo['id']}", help="Delete"):
                    delete_item(agenda_id, 'todos', todo['id'])
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No to-do items yet. Add your first task above!")

def render_action_items_section(agenda_id: str, agenda: dict):
    """Render the action items section"""
    st.markdown("### 🎯 Action Items")
    
    # Add new action item
    with st.expander("➕ Add New Action Item", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            action = st.text_input("Action", key="new_action", placeholder="What needs to be done?")
            owner = st.text_input("Owner", key="new_action_owner", placeholder="Who is responsible?")
        with col2:
            due_date = st.date_input("Due Date", key="new_action_due")
            priority = st.selectbox("Priority", ['low', 'medium', 'high'], index=1, key="new_action_priority")
        
        if st.button("💾 Save Action Item", key="save_action"):
            if action.strip() and owner.strip():
                add_action_item(agenda_id, action.strip(), owner.strip(), due_date, priority)
                st.success("Action item added!")
                st.rerun()
            else:
                st.warning("Please fill in action and owner")
    
    # Display existing action items
    if agenda.get('action_items'):
        for action in agenda['action_items']:
            status_colors = {'pending': 'badge-primary', 'in_progress': 'badge-warning', 'completed': 'badge-success'}
            st.markdown('<div class="item-card">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns([3, 1, 2, 1])
            with col1:
                st.markdown(f"**{action['action']}**")
                st.caption(f"👤 {action['owner']} &nbsp;|&nbsp; 📅 Due: {action['due_date']}")
            with col2:
                priority_colors = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
                st.markdown(f"{priority_colors.get(action['priority'], '⚪')} {action['priority'].upper()}")
            with col3:
                new_status = st.selectbox(
                    "Status",
                    ['pending', 'in_progress', 'completed'],
                    index=['pending', 'in_progress', 'completed'].index(action['status']),
                    key=f"status_{action['id']}",
                    label_visibility="collapsed"
                )
                if new_status != action['status']:
                    update_action_status(agenda_id, action['id'], new_status)
                    st.rerun()
            with col4:
                if st.button("🗑️", key=f"del_action_{action['id']}", help="Delete"):
                    delete_item(agenda_id, 'action_items', action['id'])
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No action items yet. Add your first action item above!")

def render_email_modal(agenda: dict):
    """Render the email sending modal"""
    st.markdown("---")
    st.markdown("### 📧 Send Agenda via Email")
    
    with st.form(key="email_form"):
        recipients = st.text_area(
            "Recipients (one email per line)",
            placeholder="email1@example.com\nemail2@example.com",
            height=100
        )
        
        subject = st.text_input(
            "Subject",
            value=f"Meeting Agenda: {agenda['topic']} - {agenda['date']}"
        )
        
        st.markdown("**Include in email:**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            inc_urls = st.checkbox("URLs", value=True)
        with col2:
            inc_notes = st.checkbox("Notes", value=True)
        with col3:
            inc_todos = st.checkbox("To-Dos", value=True)
        with col4:
            inc_actions = st.checkbox("Action Items", value=True)
        
        st.markdown("---")
        st.markdown("**SMTP Settings:**")
        
        col1, col2 = st.columns(2)
        with col1:
            smtp_server = st.text_input("SMTP Server", value=st.session_state.email_settings.get('smtp_server', ''))
            sender_email = st.text_input("Sender Email", value=st.session_state.email_settings.get('sender_email', ''))
        with col2:
            smtp_port = st.number_input("SMTP Port", value=st.session_state.email_settings.get('smtp_port', 587))
            sender_password = st.text_input("App Password", type="password")
        
        col_send, col_cancel = st.columns(2)
        with col_send:
            submitted = st.form_submit_button("📤 Send Email", use_container_width=True, type="primary")
        with col_cancel:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.session_state.show_email_modal = False
                st.rerun()
        
        if submitted:
            recipient_list = [r.strip() for r in recipients.strip().split('\n') if r.strip()]
            
            if not recipient_list:
                st.error("Please enter at least one recipient")
            elif not smtp_server or not sender_email or not sender_password:
                st.error("Please fill in all SMTP settings")
            else:
                include_items = {
                    'urls': inc_urls,
                    'notes': inc_notes,
                    'todos': inc_todos,
                    'action_items': inc_actions
                }
                
                success, message = send_email(
                    agenda, recipient_list, subject, include_items,
                    smtp_server, smtp_port, sender_email, sender_password
                )
                
                if success:
                    st.success(message)
                    st.session_state.show_email_modal = False
                    # Save SMTP settings for next time
                    st.session_state.email_settings.update({
                        'smtp_server': smtp_server,
                        'smtp_port': smtp_port,
                        'sender_email': sender_email
                    })
                else:
                    st.error(message)

def render_email_settings():
    """Render email settings page"""
    st.markdown('<h1 class="main-title">⚙️ Email Settings</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Configure your email settings for sending meeting agendas. 
    These settings will be saved for the current session.
    
    **For Gmail users:**
    - Use `smtp.gmail.com` as the SMTP server
    - Port should be `587` for TLS
    - You'll need to generate an **App Password** (not your regular password)
    - Enable 2-factor authentication first, then generate an app password at https://myaccount.google.com/apppasswords
    """)
    
    with st.form(key="email_settings_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            smtp_server = st.text_input(
                "SMTP Server",
                value=st.session_state.email_settings.get('smtp_server', 'smtp.gmail.com'),
                placeholder="smtp.gmail.com"
            )
            sender_email = st.text_input(
                "Sender Email",
                value=st.session_state.email_settings.get('sender_email', ''),
                placeholder="your.email@gmail.com"
            )
        
        with col2:
            smtp_port = st.number_input(
                "SMTP Port",
                value=st.session_state.email_settings.get('smtp_port', 587),
                min_value=1,
                max_value=65535
            )
            sender_password = st.text_input(
                "App Password",
                type="password",
                help="For Gmail, use an App Password, not your regular password"
            )
        
        st.markdown("---")
        st.markdown("### 📬 Distribution List")
        st.markdown("Add commonly used email addresses for quick access when sending agendas.")
        
        distribution_list = st.text_area(
            "Distribution List (one email per line)",
            value='\n'.join(st.session_state.email_settings.get('distribution_list', [])),
            height=150,
            placeholder="team.member1@company.com\nteam.member2@company.com"
        )
        
        if st.form_submit_button("💾 Save Settings", use_container_width=True, type="primary"):
            st.session_state.email_settings = {
                'smtp_server': smtp_server,
                'smtp_port': smtp_port,
                'sender_email': sender_email,
                'sender_password': sender_password,
                'distribution_list': [e.strip() for e in distribution_list.split('\n') if e.strip()]
            }
            st.success("✅ Settings saved successfully!")

def render_import_export():
    """Render import/export page"""
    st.markdown('<h1 class="main-title">📁 Import / Export Data</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📤 Export Data")
        st.markdown("Download all your agendas as a JSON file for backup or transfer.")
        
        if st.session_state.agendas:
            export_json = export_data()
            st.download_button(
                "📥 Download All Agendas (JSON)",
                export_json,
                file_name=f"meeting_agendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            
            st.info(f"📊 Total agendas: {len(st.session_state.agendas)}")
        else:
            st.warning("No agendas to export yet.")
    
    with col2:
        st.markdown("### 📥 Import Data")
        st.markdown("Upload a previously exported JSON file to restore your agendas.")
        
        uploaded_file = st.file_uploader("Choose a JSON file", type=['json'])
        
        if uploaded_file is not None:
            try:
                content = uploaded_file.getvalue().decode('utf-8')
                preview_data = json.loads(content)
                
                st.info(f"📊 Found {len(preview_data)} agenda(s) in file")
                
                if st.button("📤 Import Agendas", use_container_width=True, type="primary"):
                    success, message = import_data(content)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    init_session_state()
    render_sidebar()
    
    # Route to appropriate view
    view = st.session_state.current_view
    
    if view == 'list':
        render_agenda_list()
    elif view == 'create':
        render_agenda_form()
    elif view == 'detail' and st.session_state.selected_agenda_id:
        render_agenda_detail(st.session_state.selected_agenda_id)
    elif view == 'settings':
        render_email_settings()
    elif view == 'import_export':
        render_import_export()
    else:
        render_agenda_list()

if __name__ == "__main__":
    main()
