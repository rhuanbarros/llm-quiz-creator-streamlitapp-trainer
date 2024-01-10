from supabase import create_client, Client
import json

url = "https://xoxlgvakygiyfijfeixu.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhveGxndmFreWdpeWZpamZlaXh1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNDkyNzU2NywiZXhwIjoyMDIwNTAzNTY3fQ.V3766GRj6hkt1Ci-52tjSiULVoF3nfCPPDnR6Hc_rT0"

supabase: Client = create_client(url, key)

with open('./src/database_scripts/jsons/q1.json', 'r') as file:
    data_questions = json.load(file)

    
data, count = supabase.table('questions').insert(data_questions).execute()
print(data)


