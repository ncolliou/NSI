import random


def generate_map(seed, rg):
    """
    Fonction qui renvoie une liste de nombres aléatoires 'smooth', qui s'accordent entre eux
    :param seed: Si seed est identique a chaque fois l'aléatoire sera le meme
    :param rg: la taille de la map
    :return: liste de rg nombres choisi aléatoirement
    """
    random.seed(seed)
    x = 0
    lis = [x]
    for i in range(rg):
        # ajouter un nb aleatoire en -1 et 1 a x pour avoir du 'smooth'
        x += random.randint(-1, 1)
        lis.append(x)
    return better(lis)


def better(lis):
    """
    Fonction qui renvoie une liste mieux organisée (plus 'SMOOTH') pour faire de la generation aleatoire
    :param lis: liste qui sera plus 'SMOOTH'
    :return: la liste en plus 'SMOOTH'
    """
    for i in range(1, len(lis) - 1):
        if lis[i - 1] == lis[i + 1]:
            lis[i] = lis[i - 1]
    return lis


def random_number_int(luck):
    """
    Fonction
    :param luck: chance sur 100
    :return:
    """
    if random.randint(0, 100) <= luck:
        # condition vrai
        return True
    else:
        return False

