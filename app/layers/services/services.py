# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    listaCards = []
   
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    rawImages = transport.getAllImages() 

    # 2) convertir cada img. en una card.
    for rawImage in rawImages:
        card = translator.fromRequestIntoCard(rawImage) # Esto convierte cada imagen cruda en una card. Ejemplo: Card(id=1, name='bulbasaur', base=64, types=['grass', 'poison']), esto es una clase que se encuentra en el archivo translator.py
        listaCards.append(card)
    
    # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
    return listaCards # Esto retorna un listado de cards. Ejemplo: [Card(id=1, name='bulbasaur', base=64, types=['grass', 'poison']), Card(id=2, name='ivysaur', base=142, types=['grass', 'poison']), Card(id=3, name='venusaur', base=236, types=['grass', 'poison'])]

# función que filtra según el nombre del pokemon.
def filterByCharacter(name): #name = 'bulbasaur'
    filtered_cards = []
    cards = getAllImages() # Esto retorna un listado de cards. Ejemplo: [Card(id=1, name='bulbasaur', base=64, types=['grass', 'poison']), Card(id=2, name='ivysaur', base=142, types=['grass', 'poison']), Card(id=3, name='venusaur', base=236, types=['grass', 'poison'])]

    for card in cards: # Esto recorre cada card del listado de cards.
        if name.lower() in card.name.lower(): # Esto verifica si el nombre del pokemon coincide con el nombre recibido por parámetro.
            filtered_cards.append(card)

    return filtered_cards # Esto retorna un listado de cards filtrados. Ejemplo: [Card(id=1, name='bulbasaur', base=64, types=['grass', 'poison'])]

# función que filtra las cards según su tipo.
def filterByType(type_filter): #type_filter = 'grass'
    filtered_cards = []
    cards = getAllImages() # Esto retorna un listado de cards. Ejemplo: [Card(id=1, name='bulbasaur', base=64, types=['grass', 'poison']), Card(id=2, name='ivysaur', base=142, types=['grass', 'poison']), Card(id=3, name='venusaur', base=236, types=['grass', 'poison'])]

    for card in cards: # Esto recorre cada card del listado de cards.
        for type in card.types: # Esto recorre cada tipo de la card.
            if type_filter.lower() == type.lower(): # Esto verifica si el tipo del pokemon coincide con el tipo recibido por parámetro.
                filtered_cards.append(card) 

    return filtered_cards # Esto retorna un listado de cards filtrados. Ejemplo: [Card(id=1, name='bulbasaur', base=64, types=['grass', 'poison']), Card(id=2, name='ivysaur', base=142, types=['grass', 'poison']), Card(id=3, name='venusaur', base=236, types=['grass', 'poison'])]

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request) # transformamos un request en una Card (ver translator.py). fromTemplateIntoCard es una función que convierte un request en una Card.
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.get_all_favourites(user) # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = translator.fromRepositoryIntoCard(favourite) # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower()) # Esto obtiene el id correspondiente a un tipo según su nombre. Ejemplo: 'grass' -> 1
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id) # Esto obtiene la url de la imagen correspondiente a un tipo según su id. Ejemplo: 1 -> 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/colosseum/grass.png'