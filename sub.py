


# import streamlit as st
# import subprocess
# import json
# import os

# st.set_page_config(page_title="IBM Cloud File Uploader", layout="centered")

# st.title("IBM Cloud Object Storage Uploader")
# st.subheader("Upload a file securely using IAM Token")

# # User input fields
# apikey = st.text_input("Enter your IBM Cloud API Key", type="password")
# bucket_url = st.text_input("Enter the Cloud Object Storage URL (Bucket Name Only)", 
#                            "https://s3.us-south.cloud-object-storage.appdomain.cloud/ozonetell")

# uploaded_file = st.file_uploader("Choose a file to upload", type=["xlsx", "csv", "txt", "json"])

# # Function to get IAM token
# def get_iam_token(api_key):
#     command = [
#         "curl", "-X", "POST", "https://iam.cloud.ibm.com/oidc/token",
#         "-H", "Accept: application/json",
#         "-H", "Content-Type: application/x-www-form-urlencoded",
#         "--data-urlencode", f"apikey={api_key}",
#         "--data-urlencode", "response_type=cloud_iam",
#         "--data-urlencode", "grant_type=urn:ibm:params:oauth:grant-type:apikey"
#     ]
#     result = subprocess.run(command, capture_output=True, text=True)
    
#     if result.returncode == 0:
#         try:
#             response = json.loads(result.stdout)
#             return response.get("access_token")
#         except json.JSONDecodeError:
#             st.error("Failed to parse IAM token response. Check API Key or connectivity.")
#             st.text(result.stdout)  # Show raw response for debugging
#             return None
#     else:
#         st.error("Error fetching IAM token: " + result.stderr)
#         return None

# # Function to upload file
# def upload_file(access_token, file_path, object_url):
#     command = [
#         "curl", "-X", "PUT", object_url,
#         "-H", f"Authorization: Bearer {access_token}",
#         "-H", "Content-Type: application/octet-stream",
#         "--data-binary", f"@{file_path}"
#     ]
#     result = subprocess.run(command, capture_output=True, text=True)
    
#     if result.returncode == 0:
#         st.success("File uploaded successfully!")
#         st.text(result.stdout)  # Show raw response
#     else:
#         st.error("Error uploading file: " + result.stderr)

# # Upload button
# if st.button("Upload File"):
#     if not apikey or not bucket_url or not uploaded_file:
#         st.warning("Please enter all required fields.")
#     else:
#         st.info("Fetching IAM token...")
#         iam_token = get_iam_token(apikey)
        
#         if iam_token:
#             # Ensure the file is saved temporarily
#             temp_dir = "temp_upload"
#             os.makedirs(temp_dir, exist_ok=True)
#             file_path = os.path.join(temp_dir, uploaded_file.name)

#             with open(file_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())

#             # Construct correct object URL with filename
#             object_url = f"{bucket_url}/{uploaded_file.name}"

#             st.info(f"Uploading file to: {object_url}")
#             upload_file(iam_token, file_path, object_url)

#             # Remove temporary file
#             os.remove(file_path)





import streamlit as st
import subprocess
import json
import os
import mimetypes
import urllib.parse  # Import for URL encoding

st.set_page_config(page_title="IBM Cloud File Uploader", layout="centered")

st.title("IBM Cloud Object Storage Uploader")
st.subheader("Upload a file securely using IAM Token")

# User input fields
apikey = st.text_input("Enter your IBM Cloud API Key", value="qOz5x3iVYdN46A02okc8ZHr91aw28xW6g9cbc3m9sjdV")
bucket_url = st.text_input("Enter the Cloud Object Storage URL (Bucket Name Only)", 
                           "https://s3.us-south.cloud-object-storage.appdomain.cloud/ozonetell")

uploaded_file = st.file_uploader("Choose a file to upload", type=["xlsx", "csv", "txt", "json", "xml","mp3","wav", "calllog"])

# Function to get IAM token
def get_iam_token(api_key):
    command = [
        "curl", "-X", "POST", "https://iam.cloud.ibm.com/oidc/token",
        "-H", "Accept: application/json",
        "-H", "Content-Type: application/x-www-form-urlencoded",
        "--data-urlencode", f"apikey={api_key}",
        "--data-urlencode", "response_type=cloud_iam",
        "--data-urlencode", "grant_type=urn:ibm:params:oauth:grant-type:apikey"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        try:
            response = json.loads(result.stdout)
            return response.get("access_token")
        except json.JSONDecodeError:
            st.error("Failed to parse IAM token response. Check API Key or connectivity.")
            st.text(result.stdout)  # Show raw response for debugging
            return None
    else:
        st.error("Error fetching IAM token: " + result.stderr)
        return None

# Function to upload file with auto-detected MIME type and URL encoding
def upload_file(access_token, file_path, object_url):
    # Detect MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"  # Default binary content-type
    
    command = [
        "curl", "-X", "PUT", object_url,
        "-H", f"Authorization: Bearer {access_token}",
        "-H", f"Content-Type: {mime_type}",
        "--data-binary", f"@{file_path}"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        st.success("File uploaded successfully!")
        st.text(result.stdout)  # Show raw response
    else:
        st.error("Error uploading file: " + result.stderr)

# Upload button
if st.button("Upload File"):
    if not apikey or not bucket_url or not uploaded_file:
        st.warning("Please enter all required fields.")
    else:
        st.info("Fetching IAM token...")
        iam_token = get_iam_token(apikey)
        
        if iam_token:
            temp_dir = "temp_upload"
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, uploaded_file.name)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Encode filename to avoid space and special character issues
            encoded_filename = urllib.parse.quote(uploaded_file.name)
            object_url = f"{bucket_url}/{encoded_filename}"

            st.info(f"Uploading file to: {object_url} (MIME Type: {mimetypes.guess_type(file_path)[0]})")
            upload_file(iam_token, file_path, object_url)

            os.remove(file_path)
