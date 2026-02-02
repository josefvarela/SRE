"""
Meeting Agenda Manager - A Streamlit App with Material UI Styling
Allows creating, updating, and deleting meeting agendas, notes, action items, and follow-ups
"""

import streamlit as st
from datetime import datetime, date, time
import uuid
import json

# Page configuration
st.set_page_config(
    page_title="Meeting Agenda Manager",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Material UI Inspired CSS with Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Root Variables - Material Design Color Palette */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --primary-light: #818cf8;
        --secondary: #10b981;
        --secondary-dark: #059669;
        --accent: #f59e0b;
        --danger: #ef4444;
        --danger-dark: #dc2626;
        --surface: #1e1e2e;
        --surface-light: #2a2a3e;
        --surface-lighter: #363650;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --border: #3f3f5a;
        --shadow: rgba(0, 0, 0, 0.3);
        --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        --gradient-secondary: linear-gradient(135deg, #10b981 0%, #14b8a6 100%);
    }
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Animation Keyframes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4);
        }
        50% {
            transform: scale(1.02);
            box-shadow: 0 0 20px 10px rgba(99, 102, 241, 0);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -200% center;
        }
        100% {
            background-position: 200% center;
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 5px rgba(99, 102, 241, 0.5), 0 0 10px rgba(99, 102, 241, 0.3);
        }
        50% {
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.8), 0 0 30px rgba(99, 102, 241, 0.5);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes ripple {
        0% {
            transform: scale(0);
            opacity: 1;
        }
        100% {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    /* Main Header */
    .main-header {
        background: var(--gradient-primary);
        padding: 2rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        animation: fadeInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(99, 102, 241, 0.3);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -200%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Card Styles */
    .meeting-card {
        background: var(--surface);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .meeting-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--gradient-primary);
        border-radius: 4px 0 0 4px;
    }
    
    .meeting-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2);
        border-color: var(--primary);
    }
    
    .meeting-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    
    .meeting-title {
        color: var(--text-primary);
        font-size: 1.4rem;
        font-weight: 600;
        margin: 0;
    }
    
    .meeting-topic {
        color: var(--primary-light);
        font-size: 1rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }
    
    .meeting-meta {
        display: flex;
        gap: 1.5rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    
    .meta-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .meta-icon {
        width: 18px;
        height: 18px;
        fill: var(--primary-light);
    }
    
    .meeting-description {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
        padding: 1rem;
        background: var(--surface-light);
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Badge Styles */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.35rem 0.85rem;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        animation: fadeInRight 0.5s ease-out;
    }
    
    .badge-primary {
        background: rgba(99, 102, 241, 0.2);
        color: var(--primary-light);
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    .badge-success {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .badge-warning {
        background: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .badge-danger {
        background: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 1.5rem 0 1rem 0;
        animation: fadeInLeft 0.5s ease-out;
    }
    
    .section-header h3 {
        color: var(--text-primary);
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
    }
    
    .section-icon {
        width: 24px;
        height: 24px;
        padding: 6px;
        background: var(--gradient-primary);
        border-radius: 8px;
    }
    
    /* List Items */
    .list-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.75rem 1rem;
        background: var(--surface-light);
        border-radius: 10px;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
        animation: slideIn 0.4s ease-out;
        border-left: 3px solid transparent;
    }
    
    .list-item:hover {
        background: var(--surface-lighter);
        border-left-color: var(--primary);
        transform: translateX(5px);
    }
    
    .list-item-content {
        flex: 1;
        color: var(--text-primary);
        font-size: 0.9rem;
    }
    
    .list-item-checkbox {
        width: 20px;
        height: 20px;
        border-radius: 4px;
        border: 2px solid var(--primary);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .list-item-checkbox.checked {
        background: var(--primary);
    }
    
    /* Button Styles */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.9rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Form Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        background: var(--surface-light) !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-family: 'Poppins', sans-serif !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }
    
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stDateInput > label,
    .stTimeInput > label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Date and Time Inputs */
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        background: var(--surface-light) !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--surface) 0%, #12121e 100%) !important;
        border-right: 1px solid var(--border);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        animation: fadeInLeft 0.6s ease-out;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--surface) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        gap: 0.5rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 10px !important;
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--surface-light) !important;
        color: var(--text-primary) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--gradient-primary) !important;
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--surface-light) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: var(--primary) !important;
        background: var(--surface-lighter) !important;
    }
    
    .streamlit-expanderContent {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* Divider */
    hr {
        border-color: var(--border) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Success/Warning/Error Messages */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 12px !important;
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* URL Link */
    .url-link {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--primary-light);
        text-decoration: none;
        padding: 0.5rem 1rem;
        background: rgba(99, 102, 241, 0.1);
        border-radius: 8px;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .url-link:hover {
        background: rgba(99, 102, 241, 0.2);
        transform: translateX(5px);
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    .empty-state h3 {
        color: var(--text-primary);
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .empty-state p {
        color: var(--text-secondary);
        font-size: 1rem;
    }
    
    /* Action Buttons Container */
    .action-buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    /* Floating Action Button */
    .fab {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: var(--gradient-primary);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
        z-index: 1000;
    }
    
    .fab:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.5);
    }
    
    /* Stats Card */
    .stats-card {
        background: var(--surface);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid var(--border);
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stats-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: var(--text-primary) !important;
    }
    
    .stCheckbox > label > span {
        color: var(--text-primary) !important;
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: var(--text-primary) !important;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        background: var(--surface-light) !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
    }
    
    /* File uploader */
    .stFileUploader > div > div {
        background: var(--surface-light) !important;
        border: 2px dashed var(--border) !important;
        border-radius: 12px !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: var(--primary) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--surface);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }
    
    /* Animations for dynamic content */
    .animate-in {
        animation: fadeInUp 0.5s ease-out;
    }
    
    .stMarkdown {
        color: var(--text-primary);
    }
    
    /* Delete button specific */
    .delete-btn button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
    }
    
    .delete-btn button:hover {
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.4) !important;
    }
    
    /* Edit button specific */
    .edit-btn button {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3) !important;
    }
    
    /* Secondary button */
    .secondary-btn button {
        background: var(--surface-lighter) !important;
        border: 2px solid var(--border) !important;
        box-shadow: none !important;
    }
    
    .secondary-btn button:hover {
        border-color: var(--primary) !important;
        background: var(--surface-light) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data storage
if 'meetings' not in st.session_state:
    st.session_state.meetings = {}

if 'current_view' not in st.session_state:
    st.session_state.current_view = 'list'

if 'editing_meeting' not in st.session_state:
    st.session_state.editing_meeting = None

if 'selected_meeting' not in st.session_state:
    st.session_state.selected_meeting = None

def generate_id():
    """Generate a unique ID for meetings and items"""
    return str(uuid.uuid4())[:8]

def create_meeting(name, meeting_date, meeting_time, topic, description, attachments, url_name, url):
    """Create a new meeting agenda"""
    meeting_id = generate_id()
    st.session_state.meetings[meeting_id] = {
        'id': meeting_id,
        'name': name,
        'date': meeting_date.isoformat() if meeting_date else None,
        'time': meeting_time.isoformat() if meeting_time else None,
        'topic': topic,
        'description': description,
        'attachments': attachments,
        'url_name': url_name,
        'url': url,
        'created_at': datetime.now().isoformat(),
        'notes': [],
        'action_items': [],
        'follow_ups': []
    }
    return meeting_id

def update_meeting(meeting_id, **kwargs):
    """Update an existing meeting"""
    if meeting_id in st.session_state.meetings:
        for key, value in kwargs.items():
            if key in ['date', 'time'] and value:
                st.session_state.meetings[meeting_id][key] = value.isoformat()
            else:
                st.session_state.meetings[meeting_id][key] = value
        return True
    return False

def delete_meeting(meeting_id):
    """Delete a meeting"""
    if meeting_id in st.session_state.meetings:
        del st.session_state.meetings[meeting_id]
        return True
    return False

def add_note(meeting_id, note):
    """Add a note to a meeting"""
    if meeting_id in st.session_state.meetings:
        note_id = generate_id()
        st.session_state.meetings[meeting_id]['notes'].append({
            'id': note_id,
            'content': note,
            'created_at': datetime.now().isoformat()
        })
        return note_id
    return None

def add_action_item(meeting_id, item, assignee="", due_date=None):
    """Add an action item to a meeting"""
    if meeting_id in st.session_state.meetings:
        item_id = generate_id()
        st.session_state.meetings[meeting_id]['action_items'].append({
            'id': item_id,
            'content': item,
            'assignee': assignee,
            'due_date': due_date.isoformat() if due_date else None,
            'completed': False,
            'created_at': datetime.now().isoformat()
        })
        return item_id
    return None

def add_follow_up(meeting_id, item, priority="Medium"):
    """Add a follow-up item to a meeting"""
    if meeting_id in st.session_state.meetings:
        item_id = generate_id()
        st.session_state.meetings[meeting_id]['follow_ups'].append({
            'id': item_id,
            'content': item,
            'priority': priority,
            'completed': False,
            'created_at': datetime.now().isoformat()
        })
        return item_id
    return None

def toggle_action_item(meeting_id, item_id):
    """Toggle completion status of an action item"""
    if meeting_id in st.session_state.meetings:
        for item in st.session_state.meetings[meeting_id]['action_items']:
            if item['id'] == item_id:
                item['completed'] = not item['completed']
                return True
    return False

def toggle_follow_up(meeting_id, item_id):
    """Toggle completion status of a follow-up item"""
    if meeting_id in st.session_state.meetings:
        for item in st.session_state.meetings[meeting_id]['follow_ups']:
            if item['id'] == item_id:
                item['completed'] = not item['completed']
                return True
    return False

def delete_note(meeting_id, note_id):
    """Delete a note from a meeting"""
    if meeting_id in st.session_state.meetings:
        st.session_state.meetings[meeting_id]['notes'] = [
            n for n in st.session_state.meetings[meeting_id]['notes'] if n['id'] != note_id
        ]
        return True
    return False

def delete_action_item(meeting_id, item_id):
    """Delete an action item from a meeting"""
    if meeting_id in st.session_state.meetings:
        st.session_state.meetings[meeting_id]['action_items'] = [
            i for i in st.session_state.meetings[meeting_id]['action_items'] if i['id'] != item_id
        ]
        return True
    return False

def delete_follow_up(meeting_id, item_id):
    """Delete a follow-up item from a meeting"""
    if meeting_id in st.session_state.meetings:
        st.session_state.meetings[meeting_id]['follow_ups'] = [
            i for i in st.session_state.meetings[meeting_id]['follow_ups'] if i['id'] != item_id
        ]
        return True
    return False

def render_header():
    """Render the main header"""
    st.markdown("""
        <div class="main-header">
            <h1>📋 Meeting Agenda Manager</h1>
            <p>Create, organize, and track your meetings with style</p>
        </div>
    """, unsafe_allow_html=True)

def render_stats():
    """Render statistics cards"""
    total_meetings = len(st.session_state.meetings)
    total_action_items = sum(len(m['action_items']) for m in st.session_state.meetings.values())
    completed_actions = sum(
        sum(1 for i in m['action_items'] if i['completed']) 
        for m in st.session_state.meetings.values()
    )
    total_follow_ups = sum(len(m['follow_ups']) for m in st.session_state.meetings.values())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{total_meetings}</div>
                <div class="stats-label">Total Meetings</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{total_action_items}</div>
                <div class="stats-label">Action Items</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{completed_actions}</div>
                <div class="stats-label">Completed Actions</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{total_follow_ups}</div>
                <div class="stats-label">Follow-ups</div>
            </div>
        """, unsafe_allow_html=True)

def render_meeting_form(editing=False, meeting_data=None):
    """Render the meeting creation/edit form"""
    with st.form(key="meeting_form", clear_on_submit=not editing):
        st.markdown("### " + ("✏️ Edit Meeting" if editing else "➕ Create New Meeting"))
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Meeting Name *",
                value=meeting_data.get('name', '') if meeting_data else '',
                placeholder="e.g., Q1 Planning Session"
            )
            
            meeting_date = st.date_input(
                "Date *",
                value=date.fromisoformat(meeting_data['date']) if meeting_data and meeting_data.get('date') else date.today()
            )
            
            topic = st.text_input(
                "Topic *",
                value=meeting_data.get('topic', '') if meeting_data else '',
                placeholder="e.g., Budget Review"
            )
            
            url_name = st.text_input(
                "URL Name",
                value=meeting_data.get('url_name', '') if meeting_data else '',
                placeholder="e.g., Meeting Link"
            )
        
        with col2:
            meeting_time = st.time_input(
                "Time *",
                value=time.fromisoformat(meeting_data['time']) if meeting_data and meeting_data.get('time') else time(9, 0)
            )
            
            attachments = st.text_input(
                "Attachments",
                value=meeting_data.get('attachments', '') if meeting_data else '',
                placeholder="e.g., report.pdf, slides.pptx"
            )
            
            url = st.text_input(
                "URL",
                value=meeting_data.get('url', '') if meeting_data else '',
                placeholder="e.g., https://zoom.us/j/123456"
            )
        
        description = st.text_area(
            "Brief Description",
            value=meeting_data.get('description', '') if meeting_data else '',
            placeholder="Enter a brief description of the meeting agenda...",
            height=100
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submitted = st.form_submit_button(
                "💾 Save Meeting" if editing else "➕ Create Meeting",
                use_container_width=True
            )
        
        with col2:
            if editing:
                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                if cancel:
                    st.session_state.editing_meeting = None
                    st.rerun()
        
        if submitted:
            if not name or not topic:
                st.error("Please fill in all required fields (Name and Topic)")
            else:
                if editing and meeting_data:
                    update_meeting(
                        meeting_data['id'],
                        name=name,
                        date=meeting_date,
                        time=meeting_time,
                        topic=topic,
                        description=description,
                        attachments=attachments,
                        url_name=url_name,
                        url=url
                    )
                    st.session_state.editing_meeting = None
                    st.success("✅ Meeting updated successfully!")
                else:
                    create_meeting(
                        name=name,
                        meeting_date=meeting_date,
                        meeting_time=meeting_time,
                        topic=topic,
                        description=description,
                        attachments=attachments,
                        url_name=url_name,
                        url=url
                    )
                    st.success("✅ Meeting created successfully!")
                st.rerun()

def render_meeting_card(meeting):
    """Render a single meeting card"""
    meeting_date = date.fromisoformat(meeting['date']) if meeting.get('date') else None
    meeting_time = time.fromisoformat(meeting['time']) if meeting.get('time') else None
    
    date_str = meeting_date.strftime("%B %d, %Y") if meeting_date else "No date"
    time_str = meeting_time.strftime("%I:%M %p") if meeting_time else "No time"
    
    action_count = len(meeting.get('action_items', []))
    completed_count = sum(1 for i in meeting.get('action_items', []) if i.get('completed'))
    notes_count = len(meeting.get('notes', []))
    followup_count = len(meeting.get('follow_ups', []))
    
    st.markdown(f"""
        <div class="meeting-card">
            <div class="meeting-card-header">
                <div>
                    <h3 class="meeting-title">{meeting['name']}</h3>
                    <p class="meeting-topic">📌 {meeting['topic']}</p>
                </div>
                <div>
                    <span class="badge badge-primary">ID: {meeting['id']}</span>
                </div>
            </div>
            <div class="meeting-meta">
                <div class="meta-item">
                    📅 {date_str}
                </div>
                <div class="meta-item">
                    ⏰ {time_str}
                </div>
                <div class="meta-item">
                    📝 {notes_count} Notes
                </div>
                <div class="meta-item">
                    ✅ {completed_count}/{action_count} Actions
                </div>
                <div class="meta-item">
                    🔄 {followup_count} Follow-ups
                </div>
            </div>
            {f'<div class="meeting-description">{meeting["description"]}</div>' if meeting.get('description') else ''}
            {f'<a href="{meeting["url"]}" target="_blank" class="url-link">🔗 {meeting.get("url_name", "Meeting Link")}</a>' if meeting.get('url') else ''}
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📝 View/Edit", key=f"view_{meeting['id']}", use_container_width=True):
            st.session_state.selected_meeting = meeting['id']
            st.rerun()
    
    with col2:
        if st.button("🗑️ Delete", key=f"delete_{meeting['id']}", use_container_width=True):
            delete_meeting(meeting['id'])
            st.success("Meeting deleted!")
            st.rerun()

def render_meeting_details(meeting_id):
    """Render detailed view of a meeting with notes, action items, and follow-ups"""
    meeting = st.session_state.meetings.get(meeting_id)
    
    if not meeting:
        st.error("Meeting not found!")
        return
    
    # Back button
    if st.button("← Back to Meetings"):
        st.session_state.selected_meeting = None
        st.rerun()
    
    st.markdown("---")
    
    # Meeting header
    meeting_date = date.fromisoformat(meeting['date']) if meeting.get('date') else None
    meeting_time = time.fromisoformat(meeting['time']) if meeting.get('time') else None
    
    date_str = meeting_date.strftime("%B %d, %Y") if meeting_date else "No date"
    time_str = meeting_time.strftime("%I:%M %p") if meeting_time else "No time"
    
    st.markdown(f"""
        <div class="meeting-card">
            <div class="meeting-card-header">
                <div>
                    <h2 class="meeting-title" style="font-size: 1.8rem;">{meeting['name']}</h2>
                    <p class="meeting-topic" style="font-size: 1.2rem;">📌 {meeting['topic']}</p>
                </div>
            </div>
            <div class="meeting-meta">
                <div class="meta-item">📅 {date_str}</div>
                <div class="meta-item">⏰ {time_str}</div>
                {f'<div class="meta-item">📎 {meeting["attachments"]}</div>' if meeting.get('attachments') else ''}
            </div>
            {f'<div class="meeting-description">{meeting["description"]}</div>' if meeting.get('description') else ''}
            {f'<a href="{meeting["url"]}" target="_blank" class="url-link">🔗 {meeting.get("url_name", "Meeting Link")}</a>' if meeting.get('url') else ''}
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✏️ Edit Meeting Details", use_container_width=True):
            st.session_state.editing_meeting = meeting_id
            st.rerun()
    
    with col2:
        if st.button("🗑️ Delete Meeting", use_container_width=True):
            delete_meeting(meeting_id)
            st.session_state.selected_meeting = None
            st.success("Meeting deleted!")
            st.rerun()
    
    st.markdown("---")
    
    # Tabs for Notes, Action Items, Follow-ups
    tab1, tab2, tab3 = st.tabs(["📝 Meeting Notes", "✅ Action Items", "🔄 Follow-ups"])
    
    with tab1:
        render_notes_section(meeting_id, meeting)
    
    with tab2:
        render_action_items_section(meeting_id, meeting)
    
    with tab3:
        render_follow_ups_section(meeting_id, meeting)

def render_notes_section(meeting_id, meeting):
    """Render the notes section"""
    st.markdown("""
        <div class="section-header">
            <h3>📝 Meeting Notes</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Add new note
    with st.form(key="add_note_form", clear_on_submit=True):
        new_note = st.text_area(
            "Add a new note",
            placeholder="Enter meeting notes here...",
            height=100
        )
        
        if st.form_submit_button("➕ Add Note", use_container_width=True):
            if new_note.strip():
                add_note(meeting_id, new_note)
                st.success("Note added!")
                st.rerun()
            else:
                st.warning("Please enter a note")
    
    # Display existing notes
    if meeting.get('notes'):
        for note in meeting['notes']:
            with st.container():
                col1, col2 = st.columns([6, 1])
                
                with col1:
                    created_at = datetime.fromisoformat(note['created_at']).strftime("%b %d, %Y %I:%M %p")
                    st.markdown(f"""
                        <div class="list-item">
                            <div class="list-item-content">
                                <p style="margin: 0; color: #f8fafc;">{note['content']}</p>
                                <small style="color: #94a3b8;">Added: {created_at}</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("🗑️", key=f"del_note_{note['id']}"):
                        delete_note(meeting_id, note['id'])
                        st.rerun()
    else:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📝</div>
                <h3>No notes yet</h3>
                <p>Add notes to capture important discussion points</p>
            </div>
        """, unsafe_allow_html=True)

def render_action_items_section(meeting_id, meeting):
    """Render the action items section"""
    st.markdown("""
        <div class="section-header">
            <h3>✅ Action Items</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Add new action item
    with st.form(key="add_action_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            action_content = st.text_input(
                "Action Item",
                placeholder="What needs to be done?"
            )
            assignee = st.text_input(
                "Assignee",
                placeholder="Who is responsible?"
            )
        
        with col2:
            due_date = st.date_input(
                "Due Date",
                value=None
            )
        
        if st.form_submit_button("➕ Add Action Item", use_container_width=True):
            if action_content.strip():
                add_action_item(meeting_id, action_content, assignee, due_date)
                st.success("Action item added!")
                st.rerun()
            else:
                st.warning("Please enter an action item")
    
    # Display existing action items
    if meeting.get('action_items'):
        for item in meeting['action_items']:
            with st.container():
                col1, col2, col3 = st.columns([0.5, 5.5, 1])
                
                with col1:
                    completed = st.checkbox(
                        "Done",
                        value=item['completed'],
                        key=f"check_{item['id']}",
                        label_visibility="collapsed"
                    )
                    if completed != item['completed']:
                        toggle_action_item(meeting_id, item['id'])
                        st.rerun()
                
                with col2:
                    due_str = ""
                    if item.get('due_date'):
                        due_date = date.fromisoformat(item['due_date'])
                        due_str = f"Due: {due_date.strftime('%b %d, %Y')}"
                    
                    status_style = "text-decoration: line-through; opacity: 0.6;" if item['completed'] else ""
                    badge_class = "badge-success" if item['completed'] else "badge-warning"
                    badge_text = "Completed" if item['completed'] else "Pending"
                    
                    st.markdown(f"""
                        <div class="list-item">
                            <div class="list-item-content" style="{status_style}">
                                <p style="margin: 0; color: #f8fafc;">{item['content']}</p>
                                <small style="color: #94a3b8;">
                                    {f'Assignee: {item["assignee"]} | ' if item.get('assignee') else ''}{due_str}
                                </small>
                            </div>
                            <span class="badge {badge_class}">{badge_text}</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    if st.button("🗑️", key=f"del_action_{item['id']}"):
                        delete_action_item(meeting_id, item['id'])
                        st.rerun()
    else:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">✅</div>
                <h3>No action items yet</h3>
                <p>Add action items to track tasks and responsibilities</p>
            </div>
        """, unsafe_allow_html=True)

def render_follow_ups_section(meeting_id, meeting):
    """Render the follow-ups section"""
    st.markdown("""
        <div class="section-header">
            <h3>🔄 Follow-up Items</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Add new follow-up
    with st.form(key="add_followup_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            followup_content = st.text_input(
                "Follow-up Item",
                placeholder="What needs follow-up?"
            )
        
        with col2:
            priority = st.selectbox(
                "Priority",
                options=["Low", "Medium", "High", "Critical"]
            )
        
        if st.form_submit_button("➕ Add Follow-up", use_container_width=True):
            if followup_content.strip():
                add_follow_up(meeting_id, followup_content, priority)
                st.success("Follow-up added!")
                st.rerun()
            else:
                st.warning("Please enter a follow-up item")
    
    # Display existing follow-ups
    if meeting.get('follow_ups'):
        for item in meeting['follow_ups']:
            with st.container():
                col1, col2, col3 = st.columns([0.5, 5.5, 1])
                
                with col1:
                    completed = st.checkbox(
                        "Done",
                        value=item['completed'],
                        key=f"followup_check_{item['id']}",
                        label_visibility="collapsed"
                    )
                    if completed != item['completed']:
                        toggle_follow_up(meeting_id, item['id'])
                        st.rerun()
                
                with col2:
                    priority_colors = {
                        "Low": "badge-primary",
                        "Medium": "badge-warning",
                        "High": "badge-danger",
                        "Critical": "badge-danger"
                    }
                    badge_class = priority_colors.get(item.get('priority', 'Medium'), 'badge-primary')
                    
                    status_style = "text-decoration: line-through; opacity: 0.6;" if item['completed'] else ""
                    
                    st.markdown(f"""
                        <div class="list-item">
                            <div class="list-item-content" style="{status_style}">
                                <p style="margin: 0; color: #f8fafc;">{item['content']}</p>
                            </div>
                            <span class="badge {badge_class}">{item.get('priority', 'Medium')}</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    if st.button("🗑️", key=f"del_followup_{item['id']}"):
                        delete_follow_up(meeting_id, item['id'])
                        st.rerun()
    else:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🔄</div>
                <h3>No follow-ups yet</h3>
                <p>Add follow-up items to track pending tasks</p>
            </div>
        """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h2 style="color: #f8fafc; margin: 0;">📋 Agenda Manager</h2>
                <p style="color: #94a3b8; font-size: 0.9rem;">Organize your meetings</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick stats
        total = len(st.session_state.meetings)
        upcoming = sum(
            1 for m in st.session_state.meetings.values()
            if m.get('date') and date.fromisoformat(m['date']) >= date.today()
        )
        
        st.markdown(f"""
            <div style="padding: 1rem; background: rgba(99, 102, 241, 0.1); border-radius: 12px; margin-bottom: 1rem;">
                <p style="color: #818cf8; margin: 0; font-size: 0.85rem;">QUICK STATS</p>
                <p style="color: #f8fafc; margin: 0.5rem 0 0 0;">📊 Total: {total} meetings</p>
                <p style="color: #f8fafc; margin: 0.25rem 0 0 0;">📅 Upcoming: {upcoming}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 🧭 Navigation")
        
        if st.button("📋 All Meetings", use_container_width=True):
            st.session_state.selected_meeting = None
            st.session_state.editing_meeting = None
            st.session_state.current_view = 'list'
            st.rerun()
        
        if st.button("➕ New Meeting", use_container_width=True):
            st.session_state.selected_meeting = None
            st.session_state.editing_meeting = None
            st.session_state.current_view = 'create'
            st.rerun()
        
        st.markdown("---")
        
        # Recent meetings quick access
        if st.session_state.meetings:
            st.markdown("### 🕐 Recent Meetings")
            
            sorted_meetings = sorted(
                st.session_state.meetings.values(),
                key=lambda x: x.get('created_at', ''),
                reverse=True
            )[:5]
            
            for meeting in sorted_meetings:
                if st.button(
                    f"📌 {meeting['name'][:20]}...",
                    key=f"sidebar_{meeting['id']}",
                    use_container_width=True
                ):
                    st.session_state.selected_meeting = meeting['id']
                    st.rerun()
        
        st.markdown("---")
        
        # Info
        st.markdown("""
            <div style="padding: 1rem; background: rgba(16, 185, 129, 0.1); border-radius: 12px;">
                <p style="color: #34d399; margin: 0; font-size: 0.85rem;">💡 TIP</p>
                <p style="color: #94a3b8; margin: 0.5rem 0 0 0; font-size: 0.8rem;">
                    Click on a meeting to view details, add notes, action items, and follow-ups!
                </p>
            </div>
        """, unsafe_allow_html=True)

def main():
    """Main application logic"""
    render_sidebar()
    
    # Check if we're editing a meeting
    if st.session_state.editing_meeting:
        meeting_data = st.session_state.meetings.get(st.session_state.editing_meeting)
        if meeting_data:
            render_header()
            render_meeting_form(editing=True, meeting_data=meeting_data)
        return
    
    # Check if viewing a specific meeting
    if st.session_state.selected_meeting:
        render_header()
        render_meeting_details(st.session_state.selected_meeting)
        return
    
    # Default views
    render_header()
    
    if st.session_state.current_view == 'create':
        render_meeting_form()
        st.markdown("---")
    
    # Stats section
    render_stats()
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["📋 All Meetings", "➕ Create New"])
    
    with tab1:
        if st.session_state.meetings:
            # Sort meetings by date
            sorted_meetings = sorted(
                st.session_state.meetings.values(),
                key=lambda x: (x.get('date', ''), x.get('time', '')),
                reverse=True
            )
            
            # Search/filter
            search = st.text_input("🔍 Search meetings...", placeholder="Search by name or topic")
            
            if search:
                sorted_meetings = [
                    m for m in sorted_meetings
                    if search.lower() in m['name'].lower() or search.lower() in m.get('topic', '').lower()
                ]
            
            if sorted_meetings:
                for meeting in sorted_meetings:
                    render_meeting_card(meeting)
            else:
                st.info("No meetings found matching your search.")
        else:
            st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-icon">📋</div>
                    <h3>No meetings yet</h3>
                    <p>Create your first meeting agenda to get started!</p>
                </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        render_meeting_form()

if __name__ == "__main__":
    main()
