from Core.helper import has_valid_sale_session


def has_valid_session(request):

    context = {"has_valid_session" : has_valid_sale_session()}
    return context