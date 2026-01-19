import os
from pageindex import PageIndexClient
from dotenv import load_dotenv

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY")
client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

# Use the test PDF we created earlier
file_path = "test_doc.pdf"

# Create dummy PDF if not exists
if not os.path.exists(file_path):
    pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000060 00000 n\n0000000120 00000 n\ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n190\n%%EOF"
    with open(file_path, "wb") as f:
        f.write(pdf_content)

print("Submitting document...")
try:
    response = client.submit_document(file_path=file_path)
    print("Response Type:", type(response))
    print("Response Content:", response)
    
    # Try to extract ID
    if isinstance(response, dict):
        print("ID from dict:", response.get('id') or response.get('doc_id'))
    else:
        print("ID from attr:", getattr(response, 'id', None) or getattr(response, 'doc_id', None))

except Exception as e:
    print(f"Upload failed: {e}")
