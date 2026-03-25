import streamlit as st
import requests
import time

# --- 1. CONFIGURATION ---
# PASTE YOUR ACTUAL KEY BETWEEN THE QUOTES BELOW
API_KEY = "sk-f*******************************************mnbm"

GENERATE_URL = "https://api.siliconflow.cn/v1/video/text-to-video"
CHECK_STATUS_URL = "https://api.siliconflow.cn/v1/video/get-result"

st.set_page_config(page_title="TheDailyDesign.AI | Video Studio", layout="centered")

# --- 2. USER INTERFACE ---
st.title("🎬 TheDailyDesign.AI Video Studio")
st.info("Creating cinematic AI videos for your brand.")

prompt = st.text_area("Describe your video:", 
                     placeholder="An ultra-realistic 8k portrait of a person in cinematic lighting...")

# --- 3. THE GENERATION PROCESS ---
if st.button("Generate Video"):
    if not prompt:
        st.warning("Please enter a prompt first!")
    elif "YOUR_SILICONFLOW" in API_KEY:
        st.error("Please replace the placeholder with your actual API Key.")
    else:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-ai/Wan2.1-T2V-14B", # Professional high-quality model
            "prompt": prompt
        }

        with st.spinner("🚀 Sending request to AI server..."):
            try:
                response = requests.post(GENERATE_URL, json=payload, headers=headers)
                res_data = response.json()
                
                if "id" in res_data:
                    job_id = res_data["id"]
                    
                    # --- 4. POLLING (WAITING FOR VIDEO) ---
                    status_placeholder = st.empty()
                    while True:
                        status_placeholder.info("⌛ AI is rendering your video... this usually takes 1-2 minutes.")
                        time.sleep(10) # Wait 10 seconds before checking
                        
                        check_req = requests.get(f"{CHECK_STATUS_URL}?id={job_id}", headers=headers)
                        status_data = check_req.json()
                        
                        if status_data.get("status") == "SUCCEED":
                            video_url = status_data.get("video_url")
                            status_placeholder.empty()
                            st.success("✅ Video Ready!")
                            st.video(video_url)
                            st.download_button("Download Video", video_url)
                            break
                        elif status_data.get("status") == "FAILED":
                            st.error("The AI failed to generate this video. Try a different prompt.")
                            break
                else:
                    st.error(f"Error: {res_data.get('message', 'Failed to start.')}")
            
            except Exception as e:
                st.error(f"Connection Error: {e}")
