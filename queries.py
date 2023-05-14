import math
from flask import json
import psycopg2 as pg
import os
from dotenv import load_dotenv

load_dotenv()

db_name = os.environ.get("DB_NAME")
db_uri = os.environ.get("DB_URI")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")

conn = pg.connect(database=db_name, user=db_user, password=db_password, host="containers-us-west-81.railway.app", port="7846")

def get_character():
  cursor = conn.cursor()
  query = "SELECT * FROM characters WHERE name = %s;"
  data = "Jeff"
  cursor.execute(query, (data,))
  query_results = cursor.fetchall()
  print("Got characters: ", query_results[0][1])
  return query_results[0]

def set_session(prompt, name, fav_color):
  cursor = conn.cursor()
  query = "INSERT INTO messages (id, message, character, fav_color) VALUES (NEXTVAL('messages_id_seq'), %s, %s, %s) RETURNING id, fav_color ;"
  prompt_json = json.dumps({"promptContext": prompt})
  data = (prompt_json, name, fav_color)
  cursor.execute(query, data)
  conn.commit()
  print("Session set successfully!")
  return cursor.fetchone()

def get_winners(character):
  cursor = conn.cursor()
  query = "SELECT id, number_of_prompts, user_name, character FROM answers WHERE number_of_prompts > 0 AND character = %s ORDER BY number_of_prompts DESC LIMIT 10;"
  cursor.execute(query, (character,))
  query_results = cursor.fetchall()
  print("Got Winners! : ")
  return query_results

def save_winner(winner_id, username , character):
  query = "INSERT INTO answers (id, answer, number_of_prompts, user_name, character) VALUES (NEXTVAL('answers_id_seq'), %s, %s, %s, %s) RETURNING id ;"
  cursor = conn.cursor()
  print("Saving Winner! : ", winner_id)
  winner_context = get_messages(winner_id)[0][1]
  winner_context_json = json.dumps(winner_context)
  winner_attempt_length = math.ceil((len(winner_context) - 6) / 2)
  print("Winner Context: ", winner_context)
  
  cursor.execute(query, (winner_context_json, winner_attempt_length, username, character))
  conn.commit()
  print("Saved Winner! : ")
  return cursor.fetchall()


async def update_messages(id, prompt):
  cursor = conn.cursor()
  print("Get messages: ==>", prompt)
  current_context: list = await get_messages(id)[0][1]["promptContext"]

  updated_context = current_context.append({"role": "user", "content": prompt})
  print("Current Context: ", current_context, " Type: ", type(current_context))
  print("Updated Context: ", updated_context, " Type: ", type(updated_context))



async def get_messages(id):
  cursor = conn.cursor()
  query = "SELECT * FROM messages WHERE id = %s;"
  cursor.execute(query, (id,))
  query_results = cursor.fetchall()
  return query_results
