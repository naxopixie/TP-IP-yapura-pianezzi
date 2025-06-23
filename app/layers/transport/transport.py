# capa de transporte/comunicación con otras interfaces o sistemas externos.

import requests
from ...config import config

# comunicación con la REST API.
# este método se encarga de "pegarle" a la API y traer una lista de objetos JSON.
def getAllImages():
    json_collection = []
    for id in range(1, 31):
        response = requests.get(config.STUDENTS_REST_API_URL + str(id))

        # si la búsqueda no arroja resultados, entonces retornamos una lista vacía de elementos.    
        if not response.ok:
            print(f"[transport.py]: error al obtener datos para el id {id}")
            continue

        raw_data = response.json() # Esto convierte la respuesta de la API en un diccionario. Ejemplo: {'id': 1, 'name': 'bulbasaur', 'base': 64, 'types': ['grass', 'poison']}

        if 'detail' in raw_data and raw_data['detail'] == 'Not found.':
            print(f"[transport.py]: Pokémon con id {id} no encontrado.")
            continue

        json_collection.append(raw_data)

    return json_collection # Esto retorna un listado de imágenes crudas. Ejemplo: [{'id': 1, 'name': 'bulbasaur', 'base': 64, 'types': ['grass', 'poison']}, {'id': 2, 'name': 'ivysaur', 'base': 142, 'types': ['grass', 'poison']}, {'id': 3, 'name': 'venusaur', 'base': 236, 'types': ['grass', 'poison']}]

# obtiene la imagen correspodiente para un type_id especifico 
def get_type_icon_url_by_id(type_id):
    base_url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/colosseum/' # Esto define la url base de las imágenes de los tipos. Sin embargo, no funciona (Error 404).
    return f"{base_url}{type_id}.png"