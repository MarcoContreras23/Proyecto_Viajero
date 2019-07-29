from Model.Graph import Graph
import json
from Model.Transport import Transport
from Model.Vertex import Vertex
from Model.Jobs import Jobs
from Model.ThingsDo import ThingsDo
from Model.Conection import Conection
from View.GUI import GUI
from math import inf

class Main:
    if __name__ == '__main__':
        graph = Graph()
        with open('..//Resource//p.json') as f:
            data = json.load(f)

        for transpor in data['transportForm']:
            id = transpor['id']
            name = transpor['name']
            value = transpor['valueByKm']
            time = transpor['timeByKm']
            transpor = Transport(id,name,value,time)
            graph.transport.append(transpor)
            print(graph.transport)

        for places in data['places']:
            label = places['label']
            name = places['name']
            timeHere = places['minTimeHere']
            posx = places['posx']
            posy = places['posy']
            place = Vertex(label,name,timeHere,posx,posy)
            graph.place.append(place)

            for jobs  in places['jobs']:
                name2 = jobs['name']
                gain = jobs['gain']
                time2 =  jobs['time']
                job = Jobs(name2,gain,time2)
                place.jobs.append(job)

            for do in places['things_to_do']:
                name3 = do['name']
                cost = do['cost']
                time3 = do['time']
                type = do['type']
                Things = ThingsDo(name3,cost,time3,type)
                place.task.append(Things)

        for place in data['places']:
            for go in place["goingTo"]:
                origin = graph.search_node(place['label'])
                destiny = graph.search_node(go["label"])
                distance = go["travelDistance"]
                transport = go["transportForms"]
                conection = Conection(origin,destiny,distance, origin.x, origin.y)
                origin.adjacencies.append(conection)
                graph.conection.append(conection)

        #graph.Dijkstra()
        gui =GUI(graph)
