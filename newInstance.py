from queries import get_character, set_session

def new_instance():
  
  chosen_character = get_character()
  print("Connected to database successfully!: ", chosen_character)

  chosen_character_name = chosen_character[1]
  chosen_character_prompt = chosen_character[2]["promptContext"]
  chosen_character_fav_color = chosen_character[3]

  session_data = set_session(chosen_character_prompt, chosen_character_name, chosen_character_fav_color)

  print("Session Data: ", session_data)

  return session_data