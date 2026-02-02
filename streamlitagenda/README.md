# 📋 Meeting Agenda Manager

A comprehensive Streamlit application for creating, editing, and managing meeting agendas with notes, to-dos, action items, and email distribution capabilities.

## ✨ Features

### Agenda Management
- **Create, Edit, Delete** meeting agendas
- **Topic** with optional image display
- **Presenter Name** 
- **Date and Time** scheduling
- **Duration** tracking
- **URL Links** with custom names
- **File Attachments** (supports JPG, PNG, PDF, Excel, PowerPoint, Word)

### Meeting Items
- **📝 Notes** - Add meeting notes with timestamps
- **✅ To-Do Items** - Task management with priority levels and assignees
- **🎯 Action Items** - Track actions with owners, due dates, and status

### Email Distribution
- Send formatted HTML emails with meeting agendas
- Configure SMTP settings (Gmail, Outlook, etc.)
- Save distribution lists for quick access
- Select which sections to include in emails
- Attachments included automatically

### Data Management
- **Export** all agendas to JSON
- **Import** previously exported data
- Session-based storage (data persists during session)
- Search and filter agendas

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project files**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run meeting_agenda_manager.py
```

4. **Open your browser** to `http://localhost:8501`

## 📖 Usage Guide

### Creating an Agenda

1. Click **"➕ Create New"** in the sidebar
2. Fill in the required fields:
   - Topic (required)
   - Presenter Name (required)
   - Date and Time
   - Duration
3. Optionally add:
   - Topic image (displayed next to the title)
   - Related URLs with names
   - File attachments
4. Click **"✨ Create Agenda"**

### Managing Meeting Items

Once you've created an agenda, click **"📖 View"** to access:

#### Notes Tab
- Add meeting notes with the "➕ Add New Note" expander
- Notes are timestamped automatically
- Delete notes with the 🗑️ button

#### To-Do Items Tab
- Add tasks with priority (Low/Medium/High)
- Assign to team members
- Toggle completion status with ✓/✗ button
- Visual indicators for priority and completion

#### Action Items Tab
- Track specific actions needed
- Assign owners and due dates
- Update status (Pending → In Progress → Completed)
- Priority-based visual indicators

### Email Distribution

1. Open an agenda and click **"📧 Email"**
2. Enter recipient email addresses (one per line)
3. Customize the subject line
4. Select which sections to include:
   - URLs
   - Notes
   - To-Do Items
   - Action Items
5. Configure SMTP settings:
   - **Gmail**: Use `smtp.gmail.com`, port `587`
   - Generate an [App Password](https://myaccount.google.com/apppasswords)
6. Click **"📤 Send Email"**

### Data Backup

#### Export
1. Go to **"📁 Import/Export"** in the sidebar
2. Click **"📥 Download All Agendas (JSON)"**
3. Save the file to your computer

#### Import
1. Go to **"📁 Import/Export"**
2. Upload your previously exported JSON file
3. Click **"📤 Import Agendas"**

## ⚙️ Email Configuration

### Gmail Setup
1. Enable 2-Factor Authentication on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new app password for "Mail"
4. Use these settings:
   - **SMTP Server**: `smtp.gmail.com`
   - **SMTP Port**: `587`
   - **Sender Email**: Your Gmail address
   - **App Password**: The generated app password

### Outlook/Microsoft 365
- **SMTP Server**: `smtp.office365.com`
- **SMTP Port**: `587`

## 📁 Project Structure

```
meeting_agenda_app/
├── meeting_agenda_manager.py  # Main application
├── requirements.txt           # Python dependencies
└── README.md                 # This documentation
```

## 🔧 Technical Details

### Data Storage
- All data is stored in Streamlit's `session_state`
- Data persists during the browser session
- Use Export/Import for permanent storage
- Files are stored as Base64-encoded strings

### Supported File Types
- **Images**: JPG, JPEG, PNG, GIF, WebP
- **Documents**: PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🎨 Customization

The application uses custom CSS for styling. To customize the appearance, modify the CSS in the `st.markdown()` section near the top of `meeting_agenda_manager.py`.

## 📝 License

This project is provided as-is for personal and commercial use.

## 🤝 Support

For issues or feature requests, please contact your system administrator or modify the code as needed.

---

**Built with ❤️ using Streamlit**
