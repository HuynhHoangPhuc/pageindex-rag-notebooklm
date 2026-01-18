import requests
import time

BASE_URL = "http://localhost:8000"
EMAIL = f"test_{int(time.time())}@example.com"
PASSWORD = "password123"

def test_api():
    print(f"Testing with User: {EMAIL}")
    
    # 1. Register
    resp = requests.post(f"{BASE_URL}/auth/register", json={
        "email": EMAIL,
        "hashed_password": PASSWORD,
        "full_name": "Test User"
    })
    print(f"Register: {resp.status_code} - {resp.text}")
    if resp.status_code != 200:
        return

    # 2. Login
    resp = requests.post(f"{BASE_URL}/auth/login", data={
        "username": EMAIL, 
        "password": PASSWORD
    })
    print(f"Login: {resp.status_code}")
    if resp.status_code != 200:
        print(resp.text)
        return
    
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Upload File
    # Create a dummy PDF file
    pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000060 00000 n\n0000000120 00000 n\ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n190\n%%EOF"
    
    with open("test_doc.pdf", "wb") as f:
        f.write(pdf_content)
    
    files = {'file': open('test_doc.pdf', 'rb')} # Send as PDF
    resp = requests.post(f"{BASE_URL}/upload", headers=headers, files=files)
    print(f"Upload: {resp.status_code}")
    if resp.status_code != 200:
        print(resp.text)
        # Proceed only if upload worked (it might fail if API key invalid, but local save works)
    
    if resp.status_code == 200:
        doc = resp.json()
        doc_id = doc["pageindex_file_id"]
        print(f"Uploaded Doc ID: {doc_id}")
        
        # 4. Chat
        if doc_id != "mock_id":
            payload = ["test_doc.txt"] # Wait, check api definition.
            # In api.py: chat(query: str, file_ids: list[str])
            # query is param, file_ids is body.
            
            resp = requests.post(
                f"{BASE_URL}/chat", 
                headers=headers, 
                params={"query": "How does PageIndex work?"},
                json=[doc_id]
            )
            print(f"Chat: {resp.status_code}")
            print(f"Response: {resp.text}")
        else:
             print("Skipping chat test as Mock ID was returned (likely due to missing API key or mock logic)")

    # 5. List Docs
    resp = requests.get(f"{BASE_URL}/documents", headers=headers)
    print(f"List Documents: {resp.status_code} - {len(resp.json())} docs found")

test_api()
