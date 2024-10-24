import os
from supabase import create_client, Client

url: str = 'https://rmifubwuwvkiawgakwno.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJtaWZ1Ynd1d3ZraWF3Z2Frd25vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjg4MTcwNDksImV4cCI6MjA0NDM5MzA0OX0.6ZDINmoFFgYVzEENBaGyWB1XfMjqBqbgURsNC8SbEoQ'
supabase: Client = create_client(url, key)

def read_users():
    result = supabase.table("utilizadores").select("id", "nome").execute()

    new_dict = {}
    count = 1
    print(result.data)
    for user in result.data:
       key = f'user_{count}'
       new_dict[key] = user
       count = count + 1

    return new_dict


if __name__ == "__main__":
    print(read_users())