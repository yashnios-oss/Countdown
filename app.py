import streamlit as st

# Set up the app title
st.title("👤 Person Detail Locator")

# Initialize a "database" in the session state so data persists 
# while the app is running
if 'person_db' not in st.session_state:
    st.session_state.person_db = {}

# --- Sidebar for Data Entry ---
st.sidebar.header("Add New Person")
with st.sidebar.form("entry_form"):
    name = st.text_input("Full Name").strip()
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    country = st.text_input("Country")
    
    submit_button = st.form_submit_button("Save Details")

if submit_button and name:
    # Save to our temporary dictionary
    st.session_state.person_db[name.lower()] = {
        "Name": name,
        "Age": age,
        "Country": country
    }
    st.sidebar.success(f"Added {name} to the list!")

# --- Main Area for Searching ---
st.subheader("Search for a Person")
search_query = st.text_input("Enter the name of the person you want to look up:")

if search_query:
    result = st.session_state.person_db.get(search_query.lower())
    
    if result:
        st.write("### Result Found:")
        col1, col2, col3 = st.columns(3)
        col1.metric("Name", result["Name"])
        col2.metric("Age", result["Age"])
        col3.metric("Country", result["Country"])
    else:
        st.error("No record found for that name. Did you add them in the sidebar yet?")

# --- Optional: View All Records ---
if st.checkbox("Show all saved records"):
    st.table(st.session_state.person_db.values())
