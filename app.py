import streamlit as st
import requests
import time

# --- 1. SETTINGS ---
# BE CAREFUL: Ensure there are no spaces before or after your key
API_KEY = "PASTE_YOUR_SILICONFLOW_KEY_HERE"

# These must be exactly as written
GENERATE_URL = "https://api.siliconflow.cn/v1/video/text-to-video"
CHECK_STATUS_URL = "https://api.siliconflow.cn/v1/video/get-result"

st.set_page_config(page_title="TheDailyDesign.AI Video Studio")
st.title("🎬 AI Video Studio")

prompt = st.text_area("Describe your video:", placeholder="A cinematic 8k shot of...")

if st.button("Generate Video"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        # This model name must be exact
        payload = {
            "model": "deepseek-ai/Wan2.1-T2V-14B",
            "prompt": prompt
        }

        with st.spinner("Connecting to AI..."):
            try:
                response = requests.post(GENERATE_URL, json=payload, headers=headers)
                
                # --- DEBUG SECTION ---
                if response.status_code != 200:
                    st.error(f"Server Error Code: {response.status_code}")
                    st.write("The server said: ", response.text) 
                    st.stop() # Stops the app so we can read the error
                
                res_data = response.json()
                
                if "id" in res_data:
                    job_id = res_data["id"]
                    status_ui = st.empty()
                    
                    while True:
                        status_ui.info("⌛ Rendering... please wait 60 seconds.")
                        time.sleep(10)
                        
                        check = requests.get(f"{CHECK_STATUS_URL}?id={job_id}", headers=headers)
                        status_data = check.json()
                        
                        if status_data.get("status") == "SUCCEED":
                            st.video(status_data.get("video_url"))
                            break
                        elif status_data.get("status") == "FAILED":
                            st.error("Generation failed.")
                            break
                else:
                    st.error("Could not find Task ID in response.")

            except Exception as e:
                st.error(f"App Error: {e}")
