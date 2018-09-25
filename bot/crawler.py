import requests

class BuscatanCrawler:
    """ Esta clase proporciona los métodos para realizar las peticiones a la página,
     ási como una url base y una cola para almacenar las paginas que se deben visitar,
      recibe dos parámetros para inicializar.

      _content mantiene el valor de la última página visitada
      _url_queue es una lista con las páginas a visitar
      """

    def __init__(self, base_url, url_search_parameter):
        self.base_url = base_url
        self.url_search_parameter = url_search_parameter
        self._url_queue = []
        self._content = "" # atributo privado


    def request(self, url_path):
        """ realiza una petición http, conformando la url con la url base y el parámetro url_path
        la información que regresa (código html) se guarda como cadena en el atributo _content y
        se retorna de igual manera."""
        self._content = ""
        """ Método que recibe un path de una url y retorna el contenido html """
        url = ""
        
        # se forma la url completa para realizar la petición
        if self.base_url.endswith('/') and not url_path.startswith('/'):
            url = self.base_url + url_path
        elif not self.base_url.endswith('/') and url_path.startswith('/'):
            url = self.base_url + url_path
        else:
            raise Exception("No puede formarse la url de forma correcta")
        # se realiza la petición usando el método get de request
        #TODO: realizar la petición usando la biblioteca requests, y el método get de dicha biblioteca
        #TODO: recuerda que la cadena que representa la url ya esta en su formato y esta asignada a la variable url


        r = requests.get(url)# aquí va tu código

        # se asigna el contenido a _content
        self._content = r.text
        return r.text

    @property
    def content(self):
        """ devuelve el contenido de la última página visitada """
        return self._content

    @property
    def url_queue(self):
        """ devuelve la lista con las páginas a visitar"""
        return self._url_queue

    @url_queue.setter
    def url_queue(self, path):
        if isinstance(path, str):
            path = path.replace("\n", "").replace("<br>", "").replace("\t", "")
            self._url_queue.append(path)

    def get_url(self):
        """ Método que saca al primer elemento de la lista y lo retorna """
        if len(self._url_queue) > 0:
            return self._url_queue.pop(0)
        else:
            return None

    def is_queue_empty(self):
        """ Verifica si la cola no contiene mas urls como paginas"""
        if len(self._url_queue) > 0:
            return False
        else:
            return True

    def generate_queue(self, html):
        """ busca en la página web si se tiene paginación, si es así obtiene la página que se debe visitar
        y la añade a _url_queue
        """
        
        # realiza una búsqueda de la subcadena paginación, para saber si cuenta con ello
        start = html.find("id='paginacion'")
        
        # busca el cierre de la paginación
        end = html.find('</div>', start)
        # crea la variable html y asigna la sección de código html que contiene los datos de la paginación

        #TODO: debes asignar a la variable html, una cadena la cual contiene solamente el pedazo de html
        #TODO: de la paginación, ya que en ella tendrás que buscar cada una de las páginas
        #TODO: recuerda que ya tienes los índices y la variable html contiene todo el código html de la web

        html = html[start:end]# aqui va tu codigo

        start = 0
        
        # realiza un ciclo que hace la búsqueda de las páginas que contiene la paginación
        while start != -1:
            # las páginas estan dentro de un link (etiqueta <a> en html)
            start_pattern = "<a href='"
            # va cambiando el índice de inicio de la búsqueda para no tomar siempre el primero de lacadena

            #TODO: debes encontrar el patrón que está en start_pattern para cada página de la paginación
            #TODO: ya se proporcionan las variables que debes manejar, solamente falta la instrucción correcta
            #TODO: la variable path, debe tener asignada una cadena similar a: "medicos-pag2.html"
            start = html.find(start_pattern, start+1, end)# aqui va tu codigo
            end_a = html.find("'>", start+1, end)# aqui va tu codigo
            path = html[start + len(start_pattern):end_a]# aquí va tu código
            
            # si encuentra caracteres de escape o el tag de salto de linea en html, lo cambia
            path = path.replace("\n", "").replace("<br>", ""). replace("</br>", "").replace("\t", "")
            # si encuentra que el link tiene un parámetro html title, no toma en cuenta ese link
            # esto se debe a que en el código eso representa a siguiente (ver paginación)
            if 'title' in path:
                continue
            
            if start == -1:
                # si ya no encuentra mas links rompe el ciclo
                break
            # se añade la página a la cola
            self._url_queue.append(path)



if __name__ == '__main__':
    c = BuscatanCrawler("http://www.buscatan.com/directorio/", "?b=")
    print(c.request('medicos-pag2.html'))
    c.generate_queue(c.content)
    print(c.url_queue)

