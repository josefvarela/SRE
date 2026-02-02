# 📋 Meeting Agenda Manager

A beautiful, animated Streamlit application with Material UI-inspired styling for managing meeting agendas, notes, action items, and follow-ups.

## Features

### Meeting Agenda Management
- **Create meetings** with comprehensive details:
  - Name
  - Date & Time
  - Topic
  - Brief Description
  - Attachments (text field for file names)
  - URL Name & URL (for meeting links)
  
- **Full CRUD Operations**:
  - Create new meeting agendas
  - Read/View meeting details
  - Update/Edit existing meetings
  - Delete meetings

### Post-Meeting Management
Once a meeting is created, you can add:
- **📝 Meeting Notes**: Capture important discussion points
- **✅ Action Items**: Track tasks with assignees and due dates
- **🔄 Follow-ups**: Monitor pending items with priority levels

### UI Features
- **Material UI-inspired design** with dark theme
- **Smooth animations** including:
  - Fade-in effects
  - Slide-in animations
  - Hover effects
  - Pulse animations
  - Shimmer effects
- **Responsive layout** with sidebar navigation
- **Quick stats dashboard**
- **Search functionality**

## Installation

1. Make sure you have Python 3.8+ installed

2. Install the required package:
```bash
pip install streamlit
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

## Running the App

Run the following command in your terminal:

```bash
streamlit run meeting_agenda_app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Data Storage

All data is stored locally in Streamlit's session state. This means:
- Data persists during your browser session
- Data is lost when you refresh the page or close the browser
- No external database required

For production use, you may want to integrate a database like SQLite, PostgreSQL, or use Streamlit's `st.cache_data` with file-based storage.

## Screenshots

The app features:
- A stunning gradient header
- Card-based meeting display
- Tabbed interface for notes, actions, and follow-ups
- Statistics dashboard with animated cards
- Sidebar navigation with quick access

## Customization

### Colors
The color scheme can be modified by editing the CSS variables in the `:root` section:

```css
:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --secondary: #10b981;
    /* ... etc */
}
```

### Animations
Animation speeds and effects can be adjusted in the `@keyframes` sections of the CSS.

## License

Free to use and modify.
