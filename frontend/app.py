import streamlit as st
import requests
import time
import datetime
from datetime import datetime
import threading
import random

# Set page configuration for a cleaner look
st.set_page_config(
    page_title="Personal Diary",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to make the app look more like Google Keep
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #f9f9f9;
        padding: 10px;
    }
    
    /* Card styling */
    .diary-card {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        transition: all 0.2s cubic-bezier(.25,.8,.25,1);
        overflow: hidden;
        position: relative;
        border: 1px solid #e0e0e0;
        cursor: pointer;
    }
    
    .diary-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Card title styling */
    .card-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #202124;
        display: flex;
        justify-content: space-between;
    }
    
    /* Card content styling */
    .card-content {
        font-size: 14px;
        margin-bottom: 10px;
        color: #5f6368;
        white-space: pre-wrap;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 5;
        -webkit-box-orient: vertical;
    }
    
    /* List view specific styling */
    .list-item .card-content {
        display: none; /* Hide content in list view */
    }
    
    .list-item .tag-container,
    .list-item .date-text {
        display: none; /* Hide tags and date in list view */
    }
    
    /* Detailed view styling */
    .detail-view {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        padding: 25px;
        margin: 20px 0;
        border: 1px solid #e0e0e0;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .detail-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #202124;
        padding-bottom: 10px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .detail-content {
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 20px;
        color: #3c4043;
        white-space: pre-wrap;
    }
    
    .detail-actions {
        display: flex;
        justify-content: space-between;
        border-top: 1px solid #e0e0e0;
        padding-top: 15px;
        margin-top: 15px;
    }
    
    .detail-meta {
        margin-top: 15px;
        color: #5f6368;
        font-size: 14px;
    }
    
    /* Tag styling */
    .tag-container {
        margin-top: 10px;
        display: flex;
        flex-wrap: wrap;
    }
    
    .tag {
        display: inline-block;
        background-color: #e0e0e0;
        border-radius: 15px;
        padding: 2px 8px;
        margin-right: 5px;
        margin-bottom: 5px;
        font-size: 12px;
        color: #5f6368;
        font-weight: 500;
        box-shadow: 0 1px 1px rgba(0,0,0,0.05);
    }
    
    /* Tag colors */
    .tag-Personal { background-color: #fdcfe8; color: #c51162; }
    .tag-Work { background-color: #d7aefb; color: #6200ee; }
    .tag-Ideas { background-color: #a7ffeb; color: #00bfa5; }
    .tag-Important { background-color: #fff8e1; color: #ff6d00; }
    .tag-To-Do { background-color: #ccff90; color: #64dd17; }
    
    /* Action button styling */
    .stButton>button {
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 12px;
        margin: 2px;
        background-color: transparent;
        color: #5f6368;
        border: 1px solid #e0e0e0;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #f5f5f5;
        color: #202124;
        border-color: #d0d0d0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Pin icon */
    .pin-icon {
        font-size: 18px;
        color: #f4b400;
        margin-left: 8px;
    }
    
    /* Back button styling */
    .back-button {
        display: inline-flex;
        align-items: center;
        margin-bottom: 15px;
        color: #4285f4;
        background-color: transparent;
        border: none;
        cursor: pointer;
        padding: 5px 10px;
        border-radius: 4px;
        font-weight: 500;
    }
    
    .back-button:hover {
        background-color: #f1f3f4;
    }
    
    .back-button svg {
        margin-right: 5px;
    }
    
    /* Masonry grid layout */
    .masonry-grid {
        column-count: 3;
        column-gap: 15px;
    }
    
    .masonry-item {
        display: inline-block;
        width: 100%;
        margin-bottom: 15px;
    }
    
    /* List view styling */
    .list-item {
        margin-bottom: 10px;
        max-width: 800px;
    }
    
    .list-item .diary-card {
        border-left: 4px solid #4285f4;
        border-radius: 0 8px 8px 0;
        padding: 8px 15px; /* Reduced padding for more compact cards */
        margin-bottom: 8px; /* Less space between list items */
    }
    
    .list-item .card-title {
        margin-bottom: 0; /* Remove bottom margin in list view */
    }
    
    .list-item .diary-card:hover {
        border-left: 4px solid #0d5bdd;
    }
    
    /* Responsive grid */
    @media (max-width: 1200px) {
        .masonry-grid { column-count: 2; }
    }
    
    @media (max-width: 768px) {
        .masonry-grid { column-count: 1; }
    }
    
    /* Clean sidebar */
    .sidebar .sidebar-content {
        background-color: #f9f9f9;
    }
    
    /* Form styling */
    .stTextInput input, .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Date display */
    .date-text {
        font-size: 12px;
        color: #80868b;
        margin-top: 8px;
    }
    
    /* For the color themes */
    .theme-default { background-color: white; }
    .theme-light { background-color: #f9f9f9; }
    .theme-dark { background-color: #202124; color: #e8eaed; }
    .theme-colorful { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    /* Loading animation */
    .stSpinner > div {
        border-color: #4285f4 #4285f4 transparent !important;
    }
    
    /* Layout toggle styling */
    .layout-toggle {
        background-color: #f5f5f5;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 15px;
        border: 1px solid #e0e0e0;
    }
    
    /* Pinned note special styling */
    .pinned-note {
        position: relative;
    }
    
    .pinned-note::after {
        content: '📌';
        position: absolute;
        top: -10px;
        right: 10px;
        font-size: 20px;
        transform: rotate(30deg);
    }
</style>
""", unsafe_allow_html=True)

# Set the backend URL
backend_url = "http://localhost:5000/api"

# Initialize session state variables if they don't exist
if 'show_new_form' not in st.session_state:
    st.session_state.show_new_form = False
if 'view' not in st.session_state:
    st.session_state.view = "home"
if 'entries_cache' not in st.session_state:
    st.session_state.entries_cache = None
if 'archived_entries_cache' not in st.session_state:
    st.session_state.archived_entries_cache = None
if 'last_fetch_time' not in st.session_state:
    st.session_state.last_fetch_time = 0
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'available_tags' not in st.session_state:
    st.session_state.available_tags = ["Personal", "Work", "Ideas", "Important", "To-Do"]
if 'show_pinned_only' not in st.session_state:
    st.session_state.show_pinned_only = False
if 'loading' not in st.session_state:
    st.session_state.loading = False
if 'layout' not in st.session_state:
    st.session_state.layout = "grid"  # 'grid' or 'list'
if 'theme' not in st.session_state:
    st.session_state.theme = "default"  # default, light, dark, colorful
if 'selected_tag' not in st.session_state:
    st.session_state.selected_tag = "All Tags"  # Default to showing all tags
if 'selected_note_id' not in st.session_state:
    st.session_state.selected_note_id = None  # For detailed view
if 'editing_note' not in st.session_state:
    st.session_state.editing_note = None  # For storing the note being edited

# Function to check if the backend server is reachable
def is_server_reachable(url):
    try:
        # Check the health endpoint
        health_url = f"{url.rstrip('/')}/health"
        response = requests.get(health_url, timeout=3)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend server. Please check if it's running.")
        return False
    except requests.exceptions.Timeout:
        st.error("Connection to backend server timed out.")
        return False
    except requests.exceptions.RequestException as e:
        st.error(f"Backend server error: {e}")
        return False

# Function to navigate to a view
def navigate_to(view):
    st.session_state.view = view
    # Clear any cached entries to force a refresh
    st.session_state.entries_cache = None
    st.session_state.archived_entries_cache = None
    # Clear selected note when changing views
    st.session_state.selected_note_id = None

# Custom title with logo
st.markdown("<h1 style='text-align: center; margin-bottom: 20px; color: #4285f4;'>✨ Personal Diary ✨</h1>", unsafe_allow_html=True)

# Sidebar with enhanced navigation and options
with st.sidebar:
    st.markdown("<h3 style='color: #4285f4;'>📝 Navigation</h3>", unsafe_allow_html=True)
    
    # Navigation buttons with Google Keep style - rearranged order
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Home", use_container_width=True, key="home_btn"):
            navigate_to("home")
    with col2:
        if st.button("📒 All Entries", use_container_width=True, key="entries_btn"):
            navigate_to("entries")
            # Reset filters
            st.session_state.search_query = ""
            st.session_state.show_pinned_only = False
            st.session_state.selected_tag = "All Tags"
    
    # Add Archive button at the bottom of navigation
    if st.button("🗂️ Archive", use_container_width=True, key="archive_btn"):
        navigate_to("archive")
        # Force a refresh of archived entries
        st.session_state.archived_entries_cache = None
    
    st.divider()
    
    # Search functionality with Google Keep style
    st.markdown("<h3 style='color: #4285f4;'>🔍 Search</h3>", unsafe_allow_html=True)
    search_query = st.text_input("", value=st.session_state.search_query, 
                               placeholder="Search in notes...",
                               key="search_input")
    if search_query != st.session_state.search_query:
        st.session_state.search_query = search_query
        st.session_state.entries_cache = None  # Clear cache to refresh results
    
    st.divider()
    
    # Filter options with Google Keep style
    st.markdown("<h3 style='color: #4285f4;'>⚙️ Options</h3>", unsafe_allow_html=True)
    
    # Enhanced layout toggle with visual icons
    st.markdown("<div class='layout-toggle'>", unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom:5px;'><strong>Layout Style:</strong></p>", unsafe_allow_html=True)
    layout_options = {"🔲 Grid View": "grid", "📃 List View": "list"}
    selected_layout = st.radio("", options=list(layout_options.keys()), 
                               horizontal=True, 
                               label_visibility="collapsed")
    st.session_state.layout = layout_options[selected_layout]
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Make the pin checkbox more prominent
    st.markdown("<div style='padding: 10px; background-color: #fff8e1; border-radius: 5px; margin-bottom: 10px;'>", unsafe_allow_html=True)
    show_pinned = st.checkbox("📌 Show pinned notes only", value=st.session_state.show_pinned_only)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if show_pinned != st.session_state.show_pinned_only:
        st.session_state.show_pinned_only = show_pinned
        st.session_state.entries_cache = None  # Clear cache to refresh results
    
    # Tag filter with colored badges
    st.markdown("<h3 style='color: #4285f4;'>🏷️ Filter by Tag</h3>", unsafe_allow_html=True)
    
    # Show "All Tags" option
    selected_tag = st.session_state.selected_tag  # Initialize from session state
    
    if st.button("📑 All Tags", use_container_width=True, key="tag_all"):
        selected_tag = "All Tags"
        st.session_state.selected_tag = "All Tags"
    
    # Add buttons for each tag with appropriate colors
    for tag in st.session_state.available_tags:
        if st.button(f"🏷️ {tag}", use_container_width=True, key=f"tag_{tag}"):
            selected_tag = tag
            st.session_state.selected_tag = tag
    
    if selected_tag is None:
        selected_tag = "All Tags"
    
    # Color theme selector
    st.markdown("<h3 style='color: #4285f4;'>🎨 Theme</h3>", unsafe_allow_html=True)
    theme_options = {
        "Default": "default",
        "Light": "light", 
        "Dark": "dark", 
        "Colorful": "colorful"
    }
    selected_theme = st.selectbox("Select color theme", options=list(theme_options.keys()))
    st.session_state.theme = theme_options[selected_theme]

# Optimized fetch function to improve performance
@st.cache_data(ttl=5)  # Reduced TTL to 5 seconds for more frequent updates
def fetch_entries(endpoint):
    try:
        response = requests.get(f"{backend_url}/{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json().get('entries', [])
        return []
    except:
        return []

# Background fetch function for better UX
def background_fetch(endpoint, state_var):
    entries = fetch_entries(endpoint)
    if state_var == 'entries_cache':
        st.session_state.entries_cache = entries
    else:
        st.session_state.archived_entries_cache = entries
    st.session_state.loading = False
    # Don't force a rerun here - let the view handle it

# Helper function to apply search and filter
def filter_entries(entries):
    if not entries:
        return []
        
    filtered = entries
    
    # Apply search filter
    if st.session_state.search_query:
        query = st.session_state.search_query.lower()
        filtered = [e for e in filtered if (
            query in e.get("title", "").lower() or 
            query in e.get("content", "").lower() or
            any(tag and query in tag.lower() for tag in e.get("tags", []))
        )]
    
    # Apply tag filter
    if selected_tag != "All Tags":
        # Make sure we handle tags properly even if entry is missing tags
        filtered = [e for e in filtered if (
            selected_tag in e.get("tags", []) if isinstance(e.get("tags", []), list) 
            else selected_tag in (e.get("tags", "").split(",") if e.get("tags") else [])
        )]
    
    # Apply pinned filter - this is kept but actual filtering will be done after sorting
    pinned_filter = st.session_state.show_pinned_only
    
    # First separate pinned and unpinned entries
    pinned = [e for e in filtered if e.get("pinned", False)]
    not_pinned = [e for e in filtered if not e.get("pinned", False)]
    
    # Sort both lists by date (newest first) if date is available
    try:
        # Try both date_created and created_at fields since both are used
        pinned = sorted(pinned, key=lambda x: x.get("date_created", x.get("created_at", "")), reverse=True)
        not_pinned = sorted(not_pinned, key=lambda x: x.get("date_created", x.get("created_at", "")), reverse=True)
    except:
        # If sorting fails, leave as is
        pass
    
    # Apply pinned filter here, after sorting
    if pinned_filter:
        return pinned
    else:
        return pinned + not_pinned

# Function to get tag colors and styles
def get_tag_html(tag):
    return f'<span class="tag tag-{tag}">{tag}</span>'

# Render a card UI similar to Google Keep
def render_entry_card(entry, is_archived=False):
    title = entry.get('title', 'Untitled')
    content = entry.get('content', '')
    tags = entry.get('tags', [])
    pin_status = entry.get('pinned', False)
    entry_id = entry.get('id', 0)
    
    # Enhanced card styling for pinned notes
    card_border = 'border: 1px solid #f4b400;' if pin_status else 'border: 1px solid #e0e0e0;'
    
    # Card HTML with styling based on first tag and pin status
    pin_html = '📌' if pin_status else ''
    
    # Generate tag HTML
    tags_html = '<div class="tag-container">'
    for tag in tags:
        if tag:  # Only add non-empty tags
            tags_html += get_tag_html(tag) + " "
    tags_html += '</div>'
    
    # Format date if it exists - handle both date_created and created_at fields
    date_html = ""
    date_field = entry.get("date_created", entry.get("created_at", ""))
    if date_field:
        try:
            # Try direct format first for standard format
            created_date = datetime.strptime(date_field, '%Y-%m-%d %H:%M:%S')
            date_text = created_date.strftime('%b %d, %Y at %H:%M')
            date_html = f'<div class="date-text">{date_text}</div>'
        except:
            try:
                # Try ISO format if standard format fails
                created_date = datetime.fromisoformat(date_field)
                date_text = created_date.strftime('%b %d, %Y at %H:%M')
                date_html = f'<div class="date-text">{date_text}</div>'
            except:
                # If all parsing fails, just use raw text
                date_html = f'<div class="date-text">{date_field}</div>'
    
    # Create card HTML with improved styling for pinned notes
    card_html = f'''
    <div class="diary-card theme-{st.session_state.theme}" style="{card_border} {'' if not pin_status else 'box-shadow: 0 2px 6px rgba(244,180,0,0.3);'}" 
         onclick="parent.postMessage({{type: 'streamlit:set_state', state: {{ selected_note_id: {entry_id} }} }}, '*')">
        <div class="card-title">
            {title} <span class="pin-icon">{pin_html}</span>
        </div>
        <div class="card-content">{content}</div>
        {tags_html}
        {date_html}
    </div>
    '''
    
    # Render the HTML card
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Action buttons
    cols = st.columns(5 if not is_archived else 4)  # Added an extra column for the Edit button
    
    # Edit button (new)
    if cols[0].button("✏️ Edit", key=f"edit_{entry_id}"):
        st.session_state.editing_note = entry
        st.rerun()
    
    # Delete button
    if cols[1].button("🗑️ Delete", key=f"delete_{entry_id}"):
        try:
            delete_response = requests.delete(
                f"{backend_url}/entries/{entry_id}",
                timeout=5
            )
            if delete_response.status_code == 200:
                st.success(f"Entry deleted successfully!")
                # Clear the cache to force refresh
                fetch_entries.clear()
                if is_archived:
                    st.session_state.archived_entries_cache = None
                else:
                    st.session_state.entries_cache = None
                time.sleep(0.5)  # Brief delay
                st.rerun()
            else:
                st.error(f"Failed to delete entry.")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    
    if not is_archived:
        # Archive button
        if cols[2].button("📂 Archive", key=f"archive_{entry_id}"):
            try:
                archive_response = requests.post(
                    f"{backend_url}/archive_entry/{entry_id}",
                    timeout=5
                )
                if archive_response.status_code == 200:
                    st.success(f"Entry archived successfully!")
                    # Clear the cache to force refresh
                    fetch_entries.clear()
                    st.session_state.entries_cache = None
                    time.sleep(0.5)  # Brief delay
                    st.rerun()
                else:
                    st.error(f"Failed to archive entry.")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
        
        # Pin/Unpin button
        pin_text = "📌 Unpin" if pin_status else "📌 Pin"
        if cols[3].button(pin_text, key=f"pin_{entry_id}"):
            try:
                pin_response = requests.put(
                    f"{backend_url}/entries/{entry_id}/pin", 
                    json={"pinned": not pin_status},
                    timeout=5
                )
                if pin_response.status_code == 200:
                    st.success(f"Entry {'unpinned' if pin_status else 'pinned'} successfully!")
                    # Clear the cache to force refresh
                    fetch_entries.clear()
                    st.session_state.entries_cache = None
                    time.sleep(0.5)  # Brief delay
                    st.rerun()
                else:
                    st.error(f"Failed to {'unpin' if pin_status else 'pin'} entry.")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
    else:
        # Unarchive button - now using the dedicated endpoint
        if cols[2].button(f"📝 Unarchive", key=f"unarchive_{entry_id}"):
            try:
                # Use the direct unarchive endpoint we added to the backend
                unarchive_response = requests.post(
                    f"{backend_url}/unarchive_entry/{entry_id}",
                    timeout=5
                )
                
                if unarchive_response.status_code == 200:
                    st.success(f"Entry unarchived successfully!")
                    
                    # Clear both caches to force refresh
                    fetch_entries.clear()
                    st.session_state.entries_cache = None
                    st.session_state.archived_entries_cache = None
                    
                    # Navigate back to home view
                    st.session_state.view = "home"
                    time.sleep(0.5)  # Brief delay
                    st.rerun()
                else:
                    st.error(f"Failed to unarchive entry. Status: {unarchive_response.status_code}")
                    st.error("Please try again later.")
            except requests.exceptions.RequestException as e:
                st.error(f"Request error: {e}")
    
    # Send button (always the last column)
    send_col_idx = 4 if not is_archived else 3
    if cols[send_col_idx].button(f"📧 Send", key=f"send_{entry_id}"):
        try:
            send_response = requests.post(
                f"{backend_url}/send_entry/{entry_id}",
                timeout=5
            )
            if send_response.status_code == 200:
                st.success(f"Entry sent successfully!")
            else:
                st.error(f"Failed to send entry.")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

# Display the new entry form
def show_new_entry_form():
    st.markdown("<h2 style='color: #4285f4;'>✨ New Note</h2>", unsafe_allow_html=True)
    with st.form(key="new_entry_form", clear_on_submit=True):
        title = st.text_input("Title", placeholder="Title")
        content = st.text_area("Content", placeholder="What's on your mind?", height=150)
        
        # Add tags and color options
        col1, col2 = st.columns(2)
        with col1:
            tags = st.multiselect("Tags", options=st.session_state.available_tags)
        with col2:
            is_pinned = st.checkbox("📌 Pin to top")
        
        col1, col2 = st.columns(2)
        with col1:
            cancel_btn = st.form_submit_button("Cancel", use_container_width=True)
        with col2:
            submit_button = st.form_submit_button("Save", use_container_width=True)
        
        if submit_button:
            if title and content:
                if is_server_reachable(backend_url):
                    try:
                        # Add tags and pinned status to the request
                        response = requests.post(
                            f"{backend_url}/entries", 
                            json={
                                "title": title, 
                                "content": content,
                                "tags": tags,
                                "pinned": is_pinned,
                                "created_at": datetime.now().isoformat()
                            },
                            timeout=5
                        )
                        if response.status_code == 201:
                            st.success("Note added successfully!")
                            st.session_state.show_new_form = False
                            # Clear the cache to force refresh and fetch the latest entries
                            fetch_entries.clear()
                            st.session_state.entries_cache = None
                            st.session_state.view = "entries"  # Switch to entries view
                            time.sleep(0.5)  # Brief delay to ensure backend has processed
                            st.rerun()
                        else:
                            st.error("Failed to add note.")
                    except requests.exceptions.RequestException as e:
                        st.error(f"An error occurred: {e}")
                else:
                    st.error("Backend server is not reachable.")
            else:
                st.warning("Please enter both title and content.")
        
        if cancel_btn:
            st.session_state.show_new_form = False
            st.rerun()

# Add a new function to display the edit form
def show_edit_form(entry):
    st.markdown("<h2 style='color: #4285f4;'>✏️ Edit Note</h2>", unsafe_allow_html=True)
    
    entry_id = entry.get('id', 0)
    current_title = entry.get('title', '')
    current_content = entry.get('content', '')
    current_tags = entry.get('tags', []) if isinstance(entry.get('tags', []), list) else []
    current_pinned = entry.get('pinned', False)
    
    with st.form(key=f"edit_form_{entry_id}", clear_on_submit=True):
        title = st.text_input("Title", value=current_title)
        content = st.text_area("Content", value=current_content, height=150)
        
        # Add tags and color options
        col1, col2 = st.columns(2)
        with col1:
            tags = st.multiselect("Tags", options=st.session_state.available_tags, default=current_tags)
        with col2:
            is_pinned = st.checkbox("📌 Pin to top", value=current_pinned)
        
        col1, col2 = st.columns(2)
        with col1:
            cancel_btn = st.form_submit_button("Cancel", use_container_width=True)
        with col2:
            submit_button = st.form_submit_button("Update", use_container_width=True)
        
        if submit_button:
            if title and content:
                if is_server_reachable(backend_url):
                    try:
                        # Update the entry
                        response = requests.put(
                            f"{backend_url}/entries/{entry_id}", 
                            json={
                                "title": title, 
                                "content": content,
                                "tags": tags,
                                "pinned": is_pinned
                            },
                            timeout=5
                        )
                        if response.status_code == 200:
                            st.success("Note updated successfully!")
                            # Clear the editing state
                            st.session_state.editing_note = None
                            # Clear the cache to force refresh
                            fetch_entries.clear()
                            st.session_state.entries_cache = None
                            st.session_state.archived_entries_cache = None
                            time.sleep(0.5)  # Brief delay
                            st.rerun()
                        else:
                            st.error("Failed to update note.")
                    except requests.exceptions.RequestException as e:
                        st.error(f"An error occurred: {e}")
                else:
                    st.error("Backend server is not reachable.")
            else:
                st.warning("Please enter both title and content.")
        
        if cancel_btn:
            st.session_state.editing_note = None
            st.rerun()

# Create a new function to display detailed view of a note
def show_note_detail(entry, is_archived=False):
    title = entry.get('title', 'Untitled')
    content = entry.get('content', '')
    tags = entry.get('tags', [])
    pin_status = entry.get('pinned', False)
    entry_id = entry.get('id', 0)
    
    # Back button
    st.markdown("""
        <button class="back-button" onclick="parent.postMessage({type: 'streamlit:set_state', state: { selected_note_id: null } }, '*')">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 11H7.83L13.42 5.41L12 4L4 12L12 20L13.41 18.59L7.83 13H20V11Z" fill="#4285f4"/>
            </svg>
            Back to all notes
        </button>
    """, unsafe_allow_html=True)
    
    # Detailed view container
    st.markdown('<div class="detail-view">', unsafe_allow_html=True)
    
    # Title with pin status
    pin_icon = '📌' if pin_status else ''
    st.markdown(f'<div class="detail-title">{title} {pin_icon}</div>', unsafe_allow_html=True)
    
    # Content
    st.markdown(f'<div class="detail-content">{content}</div>', unsafe_allow_html=True)
    
    # Tags
    if tags:
        st.markdown('<div class="tag-container">', unsafe_allow_html=True)
        for tag in tags:
            if tag:
                st.markdown(get_tag_html(tag), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Date and metadata
    date_field = entry.get("date_created", entry.get("created_at", ""))
    if date_field:
        try:
            created_date = datetime.strptime(date_field, '%Y-%m-%d %H:%M:%S')
            date_text = created_date.strftime('%b %d, %Y at %H:%M')
        except:
            try:
                created_date = datetime.fromisoformat(date_field)
                date_text = created_date.strftime('%b %d, %Y at %H:%M')
            except:
                date_text = date_field
        st.markdown(f'<div class="detail-meta">Created: {date_text}</div>', unsafe_allow_html=True)
    
    # Close detail container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    st.markdown('<div class="detail-actions">', unsafe_allow_html=True)
    
    # Use 5 columns now to add Edit button
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Edit button (new)
    with col1:
        if st.button("✏️ Edit", key=f"detail_edit_{entry_id}", use_container_width=True):
            st.session_state.editing_note = entry
            st.session_state.selected_note_id = None  # Clear selected note to go back to list view
            st.rerun()
    
    # Delete button
    with col2:
        if st.button("🗑️ Delete", key=f"detail_delete_{entry_id}", use_container_width=True):
            try:
                delete_response = requests.delete(
                    f"{backend_url}/entries/{entry_id}",
                    timeout=5
                )
                if delete_response.status_code == 200:
                    st.success(f"Entry deleted successfully!")
                    # Clear the cache to force refresh
                    fetch_entries.clear()
                    if is_archived:
                        st.session_state.archived_entries_cache = None
                    else:
                        st.session_state.entries_cache = None
                    st.session_state.selected_note_id = None  # Clear selected note
                    time.sleep(0.5)  # Brief delay
                    st.rerun()
                else:
                    st.error(f"Failed to delete entry.")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
    
    if not is_archived:
        # Archive button
        with col3:
            if st.button("📂 Archive", key=f"detail_archive_{entry_id}", use_container_width=True):
                try:
                    archive_response = requests.post(
                        f"{backend_url}/archive_entry/{entry_id}",
                        timeout=5
                    )
                    if archive_response.status_code == 200:
                        st.success(f"Entry archived successfully!")
                        # Clear the cache to force refresh
                        fetch_entries.clear()
                        st.session_state.entries_cache = None
                        st.session_state.selected_note_id = None  # Clear selected note
                        time.sleep(0.5)  # Brief delay
                        st.rerun()
                    else:
                        st.error(f"Failed to archive entry.")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")
        
        # Pin/Unpin button
        with col4:
            pin_text = "📌 Unpin" if pin_status else "📌 Pin"
            if st.button(pin_text, key=f"detail_pin_{entry_id}", use_container_width=True):
                try:
                    pin_response = requests.put(
                        f"{backend_url}/entries/{entry_id}/pin", 
                        json={"pinned": not pin_status},
                        timeout=5
                    )
                    if pin_response.status_code == 200:
                        st.success(f"Entry {'unpinned' if pin_status else 'pinned'} successfully!")
                        # Clear the cache to force refresh
                        fetch_entries.clear()
                        st.session_state.entries_cache = None
                        time.sleep(0.5)  # Brief delay
                        st.rerun()
                    else:
                        st.error(f"Failed to {'unpin' if pin_status else 'pin'} entry.")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")
        
        # Send button
        with col5:
            if st.button(f"📧 Send", key=f"detail_send_{entry_id}", use_container_width=True):
                try:
                    send_response = requests.post(
                        f"{backend_url}/send_entry/{entry_id}",
                        timeout=5
                    )
                    if send_response.status_code == 200:
                        st.success(f"Entry sent successfully!")
                    else:
                        st.error(f"Failed to send entry.")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")
    else:
        # Unarchive button
        with col3:
            if st.button(f"📝 Unarchive", key=f"detail_unarchive_{entry_id}", use_container_width=True):
                try:
                    unarchive_response = requests.post(
                        f"{backend_url}/unarchive_entry/{entry_id}",
                        timeout=5
                    )
                    
                    if unarchive_response.status_code == 200:
                        st.success(f"Entry unarchived successfully!")
                        
                        # Clear both caches to force refresh
                        fetch_entries.clear()
                        st.session_state.entries_cache = None
                        st.session_state.archived_entries_cache = None
                        st.session_state.selected_note_id = None  # Clear selected note
                        
                        # Navigate back to home view
                        st.session_state.view = "home"
                        time.sleep(0.5)  # Brief delay
                        st.rerun()
                    else:
                        st.error(f"Failed to unarchive entry.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Request error: {e}")
                    
        # Send button
        with col4:
            if st.button(f"📧 Send", key=f"detail_send_{entry_id}", use_container_width=True):
                try:
                    send_response = requests.post(
                        f"{backend_url}/send_entry/{entry_id}",
                        timeout=5
                    )
                    if send_response.status_code == 200:
                        st.success(f"Entry sent successfully!")
                    else:
                        st.error(f"Failed to send entry.")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Home view modified to handle selected note view and edit form
if st.session_state.view == "home":
    # Check if a note is being edited
    if st.session_state.editing_note is not None:
        show_edit_form(st.session_state.editing_note)
    else:
        # Get selected note if any
        selected_note_id = st.session_state.selected_note_id
        
        # Check server and fetch entries
        if is_server_reachable(backend_url):
            # Show spinner while loading
            if st.session_state.loading:
                with st.spinner("Loading notes..."):
                    time.sleep(0.1)  # Small delay to show spinner
            else:
                # Start background fetch if needed
                current_time = time.time()
                if (st.session_state.entries_cache is None or 
                    (current_time - st.session_state.last_fetch_time) > 2):
                    
                    st.session_state.loading = True
                    threading.Thread(
                        target=background_fetch, 
                        args=("entries", "entries_cache")
                    ).start()
                    st.session_state.last_fetch_time = current_time
            
            # Use cached entries if available
            entries = st.session_state.entries_cache or []
            
            # If a note is selected, show its detailed view
            if selected_note_id is not None:
                # Find the selected note
                selected_entry = next((e for e in entries if e.get('id') == selected_note_id), None)
                if selected_entry:
                    show_note_detail(selected_entry)
                else:
                    st.error("Selected note not found.")
                    st.session_state.selected_note_id = None
                    st.rerun()
            else:
                # Show normal view with title
                st.markdown("<h2 style='color: #4285f4;'>📝 Your Notes</h2>", unsafe_allow_html=True)
                
                # Button to show the form
                col1, col2 = st.columns([1, 5])
                with col1:
                    if st.button("+ New Note", use_container_width=True):
                        st.session_state.show_new_form = True
                        st.rerun()  # Rerun to show the form immediately
                with col2:
                    if st.session_state.search_query:
                        st.info(f"Showing results for: '{st.session_state.search_query}'")
                    elif st.session_state.show_pinned_only:
                        st.info("Showing pinned notes only")
                    elif selected_tag != "All Tags":
                        st.info(f"Showing notes with tag: '{selected_tag}'")
                
                # Display form if show_new_form is True
                if st.session_state.show_new_form:
                    show_new_entry_form()
                
                # Apply filters and search
                filtered_entries = filter_entries(entries)
                
                if filtered_entries:
                    # Begin layout based on view type
                    if st.session_state.layout == "grid":
                        st.markdown('<div class="masonry-grid">', unsafe_allow_html=True)
                    
                    # Display entries
                    for entry in filtered_entries:
                        # Prepare container class based on layout and pin status
                        is_pinned = entry.get("pinned", False)
                        pin_class = "pinned-note" if is_pinned else ""
                        
                        if st.session_state.layout == "grid":
                            # Grid view - show in masonry layout
                            st.markdown(f'<div class="masonry-item {pin_class}">', unsafe_allow_html=True)
                            render_entry_card(entry)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            # List view - show in list layout
                            st.markdown(f'<div class="list-item {pin_class}">', unsafe_allow_html=True)
                            render_entry_card(entry)
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Close container if needed
                    if st.session_state.layout == "grid":
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    if st.session_state.search_query:
                        st.info(f"No notes found matching '{st.session_state.search_query}'")
                    elif st.session_state.show_pinned_only:
                        st.info("No pinned notes found. Pin some notes to see them here.")
                    elif selected_tag != "All Tags":
                        st.info(f"No notes found with tag '{selected_tag}'")
                    else:
                        st.info("No notes found. Create a new note to get started!")
        else:
            st.error("Backend server is not reachable.")

# Archive view modified to handle editing
elif st.session_state.view == "archive":
    # Check if a note is being edited
    if st.session_state.editing_note is not None:
        show_edit_form(st.session_state.editing_note)
    else:
        # Get selected note if any
        selected_note_id = st.session_state.selected_note_id
        
        if is_server_reachable(backend_url):
            # Force refresh the archive cache
            if st.session_state.archived_entries_cache is None:
                with st.spinner("Loading archived notes..."):
                    # Direct fetch without caching to ensure we get the latest data
                    try:
                        response = requests.get(f"{backend_url}/archived_entries", timeout=5)
                        if response.status_code == 200:
                            st.session_state.archived_entries_cache = response.json().get('entries', [])
                        else:
                            st.session_state.archived_entries_cache = []
                    except:
                        st.session_state.archived_entries_cache = []
                        st.error("Failed to fetch archived entries.")
            
            # Use cached entries
            entries = st.session_state.archived_entries_cache or []
            
            # If a note is selected, show its detailed view
            if selected_note_id is not None:
                # Find the selected note
                selected_entry = next((e for e in entries if e.get('id') == selected_note_id), None)
                if selected_entry:
                    show_note_detail(selected_entry, is_archived=True)
                else:
                    st.error("Selected note not found.")
                    st.session_state.selected_note_id = None
                    st.rerun()
            else:
                # Show normal view with title
                st.markdown("<h2 style='color: #4285f4;'>🗃️ Archived Notes</h2>", unsafe_allow_html=True)
                
                # Button to show the form
                col1, col2 = st.columns([1, 5])
                with col1:
                    if st.button("+ New Note", use_container_width=True, key="new_note_archive"):
                        st.session_state.show_new_form = True
                        st.rerun()  # Rerun to show the form immediately
                with col2:
                    if st.session_state.search_query:
                        st.info(f"Showing results for: '{st.session_state.search_query}'")
                    elif st.session_state.show_pinned_only:
                        st.info("Showing pinned notes only")
                
                # Display form if show_new_form is True
                if st.session_state.show_new_form:
                    show_new_entry_form()
                
                # Apply search filter to archived entries
                filtered_entries = filter_entries(entries)
                
                if filtered_entries:
                    # Begin layout based on view type
                    if st.session_state.layout == "grid":
                        st.markdown('<div class="masonry-grid">', unsafe_allow_html=True)
                    
                    # Display entries
                    for entry in filtered_entries:
                        # Prepare container class based on layout and pin status
                        is_pinned = entry.get("pinned", False)
                        pin_class = "pinned-note" if is_pinned else ""
                        
                        if st.session_state.layout == "grid":
                            # Grid view - show in masonry layout
                            st.markdown(f'<div class="masonry-item {pin_class}">', unsafe_allow_html=True)
                            render_entry_card(entry, is_archived=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            # List view - show in list layout
                            st.markdown(f'<div class="list-item {pin_class}">', unsafe_allow_html=True)
                            render_entry_card(entry, is_archived=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Close container if needed
                    if st.session_state.layout == "grid":
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    if st.session_state.search_query:
                        st.info(f"No archived notes matching '{st.session_state.search_query}'")
                    else:
                        st.info("No archived notes found.")
        else:
            st.error("Backend server is not reachable.")

# All Entries view modified to handle editing
elif st.session_state.view == "entries":
    # Check if a note is being edited
    if st.session_state.editing_note is not None:
        show_edit_form(st.session_state.editing_note)
    else:
        # Get selected note if any
        selected_note_id = st.session_state.selected_note_id
        
        if is_server_reachable(backend_url):
            # Direct fetch all entries
            with st.spinner("Loading all entries..."):
                # Direct fetch without caching to ensure we get the latest data
                try:
                    response = requests.get(f"{backend_url}/entries", timeout=5)
                    if response.status_code == 200:
                        all_entries = response.json().get('entries', [])
                        
                        # First separate pinned and unpinned entries
                        pinned_entries = [e for e in all_entries if e.get("pinned", False)]
                        unpinned_entries = [e for e in all_entries if not e.get("pinned", False)]
                        
                        # Sort both lists by date (newest first)
                        try:
                            pinned_entries = sorted(pinned_entries, key=lambda x: x.get("date_created", x.get("created_at", "")), reverse=True)
                            unpinned_entries = sorted(unpinned_entries, key=lambda x: x.get("date_created", x.get("created_at", "")), reverse=True)
                        except:
                            pass
                        
                        # Combine with pinned on top
                        entries = pinned_entries + unpinned_entries
                        
                        # Apply "Show pinned notes only" filter if selected
                        if st.session_state.show_pinned_only:
                            entries = pinned_entries
                    else:
                        entries = []
                except:
                    entries = []
                    st.error("Failed to fetch entries.")
            
            # If a note is selected, show its detailed view
            if selected_note_id is not None:
                # Find the selected note
                selected_entry = next((e for e in entries if e.get('id') == selected_note_id), None)
                if selected_entry:
                    show_note_detail(selected_entry)
                else:
                    st.error("Selected note not found.")
                    st.session_state.selected_note_id = None
                    st.rerun()
            else:
                # Show normal view with title
                st.markdown("<h2 style='color: #4285f4;'>📒 All Entries</h2>", unsafe_allow_html=True)
                
                # Button to show the form
                col1, col2 = st.columns([1, 5])
                with col1:
                    if st.button("+ New Note", use_container_width=True, key="new_note_entries"):
                        st.session_state.show_new_form = True
                        st.rerun()  # Rerun to show the form immediately
                with col2:
                    if st.session_state.search_query:
                        st.info(f"Showing results for: '{st.session_state.search_query}'")
                    elif st.session_state.show_pinned_only:
                        st.info("Showing pinned notes only")
                
                # Display form if show_new_form is True
                if st.session_state.show_new_form:
                    show_new_entry_form()
                
                if entries:
                    # Begin layout based on view type
                    if st.session_state.layout == "grid":
                        st.markdown('<div class="masonry-grid">', unsafe_allow_html=True)
                    
                    # Display entries
                    for entry in entries:
                        # Prepare container class based on layout and pin status
                        is_pinned = entry.get("pinned", False)
                        pin_class = "pinned-note" if is_pinned else ""
                        
                        if st.session_state.layout == "grid":
                            # Grid view - show in masonry layout
                            st.markdown(f'<div class="masonry-item {pin_class}">', unsafe_allow_html=True)
                            render_entry_card(entry)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            # List view - show in list layout
                            st.markdown(f'<div class="list-item {pin_class}">', unsafe_allow_html=True)
                            render_entry_card(entry)
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Close container if needed
                    if st.session_state.layout == "grid":
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("No entries found. Create a new note to get started!")
        else:
            st.error("Backend server is not reachable.")
