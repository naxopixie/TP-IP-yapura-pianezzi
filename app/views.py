# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()
    favourite_list = []
    
    if request.user.is_authenticated:
        favourite_list = services.getAllFavourites(request) # si el usuario está logueado, se obtiene el listado de favoritos.

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = services.filterByCharacter(name)
        favourite_list = []
        
        if request.user.is_authenticated:
            favourite_list = services.getAllFavourites(request) # si el usuario está logueado, se obtiene el listado de favoritos.

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        images = services.filterByType(type) # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        favourite_list = []
        
        if request.user.is_authenticated:
            favourite_list = services.getAllFavourites(request) # si el usuario está logueado, se obtiene el listado de favoritos.

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

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