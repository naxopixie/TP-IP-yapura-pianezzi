# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages() # Esto retorna un listado de cards. Ejemplo: [Card(id=1, name='bulbasaur', base=64, types=['grass', 'poison']), Card(id=2, name='ivysaur', base=142, types=['grass', 'poison']), Card(id=3, name='venusaur', base=236, types=['grass', 'poison'])]
    favourite_list = []
    favourite_list_ids = []
    
    if request.user.is_authenticated: # Esto verifica si el usuario está logueado.
        favourite_list = services.getAllFavourites(request) # si el usuario está logueado, se obtiene el listado de favoritos.
        favourite_list_ids = [fav.id for fav in favourite_list]

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list, 'favourite_list_ids': favourite_list_ids }) # Esto renderiza el template 'home.html' con los listados de cards y favoritos.

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '') # Esto obtiene el nombre del pokemon ingresado por el usuario.

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''): # Esto verifica si el usuario ingresó algo en el buscador.
        images = services.filterByCharacter(name) # Esto filtra las cards por el nombre del pokemon.
        favourite_list = []
        favourite_list_ids = []
        
        if request.user.is_authenticated: # Esto verifica si el usuario está logueado.
            favourite_list = services.getAllFavourites(request) # si el usuario está logueado, se obtiene el listado de favoritos.
            favourite_list_ids = [fav.id for fav in favourite_list]

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list, 'favourite_list_ids': favourite_list_ids }) # Esto renderiza el template 'home.html' con los listados de cards y favoritos.
    else:
        return redirect('home') # Esto redirige a la página de inicio, ya que no se ingresó nada en el buscador.

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '') # Esto obtiene el tipo del pokemon ingresado por el usuario.

    if type != '': # Esto verifica si el usuario ingresó algo en el buscador.
        images = services.filterByType(type) # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        favourite_list = []
        favourite_list_ids = []
        
        if request.user.is_authenticated: # Esto verifica si el usuario está logueado.
            favourite_list = services.getAllFavourites(request) # si el usuario está logueado, se obtiene el listado de favoritos.
            favourite_list_ids = [fav.id for fav in favourite_list]

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list, 'favourite_list_ids': favourite_list_ids }) # Esto renderiza el template 'home.html' con los listados de cards y favoritos.
    else:
        return redirect('home') # Esto redirige a la página de inicio, ya que no se ingresó nada en el buscador.

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list}) # Esta función se usa para obtener el listado de favoritos y mostrarlo en el template 'favourites.html'.

@login_required
def saveFavourite(request):
    result = services.saveFavourite(request)
    if result:
        return redirect('home')
    else:
        # Manejar error si es necesario
        return redirect('home') # Esta función se usa para guardar un favorito en la base de datos.

@login_required
def deleteFavourite(request):
    result = services.deleteFavourite(request)
    if result:
        return redirect('favoritos')
    else:
        return redirect('favoritos') # Esta función se usa para eliminar un favorito de la base de datos.

@login_required
def exit(request):
    logout(request)
    return redirect('home')