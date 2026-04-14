from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_ANON_KEY')

client = create_client(url, key)
data = client.table('products').select('count').execute()

print("✅ Supabase Connected!", data)