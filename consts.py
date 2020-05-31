from os.path import join
headers = {
       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0)' +
       ' Gecko/20100101 Firefox/45.0'
}

base_url = "https://wikiroutes.info"
catalog_url = "https://wikiroutes.info/spb/catalog"

files_folder = r".\files"
route_pages_folder = join(files_folder, "route_pages")
routes_href_path = join(files_folder, "route_hrefs.json")
routes_detailed_path = join(files_folder, "route_detailed.json")
catalog_page_path = join(files_folder, "catalog.html")
graph_l_path = join(files_folder, "graph_l.csv")
graph_p_path = join(files_folder, "graph_p.csv")
graph_c_path = join(files_folder, "graph_c.csv")
default_encoding = "utf8"

sleep_time = 5
