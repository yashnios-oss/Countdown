import streamlit as st
import requests
import json

st.set_page_config(page_title="OSINT Person Search", page_icon="🌐")

st.title("🌐 Google-Powered Person Search")

# --- API Configuration ---
# You will enter your API Key here
SERPER_API_KEY =  "95cddad40fabf6213923685ee418c919620d10bf"

with st.sidebar:
    st.info("Using Serper (Google Search API) for better reliability.")

# --- Input Section ---
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Full Name")
with col2:
    age = st.text_input("Age")
with col3:
    country = st.text_input("Country")

if st.button("🔍 Search Internet"):
    if not name:
        st.warning("Please enter a name.")
    else:
        query = f"{name} {age} {country}".strip()
        
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }

        with st.spinner("Fetching live data from Google..."):
            response = requests.post("https://google.serper.dev/search", headers=headers, data=payload)
            
            if response.status_code == 200:
                results = response.json().get('organic', [])
                
                if results:
                    for result in results:
                        with st.container():
                            st.markdown(f"### [{result['title']}]({result['link']})")
                            st.write(result.get('snippet', 'No preview available.'))
                            st.caption(f"Source: {result['link']}")
                            st.divider()
                else:
                    st.error("No results found.")
            else:
                st.error(f"Search failed. Error code: {response.status_code}")
