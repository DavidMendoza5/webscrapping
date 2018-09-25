#TODO: importar el módulo de web_scraping y la clase BuscatanScraping
from bot.web_scraping import BuscatanScraping
from bot.crawler import BuscatanCrawler

# aquí va tu código para importar la clase BuscatanScraping

def bot():
    term = input("¿Qué desea buscar?: \n")

    # se crea una instancia del objeto BuscatanScraping, pasandole los parámetros necesarios

    #TODO: Se debe crear la instancia del objeto BuscatanScraping, la variable a la que se asigna la instancia
    #TODO: debe llamarse b
    b = BuscatanScraping(term, 'http://www.buscatan.com/directorio/', '?b=')
    # aquí va tu código

    print("Buscando...")
    # se le indica al crawler que verifique si hay paginación en la página
    b.crawler.generate_queue(b.search())
    # Se obtienen los datos de la primera página
    b.get_anuncios()

    # verifica si no existe paginacion y no se obtuvieron datos de la primera página
    # puede ser que no se haya encontrado nada en la búsqueda
    if b.crawler.is_queue_empty() and len(b.ads) == 0:
        print("No se encontraron datos")
        return None

    # si se cuenta con paginación se obtienen los datos de cada página
    while not b.crawler.is_queue_empty():
        # obtiene la siguiente url
        url = b.crawler.get_url()
        # obtiene el contenido de la nueva página
        b.crawler.request(url)
        # obtiene los anuncios
        b.get_anuncios()

    # se guarda toda la información que se obtuvo
    #TODO: guarda la información obtenida, revisa la clase BuscatanScraping y verifica si existe
    #TODO: un método para hacerlo

    # aquí va tu código
    b.save()

def delete_all():
    print("Eliminando archivos con la información de los anunciantes.")
    #TODO: Se debe llamar al método estático para eliminar los archivos con la información de los anunciantes
    BuscatanScraping.delete_all_files()

def read_file():
    filename = input("¿Qué archivo desea leer para visualizar la información?: \n")
    if filename != "":
        BuscatanScraping.read_file(filename)

def menu():
    menu = """
    a) Obtener información
    b) Leer Información
    c) Eliminar todos los archivos
    d) Salir
    
    """
    while True:
        print("----------- MENU --------------")
        print(menu)
        option = input("Elija una opción: \n")
        print()
        # TODO: crea la logica para el menú, por cada opción se debe llamar a la función correspondiente
        # TODO: y si el usuario proporciona la opcion salir, el cliclo debe finalizar
        # TODO: si el usuario proporciona una opción que no se tiene en el menú, debe imprimir
        # TODO: el mensaje: Debe seleccionar una opción válida

        # aquí va tu código
        if option == "d":
            print("Hasta luego!!!")
            break
        elif option.lower() == 'a':
            bot()
        elif option.lower() == 'b':
            read_file()
        elif option.lower() == 'c':
            delete_all()
        else:
            print("Debe seleccionar una opción válida.")


if __name__ == '__main__':
    menu()


