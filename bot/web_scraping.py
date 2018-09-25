import os
from bot.crawler import BuscatanCrawler

class BuscatanScraping:
    """ Clase que proporciona los métodos y atributos para realizar un scraping
    de la plataforma Buscatan """

    def __init__(self, term, url_base, url_search_parameter):
        self.word = term
        self.crawler = BuscatanCrawler(url_base, url_search_parameter)
        self.url_search_parameter = url_search_parameter
        self._ads = [] # atributo privado

    @property
    def ads(self):
        """ getter para el atribuco _ads"""
        return self._ads

    def search(self):
        """ se hace la busqueda de un término en la plataforma de buscatán """
        data = self.crawler.request(self.url_search_parameter + self.word)
        return data

    def get_anuncios(self):
        """ Obtiene la seccion en donde se encuentran todos los anuncios de una pagina y devuelve
         una lista donde cada elemento es un diccionario con la información del anuncio, el anuncio
          debe estar como pagado ya que son los clientes que han pagado para anunciarse"""

        # verifica que el conten del crawler tenga datos (código html)
        if self.crawler.content != "":
            # realiza la busqueda de la sección en donde se encuentran los anuncios en el html
            ads_start = self.crawler.content.find("<div id='anuncios'>")
            if "id='paginacion'" not in self.crawler.content:
                ads_end = self.crawler.content.find("<!--#anuncios-->")
            else:
                ads_end = self.crawler.content.find("<!--#anuncios-->")

            # si existe la seccion anuncios entra para ir obteniendo cada uno de ellos
            if ads_start != 1:
                # elimina el html que se encuentra de más y solamente deja la sección donde están los anuncios
                html = self.crawler.content[ads_start:ads_end]

                ads_start = 0 # al cambiar la variable html se debe reiniciar el índice de donde comienzan los anuncios

                while True:
                    # ads_start recibirá el final del anuncio para poder buscar el siguiente de la lista
                    #TODO: debes pasar al método privado el html de la sección de anuncios, así como el índice
                    #TODO: desde donde comenzará a buscar, recuerda que el método devuelve
                    #TODO: dos valores, los nomrbes de las variables deben ser info_ad, ads_start.

                    info_ad, ads_start = self._get_anuncio(html, ads_start)
                    #aquí va tu codigo

                    # si ya no encuentra mas anuncios rompe el ciclo para ya no seguir buscando
                    if info_ad is None and ads_start == -1:
                        break
                    elif info_ad is not None:
                        # se añade el diccionario con la información del anuncio a la lista _ads
                        self._ads.append(info_ad)
            return self._ads

    def _get_anuncio(self, html, start):
        """Privado: Busca la sección del anuncio empezando desde el indice start el cual es el final
         del anuncio anterior y devuelve un diccionario
        con la información del anuncio y el índice del final del anuncio"""

        start_pattern = "<td class='info'>"
        # realiza la busqueda del patrón info que es en donde se encuentra la información del anuncio
        # para ir avanzando se pasa el índice desde donde debe comenzar
        start = html.find(start_pattern, start)
        end = html.find("<!--.info-->", start) # en el html con esa cadena se marca el final de cada anuncio

        if start == -1:
            return None, -1

        # se obtiene la cadena que contiene la información del anuncio
        new_html = html[start+len(start_pattern):end]
        # la cadena contiene algunos caracteres de escape por lo que se deben eliminar para mayor claridad
        new_html = new_html.replace("\n", "").replace("\t", "").replace("\r", "")

        # verifica que el anuncio sea de los clientes que han pagado para poder obtener su información
        if "<h2 class='pagado'>" in new_html:
            title = self._get_title(new_html)
            phone = self._get_phone(new_html)
            address = self._get_address(new_html)
            web = self._get_web_site(new_html)

            # TODO: Debes crear un diccionario con las cabeceras Titulo, Telefono, Direccion y Web como llaves, así como
            # TODO: pasarle los valores correspondientes que ya se han obtenido
            #aqui va tu codigo
            ad = {
                'Título': title,
                'Teléfono': phone,
                'Dirección': address,
                'Web': web
            }

            return ad, end
        else:
            return None, end

    def _get_phone(self, html):
        """ busca dentro del html del anuncio la clase telefono y
        obtiene los datos para retornarlos, reemplaza algunos simbolos por /"""
        pattern = "<tr class='telefono'>"
        if pattern in html:
            # Se obtiene la sección en donde se encuentra el título
            index = html.find(pattern)
            end = html.find("</tr>", index)
            html_tr = html[index + (len(pattern)):end]

            # Se obtiene el telefono, primero se busca el indice en donde empieza <h3>
            # TODO: debes obtener la cadena dentro de h3 la cual es el teléfono, si no existe debes devolver una cadena
            # TODO: vacía, debes tener una variable index que representa el inicio, y una end que representa el final

            #aquí a tu código
            index = html_tr.find("<h3>")
            if index == -1:
                return ""
            # se busca el tag de cierre </h3>
            end = html_tr.find("</h3>", index)

            phone = html_tr[index + len('</h3>')-1:end]
            phone = phone.replace(",", "/").replace("|", '/').replace("-", "/")
            return phone
        else:
            return ""

    def _get_title(self, html):
        """ busca el titulo del anuncio y lo retorna, antes reemplaza el | por /"""
        #verifica que el anuncio sea pagago
        pattern = "<h2 class='pagado'>"
        if pattern in html:
            # Se obtiene la sección en donde se encuentra el título
            index = html.find(pattern)
            end = html.find("</h2>")
            html_h2 = html[index+(len(pattern)):end]

            # Se obtiene el título, se busca el cierre del tag <a que es >
            index = html_h2.find(">")
            if index == -1:
                return ""
            # se busca el tag de cierre </a>
            end = html_h2.find("</a>")
            return html_h2[index+1:end].replace("|", "/")
        else:
            return ""

    def _get_address(self, html):
        """ busca dentro del html la dirección del anuncio, lo retorna pero antes
        reeamplaza el pipe | por /, si no encuentra la dirección devuelve vacio """

        pattern = "<tr class='direccion'>"
        # verifica que el anuncio tenga una dirección
        if pattern in html:
            # Se obtiene la sección en donde se encuentra la dirección
            index = html.find(pattern)
            end = html.find("</tr>", index)
            html_tr = html[index + (len(pattern)):end]

            # Se obtiene la dirección, primero se busca el indice en donde empieza la etiqueda html <p>
            index = html_tr.find("<p>")
            if index == -1:
                return ""
            # se busca el tag de cierre de la etiqueda </p>
            end = html_tr.find("</p>", index)
            address = html_tr[index + len('</p>')-1:end]
            address = address.replace("<br>", " ").replace("</br>", ' ').replace("|", "/")
            return address
        else:
            return ""

    def _get_web_site(self, html):
        """ busca en el html el sitio web del anunciante, lo retorna y si no lo encuentra
        retorna vacío"""

        # verifica que el anuncio tenga el sitio web del cliente
        # TODO: debes encontrar el patrón para realizar la búsqueda del sitio web, recuerdar usar el nombre
        # TODO: de la variable: pattern

        #aquí va tu código

        pattern = "<tr class='internet'>"

        if pattern in html:
            # Se obtiene la sección en donde se encuentra el sitio web
            index = html.find(pattern)
            end = html.find("</tr>", index)
            html_tr = html[index + (len(pattern)):end]

            # Se obtiene el sitio web, primero se busca el indice en donde empieza la etiqueta <a>
            index = html_tr.find("<a")
            if index == -1:
                return ""
            html_link = html_tr[index:]
            # se busca el cierre del tag a
            index = html_link.find('>')
            # se busca el tag html de cierre </a>
            end = html_link.find("</a>", index)
            address = html_link[index+1:end]
            return address
        else:
            return ""

    def _is_ads_empty(self):
        """ verifica si se ha encontrado algún anuncio en la búsqueda"""
        if self._ads:
            return False
        else:
            return True

    def save(self):
        """ guarda los datos que se encuentran en _ads, en un archivo con el nombre del término
         que se ha encontrado"""
        try:
            # obtiene la ruta en donde se encuentra el archivo donde se ejecuta la instrucción
            path = os.path.abspath(__file__)
            # obtiene la ruta para poder concatenar con el archivo que queremos crear
            dir_path = os.path.dirname(path)

            # si el término tiene espacios en blanco los reeamplaza con _
            term = self.word.replace(" ", "_")
            directory = "{}/documents/{}.txt".format(dir_path, term)
            if not self._is_ads_empty():
                print("Guardando datos...")
                # elimina el archivo si existe uno con el mismo nombre
                self._delete_file()
                is_header = False # bandera que ayudará a saber si ya se guardo la primera línea del documento

                # abre el archivo para poder escribir
                with open(directory, 'a') as f:
                    # recorre los anuncios en la lista
                    for ad in self._ads:
                        # verifica si ya se ha guardado la primera linea la cual deben ser las cabeceras
                        if not is_header:
                            # el objeto dict_keys que devuelve la funcion key se transforma a lista
                            headers = list(ad.keys())
                            # TODO: debes guardar en el archivo como primera línea las cabeceras
                            # TODO: conformadas por las llaves, estas se separan con un pipe
                            # TODO: de igual forma, debes evitar que por cada anuncio se guarde una linea con las
                            # TODO: cabeceras, ya que solo deben ir una vez como primer línea, ya tienes una lista en headers

                            # aqui va tu código
                            headers = list(ad.keys())
                            headers = '|'.join(headers)
                            f.write(headers + "\n")
                            is_header = True
                        # se guarda la información del anunciante
                        values = list(ad.values())
                        values = '|'.join(values)
                        f.write(values + '\n')
                print("Se ha guardado la información en {}".format(directory))
            else:
                print("No se tienen anuncios")

        except Exception as exc:
            print(exc)

    def _delete_file(self, file=""):
        """ verifica si existe un archivo con el nombre del término que tiene los datos de los anunciantes
         y lo elimina"""
        try:
            # obtiene la ruta en donde se encuentra el archivo donde se ejecuta la instrucción
            path = os.path.abspath(__file__)
            # obtiene la ruta para poder concatenar con el archivo que queremos eliminar
            dir_path = os.path.dirname(path)
            term = self.word.replace(" ", "_")
            # si no se envia un nombre de archivo, toma el valor de word
            directory = "{}/documents/{}.txt".format(dir_path, self.word) if file == "" else "{}/documents/{}".format(dir_path, file)
            # TODO: elimina el archivo el cual ya se apunta en la variable directory

            #aquí va tu código
            os.remove(directory)
        except:
            return None

    @staticmethod
    def delete_all_files():
        """ método estático de la clase que se encarga de borrar todos los archivos del directorio """
        try:
            # obtiene la ruta en donde se encuentra el archivo donde se ejecuta la instrucción
            path = os.path.abspath(__file__)
            # obtiene la ruta para poder concatenar con el archivo que queremos eliminar
            dir_path = os.path.dirname(path)
            directory = '{}/documents/'.format(dir_path)

            #TODO: debes eliminar cada archivo del directorio, la ruta ya se encuentra en directory
            #TODO: debes imprimir un mensaje, para que el usuario sepa en cada momento que archivo
            #TODO: se esta eliminando

            #aquí va tu código
            for filename in os.listdir(directory):
                if filename.endswith('.txt'):
                    print("Eliminando archivo {}".format(filename+'.txt'))
                    os.remove(directory + filename)

        except Exception as exc:
            print(exc)

    @staticmethod
    def read_file(filename):
        """ método estático que se encarga de leer un arhivo, recibe el nombre del archivo como parámetro"""
        try:
            # obtiene la ruta en donde se encuentra el archivo donde se ejecuta la instrucción
            path = os.path.abspath(__file__)
            # obtiene la ruta para poder concatenar con el archivo que queremos leer
            dir_path = os.path.dirname(path)

            if filename.endswith('.txt'):
                directory = "{}/documents/{}".format(dir_path, filename)
            else:
                directory = "{}/documents/{}.txt".format(dir_path,filename)

            # abre el archivo como solo lectura
            with open(directory, 'r') as f:
                lines = f.readlines()

                # verifica que el archivo tenga información, la información debe ser una lista
                # donde cada elemento es una linea del archivo, la primera son las cabeceras
                if len(lines) > 0:
                    # obtiene la primera línea del archivo (las cabeceras), y lo elimina de la lista
                    header = lines.pop(0).replace("\n", "")
                    # se convierte la cadena en una lista donde cada elemento es una etiqueta o cabecera
                    headers = header.split("|")

                    # recorre cada linea con la información de los clientes y la imprime
                    # tomando en cuenta el formato cabecera: info
                    for l in lines:
                        #TODO: debes imprimir basado en el formato que se explica en el documento
                        #TODO: recuerda que ya tienes en headers una lista donde cada elemento es una cabecera
                        #TODO: y que l es una linea la cual divide con el | (pipe) cada información del anunciante
                        #TODO: y cada información corresponde a una cabecera, puedes usar split
                        print("------------------------------------------------------------")
                        # aquí va tu código
                        l = l.split("|")
                        for index, element in enumerate(l):
                            line_to_print = "{}: {}".format(header[index], element)
                            print(line_to_print)
                        print("************************************************************")
        except IOError as ioerror:
            print("Puede que el archivo no exista")
            print(ioerror)

if __name__ == '__main__':
    # Para pruebas, debes cambiar
    b = BuscatanScraping('pizzas', 'http://www.buscatan.com/directorio/', '?b=')
    b.crawler.generate_queue(b.search())
    anuncios = b.get_anuncios()
    while not b.crawler.is_queue_empty():
        url = b.crawler.get_url()
        b.crawler.request(url)
        anuncios = b.get_anuncios()
    b.save()

    # eliminar todos los archivos
    #BuscatanScraping.delete_all_files()
    # Leer archivo
    BuscatanScraping.read_file('pizzas')




