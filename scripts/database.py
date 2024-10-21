import os
from supabase import create_client, Client

url: str = 'https://rmifubwuwvkiawgakwno.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJtaWZ1Ynd1d3ZraWF3Z2Frd25vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjg4MTcwNDksImV4cCI6MjA0NDM5MzA0OX0.6ZDINmoFFgYVzEENBaGyWB1XfMjqBqbgURsNC8SbEoQ'
supabase: Client = create_client(url, key)

def read_medico():
    return supabase.table("utilizadores").select("*").execute()

# custom_schema_query = """
# GRANT USAGE ON SCHEMA mfr_questionarios TO anon, authenticated, service_role;
# """
# supabase.rpc("execute_sql", {"sql": custom_schema_query}).execute()

def write_medico_to_db(data):
  response = (
    supabase.table("utilizadores")
    .insert({
      "nome": data["nome"], 
      "apelido": data["apelido"],
      "email": data["email"],
      "morada": data["morada"],
      "morada_2": data["morada_2"],
      "pais": data["pais"],
      "distrito": data["distrito"],
      "codigo_postal": data["codigo_postal"]})
    .execute()
  )


# rows = response.data

# if rows:
#   row_dict = dict(rows[1])
#   print(row_dict)