import requests
from lxml import html
import json
from os import path, mkdir
from consts import *
from utils import *
import networkx as nx
from matplotlib import pyplot as plt


def get_routes(page):
    catalog_node = page.get_element_by_id("catalogOfRoutesList")
    a_nodes = catalog_node.xpath("//a")
    routes = []
    for a_tag in a_nodes:
        name = a_tag.text
        href = a_tag.attrib['href']
        if name is None or not('routes' in href):
            continue
        routes.append({"name": name, "href": href})
    return routes


def get_routes_detail(routes):
    to_delete = []
    for i in range(len(routes)):
        route = routes[i]
        url = f'{base_url}{route["href"]}'
        filename = path.join(route_pages_folder, route['name']+'.html')
        page = get_or_load_page(url, filename)
        info_parts_wrap = page.xpath('//div[@class="route-part-info-wrap"]')[0]
        parts = info_parts_wrap.xpath('//div[@class="RoutePartInfo"]')
        for part in parts:
            caption = part[0][0].text
            value = part[1].text
            route[caption] = value
        key = 'Маршрут следования:'
        is_used = True
        if (len(page.xpath('//div[@class="route-not-active"]')) > 0):
            is_used = False
        if (not is_used or key not in route or route[key] is None):
            to_delete.append(i)
        else:
            route['stopes'] = parse_itinerary(route['Маршрут следования:'])
    routes = [routes[i] for i in range(len(routes)) if i not in to_delete]
    return routes


def get_graph_L(routes):
    graph = nx.Graph()
    for route in routes:
        stopes = route['stopes']
        graph.add_nodes_from(stopes)
        for i in range(len(stopes)-1):
            graph.add_edge(stopes[i], stopes[i+1])
    return graph


def get_graph_P(routes):
    graph = nx.Graph()
    for route in routes:
        stopes = route['stopes']
        graph.add_nodes_from(stopes)
        for i in range(len(stopes)):
            for j in range(i + 1, len(stopes)):
                graph.add_edge(stopes[i], stopes[j])
    return graph


def get_graph_C(routes):
    graph = nx.Graph()
    graph.add_nodes_from([route['name'] for route in routes])
    for i in range(len(routes)):
        for j in range(i + 1, len(routes)):
            if (len(intersection(routes[i]['stopes'],
                                 routes[j]['stopes'])
                    ) > 0):
                graph.add_edge(routes[i]['name'], routes[j]['name'])
    return graph


def stopes_correction():
    routes = load_json(routes_detailed_path)
    for route in routes:
        if ('stopes' not in route):
            continue
        route['stopes'] = [stop.strip()
                               .lower()
                               .replace(";", "")
                               .replace(")", "")
                           for stop in route['stopes']]
    routes2 = [route for route in routes if 'stopes' in route]
    routes = routes2
    save_json(routes, routes_detailed_path)


if __name__ == "__main__":
    sure_folder_exists(files_folder)
    sure_folder_exists(route_pages_folder)

    # page = get_or_load_page(catalog_url, catalog_page_path)
    # routes = get_routes(page)
    # save_json(routes, routes_href_path)

    routes = load_json(routes_href_path)
    routes = get_routes_detail(routes)
    save_json(routes, routes_detailed_path)

    # routes = load_json(routes_detailed_path)
    graphL = get_graph_L(routes)
    save_graph_csv(graphL, graph_l_path)
    graphP = get_graph_P(routes)
    save_graph_csv(graphP, graph_p_path)
    graphC = get_graph_C(routes)
    save_graph_csv(graphC, graph_c_path)
    # nx.draw(graph)
    # plt.show()
