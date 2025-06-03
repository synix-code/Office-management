import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import DELETE_FIELD

# Firebase की initialization
cred = credentials.Certificate("office-hub.json")  # अपना Firebase service account JSON path यहां डालें
firebase_admin.initialize_app(cred)

# Firestore client को initialize करें
db = firestore.client()

# Firestore डोक्यूमेंट का रेफेरेंस प्राप्त करें
doc_ref = db.collection('users').document('butterflyowner1@gmail.com')

# डोक्यूमेंट के सभी keys को प्रिंट करें
doc = doc_ref.get()
print("=== ALL KEYS IN DOCUMENT ===")
print(doc.to_dict().keys())  # यह डोक्यूमेंट में मौजूद सभी keys को प्रिंट करेगा

# डिलीट करने के लिए key को ढूंढें
key_to_delete = "employee.Pankaj"  # यहाँ वह key डालें जिसे आप डिलीट करना चाहते हैं

# अगर key पाई जाती है, तो उसे डिलीट करें
if key_to_delete in doc.to_dict():
    print(f"Found key to delete: {key_to_delete}")
    doc_ref.update({
        key_to_delete: DELETE_FIELD
    })
    print(f"✅ Employee '{key_to_delete}' deleted successfully.")
else:
    print(f"Key '{key_to_delete}' not found.")

# डोक्यूमेंट के अपडेटेड डेटा को चेक करें
updated_doc = doc_ref.get()
print("\n=== UPDATED DOCUMENT ===")
print(updated_doc.to_dict())  # यह डोक्यूमेंट के अपडेटेड डेटा को प्रिंट करेगा
