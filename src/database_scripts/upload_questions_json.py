from supabase import create_client, Client
import json
import csv

SUBJECT_MATTER = "LINEAR ALGEBRA"

url = "https://xoxlgvakygiyfijfeixu.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhveGxndmFreWdpeWZpamZlaXh1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNDkyNzU2NywiZXhwIjoyMDIwNTAzNTY3fQ.V3766GRj6hkt1Ci-52tjSiULVoF3nfCPPDnR6Hc_rT0"

supabase: Client = create_client(url, key)

# with open('./src/database_scripts/jsons/q2.json', 'r') as file:
#     data_questions = json.load(file)

data_questions = []

with open('./src/database_scripts/jsons/q4.csv', 'r') as file:
    csv_reader  = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        line = {}
        line["topic_id"] = row[0]
        line["topic_description"] = row[1]
        line["level"] = row[2]
        line["question"] = row[3]
        line["answer"] = row[4]
        line["explanation"] = row[5]
        line["subject_matter"] = SUBJECT_MATTER
        data_questions.append(line)
        
print(data_questions)
            
    
data, count = supabase.table('questions').insert(data_questions).execute()
print(data)


