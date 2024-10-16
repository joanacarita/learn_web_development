import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
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