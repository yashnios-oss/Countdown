import streamlit as st
from duckduckgo_search import DDGS

st.set_page_config(page_title="OSINT Person Search", page_icon="🌐")

st.title("🌐 Live Internet Person Search")
st.caption("Enter details to fetch real-time information from across the web.")

# --- Input Section ---
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Full Name", placeholder="e.g., Sundar Pichai")
    with col2:
        age = st.text_input("Age (Optional)", placeholder="e.g., 51")
    with col3:
        country = st.text_input("Country", placeholder="e.g., USA")

search_button = st.button("🔍 Search Internet")

# --- Logic Section ---
if search_button:
    if not name:
        st.warning("Please at least enter a name to start the search.")
    else:
        # Construct a targeted search query
        query = f"{name} {age} {country}".strip()
        
        with st.spinner(f"Searching the web for '{query}'..."):
            try:
                with DDGS() as ddgs:
                    # Fetching the top 5 results from the web
                    results = [r for r in ddgs.text(query, max_results=5)]
                
                if results:
                    st.success(f"Found {len(results)} relevant links!")
                    
                    for i, result in enumerate(results):
                        with st.expander(f"{i+1}. {result['title']}"):
                            st.write(f"**Source:** {result['href']}")
                            st.write(f"**Snippet:** {result['body']}")
                            st.link_button("Visit Site", result['href'])
                else:
                    st.error("No public information found. Try adding more specific details.")
            
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.divider()
st.info("Note: This app fetches public data available on search engines. Results depend on the person's digital footprint.")
