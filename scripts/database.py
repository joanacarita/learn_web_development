import os
from supabase import create_client, Client

url: str = 'https://rmifubwuwvkiawgakwno.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJtaWZ1Ynd1d3ZraWF3Z2Frd25vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjg4MTcwNDksImV4cCI6MjA0NDM5MzA0OX0.6ZDINmoFFgYVzEENBaGyWB1XfMjqBqbgURsNC8SbEoQ'
supabase: Client = create_client(url, key)

def read_users():
    result = supabase.table("utilizadores").select("id", "nome", "apelido").execute()

    new_dict = {}
    count = 1
    
    for user in result.data:
       key = f'user_{count}'
       new_dict[key] = user
       count = count + 1

    return new_dict

# custom_schema_query = """
# GRANT USAGE ON SCHEMA mfr_questionarios TO anon, authenticated, service_role;
# """
# supabase.rpc("execute_sql", {"sql": custom_schema_query}).execute()
# supabase.table("utilizadores").select("id", "nome").execute()

def write_doctor_to_db(data):
  response = (
    supabase.table("utilizadores")
    .insert({
      "nome": data["firstName"], 
      "apelido": data["lastName"],
      "numero_ordem": data["docID"],
      "email": data["email"],
      "local_trabalho": data["hospitalAdress"]})
    .execute()
  )

def write_patient_to_db(data):
  response = (
    supabase.table("utentes")
    .insert({
      "nome": data["firstName"], 
      "apelido": data["lastName"],
      "numero_utente": data["patientID"],
      "email": data["email"],
      "data_nascimento": data["patientBirthday"],
      "sexo": data["patientSex"],
      "peso": data["patientWeight"],
      "altura": data["patientHeight"]})
    .execute()
  )

def write_respostas_quest_to_db(data):

  list_to_insert = []
  dropdown_user_id = data["dropdown_user_id"]
  quest_nome = data["nome_questionario"]

  for key, value in data.items():
    if 'radioOption' in key:
      new_dict = {}
      new_dict["user_id"] = dropdown_user_id
      new_dict["quest_nome"] = quest_nome
      new_dict["num_pergunta"] = key[-1]
      new_dict["valor_resposta"] = value
      list_to_insert.append(new_dict)

  response = (
    supabase.table("quest_respostas")
    .insert(list_to_insert)
    .execute()
  )
  

# rows = response.data

# if rows:
#   row_dict = dict(rows[1])
#   print(row_dict)
