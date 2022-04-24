import requests


def get_pokemon_Infos(name):

#Getting a dictionary from thr pokeapi
    print("Getting pokemon Info")

    poke_url = 'https://pokeapi.co/api/v2/pokemon/' + name


    response = requests.get(poke_url)

    if response.status_code == 200:
        print('succesffull to get pokeinfo')
        return response.json()
    else:
        print('fail to get info',response.status_code)
        return 

# function for geting pokemon images from pokemon dictionary
def get_pokemon_img_url(name):
    pokemon_dict = get_pokemon_Infos(name)
    if pokemon_dict:
        return pokemon_dict['sprites']['other']['official-artwork']['front_default']

# this function gets a list of 1000 pokemons
def get_pokemon_list(limit=100, offset=0):
    url = 'https://pokeapi.co/api/v2/pokemon'

    params ={
        'limit': limit,
        'offset': offset
    }

    resp_msg = requests.get(url, params=params)

    if resp_msg.status_code == 200:
        resp_dict = resp_msg.json()
        return [p['name']for p in resp_dict['results']]
    else:
        print('Failed to get pokemon list.')
        print('Response code:', resp_msg.status_code)
        print(resp_msg.txt)

