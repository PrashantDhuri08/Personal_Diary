import streamlit as st
import requests
import time
import datetime
from datetime import datetime

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

# Function to check if the backend server is reachable
def is_server_reachable(url):
    try:
        # Check a specific health endpoint instead of the base URL
        # If your backend doesn't have a /health endpoint, use /entries as it's known to exist
        health_url = f"{url.rstrip('/')}/health" if '/health' in url else f"{url}/entries"
        response = requests.get(health_url, timeout=5)  # Add timeout to prevent hanging
        return True  # If no exception occurs, server is reachable
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

# Title of the app with improved styling
st.markdown("<h1 style='text-align: center;'>✨ Personal Diary ✨</h1>", unsafe_allow_html=True)

# Sidebar with enhanced navigation and options
with st.sidebar:
    st.title("Navigation")
    if st.button("📝 Home", use_container_width=True):
        navigate_to("home")
    if st.button("🗃️ Archive", use_container_width=True):
        navigate_to("archive")
    
    st.divider()
    
    # Search functionality
    st.subheader("🔍 Search Entries")
    search_query = st.text_input("Enter keywords", value=st.session_state.search_query)
    if search_query != st.session_state.search_query:
        st.session_state.search_query = search_query
        st.session_state.entries_cache = None  # Clear cache to refresh results
    
    st.divider()
    
    # Filter options
    st.subheader("⚙️ Display Options")
    show_pinned = st.checkbox("Show pinned entries only", value=st.session_state.show_pinned_only)
    if show_pinned != st.session_state.show_pinned_only:
        st.session_state.show_pinned_only = show_pinned
        st.session_state.entries_cache = None  # Clear cache to refresh results
    
    # Tag filter
    st.subheader("🏷️ Filter by Tag")
    selected_tag = st.selectbox("Select a tag", ["All Tags"] + st.session_state.available_tags)
    
    # Color theme selector
    st.subheader("🎨 Theme")
    theme = st.selectbox("Select color theme", ["Default", "Light", "Dark", "Colorful"])

# Cache fetch function to improve performance
@st.cache_data(ttl=10)
def fetch_entries(endpoint):
    try:
        response = requests.get(f"{backend_url}/{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json().get('entries', [])
        return []
    except:
        return []

# Helper function to apply search and filter
def filter_entries(entries):
    filtered = entries
    
    # Apply search filter
    if st.session_state.search_query:
        query = st.session_state.search_query.lower()
        filtered = [e for e in filtered if (
            query in e.get("title", "").lower() or 
            query in e.get("content", "").lower() or
            any(query in tag.lower() for tag in e.get("tags", []))
        )]
    
    # Apply tag filter
    if selected_tag != "All Tags":
        filtered = [e for e in filtered if selected_tag in e.get("tags", [])]
    
    # Apply pinned filter
    if st.session_state.show_pinned_only:
        filtered = [e for e in filtered if e.get("pinned", False)]
    
    # Sort with pinned on top
    pinned = [e for e in filtered if e.get("pinned", False)]
    not_pinned = [e for e in filtered if not e.get("pinned", False)]
    
    return pinned + not_pinned

# Function to generate a color based on tags
def get_entry_color(entry):
    colors = {
        "Personal": "#ffcccc",  # Light red
        "Work": "#cce5ff",      # Light blue
        "Ideas": "#ccffcc",     # Light green
        "Important": "#ffecb3",  # Light yellow/gold
        "To-Do": "#e6ccff"      # Light purple
    }
    
    # Default color
    default_color = "#ffffff"  # White
    
    # Get color based on first tag if tags exist
    if entry.get("tags") and len(entry.get("tags")) > 0:
        first_tag = entry["tags"][0]
        return colors.get(first_tag, default_color)
    
    return default_color

# Home view
if st.session_state.view == "home":
    st.header("Welcome to your Personal Diary")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("➕ NEW", type="primary", use_container_width=True):
            st.session_state.show_new_form = True
    with col2:
        if st.session_state.search_query:
            st.info(f"Showing results for: '{st.session_state.search_query}'")
    
    # Display form if show_new_form is True
    if st.session_state.show_new_form:
        st.subheader("Add a New Entry")
        with st.form(key="new_entry_form"):
            title = st.text_input("Title")
            content = st.text_area("Content")
            
            # Add tags and color options
            col1, col2 = st.columns(2)
            with col1:
                tags = st.multiselect("Tags", options=st.session_state.available_tags)
            with col2:
                is_pinned = st.checkbox("Pin to top")
            
            submit_button = st.form_submit_button("Save Entry")
            
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
                                }
                            )
                            if response.status_code == 201:
                                st.success("Entry added successfully!")
                                st.session_state.show_new_form = False
                                st.session_state.entries_cache = None  # Clear cache to refresh entries
                            else:
                                st.error("Failed to add entry.")
                        except requests.exceptions.RequestException as e:
                            st.error(f"An error occurred: {e}")
                    else:
                        st.error("Backend server is not reachable.")
                else:
                    st.warning("Please enter both title and content.")
    
    st.subheader("Your Entries")
    if is_server_reachable(backend_url):
        # Use cached entries if available and recent, otherwise fetch new ones
        current_time = time.time()
        if st.session_state.entries_cache is None or (current_time - st.session_state.last_fetch_time) > 2:
            with st.spinner("Loading entries..."):
                entries = fetch_entries("entries")
                st.session_state.entries_cache = entries
                st.session_state.last_fetch_time = current_time
        else:
            entries = st.session_state.entries_cache
        
        # Apply filters and search
        filtered_entries = filter_entries(entries)
            
        if filtered_entries:
            for entry in filtered_entries:
                # Get color based on tags
                entry_color = get_entry_color(entry)
                
                # Create an expander with styling based on color and pin status
                pin_icon = "📌 " if entry.get("pinned", False) else ""
                
                # Use an expander with custom styling
                with st.expander(f"{pin_icon}{entry['title']}"):
                    # Show entry content with styling
                    st.markdown(
                        f"""
                        <div style="background-color: black; padding: 20px; border-radius: 5px; margin-bottom: 15px; ">
                            {entry["content"]}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # Show tags if they exist
                    if entry.get("tags"):
                        st.markdown("**Tags:** " + ", ".join(entry["tags"]))
                    
                    # Show creation date if it exists
                    if entry.get("created_at"):
                        try:
                            created_date = datetime.fromisoformat(entry["created_at"])
                            st.text(f"Created: {created_date.strftime('%b %d, %Y at %H:%M')}")
                        except:
                            pass
                    
                    # Create a row of buttons using columns
                    col1, col2, col3, col4 = st.columns(4)
                    
                    # Delete button
                    if col1.button(f"🗑️ Delete", key=f"delete_{entry['id']}"):
                        try:
                            delete_response = requests.delete(f"{backend_url}/entries/{entry['id']}")
                            if delete_response.status_code == 200:
                                st.success(f"Entry '{entry['title']}' deleted successfully!")
                                # Update cache to remove the deleted entry
                                st.session_state.entries_cache = None
                            else:
                                st.error(f"Failed to delete entry '{entry['title']}'.")
                        except requests.exceptions.RequestException as e:
                            st.error(f"An error occurred: {e}")
                    
                    # Archive button
                    if col2.button(f"📂 Archive", key=f"archive_{entry['id']}"):
                        try:
                            archive_response = requests.post(f"{backend_url}/archive_entry/{entry['id']}")
                            if archive_response.status_code == 200:
                                st.success(f"Entry '{entry['title']}' archived successfully!")
                                # Update cache to remove the archived entry
                                st.session_state.entries_cache = None
                            else:
                                st.error(f"Failed to archive entry '{entry['title']}'.")
                        except requests.exceptions.RequestException as e:
                            st.error(f"An error occurred: {e}")
                    
                    # Pin/Unpin button
                    pin_status = entry.get("pinned", False)
                    pin_text = "📌 Unpin" if pin_status else "📌 Pin"
                    if col3.button(pin_text, key=f"pin_{entry['id']}"):
                        try:
                            pin_response = requests.put(
                                f"{backend_url}/entries/{entry['id']}/pin", 
                                json={"pinned": not pin_status}
                            )
                            if pin_response.status_code == 200:
                                st.success(f"Entry '{entry['title']}' {'unpinned' if pin_status else 'pinned'} successfully!")
                                st.session_state.entries_cache = None
                            else:
                                st.error(f"Failed to {'unpin' if pin_status else 'pin'} entry.")
                        except requests.exceptions.RequestException as e:
                            st.error(f"An error occurred: {e}")
                    
                    # Send button
                    if col4.button(f"📧 Send", key=f"send_{entry['id']}"):
                        try:
                            send_response = requests.post(f"{backend_url}/send_entry/{entry['id']}")
                            if send_response.status_code == 200:
                                st.success(f"Entry '{entry['title']}' sent successfully!")
                            else:
                                st.error(f"Failed to send entry '{entry['title']}'.")
                        except requests.exceptions.RequestException as e:
                            st.error(f"An error occurred: {e}")
        else:
            if st.session_state.search_query:
                st.info(f"No entries found matching '{st.session_state.search_query}'")
            elif st.session_state.show_pinned_only:
                st.info("No pinned entries found.")
            elif selected_tag != "All Tags":
                st.info(f"No entries found with tag '{selected_tag}'")
            else:
                st.info("No entries found. Create a new entry to get started!")
    else:
        st.error("Backend server is not reachable.")

# Archive view
elif st.session_state.view == "archive":
    st.header("Archived Entries")
    if is_server_reachable(backend_url):
        # Use cached archived entries if available and recent, otherwise fetch new ones
        current_time = time.time()
        if st.session_state.archived_entries_cache is None or (current_time - st.session_state.last_fetch_time) > 2:
            with st.spinner("Loading archived entries..."):
                entries = fetch_entries("archived_entries")
                st.session_state.archived_entries_cache = entries
                st.session_state.last_fetch_time = current_time
        else:
            entries = st.session_state.archived_entries_cache
        
        # Apply search filter to archived entries as well
        filtered_entries = filter_entries(entries)
        
        if filtered_entries:
            for entry in filtered_entries:
                # Get color based on tags
                entry_color = get_entry_color(entry)
                
                with st.expander(entry["title"]):
                    # Show entry content with styling
                    st.markdown(
                        f"""
                        <div style="background-color: {entry_color}; padding: 10px; border-radius: 5px;">
                            {entry["content"]}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # Show tags if they exist
                    if entry.get("tags"):
                        st.markdown("**Tags:** " + ", ".join(entry["tags"]))
                    
                    # Create a row of buttons using columns
                    col1, col2, col3 = st.columns(3)
                    
                    # Delete button in first column
                    if col1.button(f"🗑️ Delete", key=f"delete_arch_{entry['id']}"):
                        try:
                            delete_response = requests.delete(f"{backend_url}/entries/{entry['id']}")
                            if delete_response.status_code == 200:
                                st.success(f"Entry '{entry['title']}' deleted successfully!")
                                # Update cache to remove the deleted entry
                                st.session_state.archived_entries_cache = None
                            else:
                                st.error(f"Failed to delete entry '{entry['title']}'.")
                        except requests.exceptions.RequestException as e:
                            st.error(f"An error occurred: {e}")
                    
                    # Unarchive button - Try two different API approaches to improve success rate
                    if col2.button(f"📝 Unarchive", key=f"unarchive_{entry['id']}"):
                        try:
                            st.info(f"Attempting to unarchive entry '{entry['title']}'...")
                            
                            # First try the direct unarchive endpoint
                            unarchive_url = f"{backend_url}/unarchive_entry/{entry['id']}"
                            unarchive_response = requests.post(
                                unarchive_url,
                                timeout=10,
                                headers={'Content-Type': 'application/json'}
                            )
                            
                            # If that fails, try an alternative approach: update the entry's archived status
                            if unarchive_response.status_code != 200:
                                st.warning("First unarchive attempt failed, trying alternative approach...")
                                alt_url = f"{backend_url}/entries/{entry['id']}"
                                entry_data = dict(entry)
                                entry_data["archived"] = False
                                unarchive_response = requests.put(
                                    alt_url,
                                    json=entry_data,
                                    timeout=10,
                                    headers={'Content-Type': 'application/json'}
                                )
                            
                            if unarchive_response.status_code in [200, 201, 204]:
                                st.success(f"Entry '{entry['title']}' unarchived successfully!")
                                
                                # Clear both caches to force refresh
                                st.session_state.entries_cache = None
                                st.session_state.archived_entries_cache = None
                                
                                # Navigate back to home view
                                st.session_state.view = "home"
                                st.experimental_rerun()
                            else:
                                st.error(f"Failed to unarchive entry. Status: {unarchive_response.status_code}")
                                
                                # Create a manual unarchive option as fallback
                                st.warning("Automatic unarchive failed. Would you like to create a new entry with this content instead?")
                                if st.button("Create Copy in Home", key=f"copy_{entry['id']}"):
                                    # Copy the entry data to session state for recreation
                                    st.session_state.entry_to_recreate = {
                                        "title": entry["title"],
                                        "content": entry["content"],
                                        "tags": entry.get("tags", []),
                                        "pinned": entry.get("pinned", False)
                                    }
                                    st.session_state.view = "home"
                                    st.session_state.show_new_form = True
                                    st.experimental_rerun()
                                
                        except requests.exceptions.RequestException as e:
                            st.error(f"Request error: {e}")
                    
                    # Send button in third column
                    if col3.button(f"📧 Send", key=f"send_arch_{entry['id']}"):
                        try:
                            send_response = requests.post(f"{backend_url}/send_entry/{entry['id']}")
                            if send_response.status_code == 200:
                                st.success(f"Entry '{entry['title']}' sent successfully!")
                            else:
                                st.error(f"Failed to send entry '{entry['title']}'.")
                        except requests.exceptions.RequestException as e:
                            st.error(f"An error occurred: {e}")
        else:
            if st.session_state.search_query:
                st.info(f"No archived entries matching '{st.session_state.search_query}'")
            else:
                st.info("No archived entries found.")
    else:
        st.error("Backend server is not reachable.")
