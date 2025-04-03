import streamlit as st
import requests

# Flask API URL
API_URL = "http://localhost:5000/api/search"

# Custom Styling for Streamlit (Fixing CSS issues)
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(to right, #3a7bd5, #3a6073);
            color: white;
        }
        .result-card {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
st.title("🤖 AI-Powered Web Search Chatbot")
st.write("Ask me anything, and I’ll fetch answers from Google & ChatGPT!")

# User Input Section
query = st.text_input("🔎 Enter your question:")

if st.button("🚀 Search"):
    if not query.strip():
        st.warning("⚠️ Please enter a valid question!")
    else:
        with st.spinner("🔄 Thinking... Fetching relevant answers..."):
            try:
                response = requests.get(API_URL, params={"query": query}, timeout=10)
                st.write(f"ℹ️ **Debug Info**: API Response Code - {response.status_code}")  # Debugging

                # If API request fails, show error
                if response.status_code != 200:
                    st.error(f"❌ Error: Unable to fetch results. Server returned status code {response.status_code}")
                    st.json(response.json())  # Show raw response for debugging
                else:
                    data = response.json()
                    st.write("ℹ️ **Debug Info**: API Response Data -")  # Debugging
                    st.json(data)

                    # Display Google Search Results
                    st.subheader("🔍 Google Search Results")
                    if isinstance(data.get("results"), list) and len(data["results"]) > 0:
                        for item in data["results"]:
                            st.markdown(
                                f"""
                                <div class="result-card">
                                    <h4><a href="{item.get('link', '#')}" target="_blank">{item.get('title', 'No Title')}</a></h4>
                                    <p>{item.get('snippet', 'No description available.')}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    else:
                        st.warning("🚫 No search results found.")

                    # Display ChatGPT Response
                    st.subheader("🤖 ChatGPT's Take")
                    chat_response = data.get("chatgpt_response", "No response from ChatGPT.")
                    st.write(chat_response if chat_response else "🤷 No AI-generated response.")

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection Error: Unable to reach the API. \n\n Error details: {e}")
