import os
import heapq # para convertir una lista en una cola de prioridad
import time

#Designo emojis para diferenciar 
BORDE       = "🟫"
CELDA_VACIA = "⬜"
AGUA        = "🌊"
EDIFICIO    = "🏢"
BLOQUEADO   = "⛔"
INICIO      = "🚩"
META        = "🏁"
CAMINO      = "🟢"
VISITADO    = "👣"

#costo de movimiento
COSTO ={
    CELDA_VACIA: 1,
    AGUA: 3,
}

def crear_mapa(filas, columnas):
    mapa = []
    for i in range(filas):
        fila =[]
        for j in range(columnas):
            if i == 0 or i == filas-1 or j == 0 or j==columnas-1:
                fila.append(BORDE)
            else:
                fila.append(CELDA_VACIA)
        mapa.append(fila)
    return mapa
def imprimir_mapa(mapa):
    os.system("cls" if os.name == "nt" else "clear")
    
    for fila in mapa:
        print("".join(fila))


def encontrar(mapa, simbolo):  #busca simbolo y devuelve coordenadas
    for i, fila in enumerate(mapa):
        for j, val in enumerate(fila):
            if val == simbolo:
                return (i,j)
    return None

def limpiar_camino(mapa):
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if mapa[i][j] in (CAMINO, VISITADO):
                mapa[i][j] = CELDA_VACIA

def es_impasable(valor): #devuelve true si la celda es obstaculo
    return valor in (BORDE, EDIFICIO, BLOQUEADO)

def vecinos(f,c): #coordenadas arriba,abajo,izquierda, derecha
    return [(f-1,c),(f+1,c),(f,c-1),(f,c+1)]

def heuristica(a,b): #distancia manhattan
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def reconstruir_camino(predecesor,inicio,meta):
    nodo = meta
    camino = []
    while nodo != inicio:
        camino.append(nodo)
        nodo = predecesor.get(nodo)
        if nodo is None:
            return []
    camino.append(inicio)
    camino.reverse()
    return camino

def a_estrella(mapa):
    inicio = encontrar(mapa, INICIO)
    meta   = encontrar(mapa, META)
    if not inicio or not meta:
        return False,"Falta inicio 🚩 o meta 🏁"
    si,sj = inicio
    mi,mj = meta
    if es_impasable(mapa[si][sj]):
        return False,"Inicio sobre obstáculo"
    if es_impasable(mapa[mi][mj]):
        return False,"Meta sobre obstáculo"
        
    #f(n) = g(n) + h(n)
    abiertos = [] #lista de nodos abiertos a explorar
    g_score = {inicio:0}  #g costo real acumulado dede in inicio hasta un nodo especifico
    f_score = {inicio:heuristica(inicio,meta)} # f es la suma de ambos valores
    predecesor = {} #diccionario para guardar predecesor
    cerrados = set() #conjunto para nodos explorados
    heapq.heappush(abiertos,(f_score[inicio],0,inicio)) #para anadir un elemnto a la lista

    while abiertos:
        _,g_actual,actual = heapq.heappop(abiertos) #se extrae el nodo con menor fscore
        if actual in cerrados: 
            continue  # para pasar si es true o agregar a cerrados
        cerrados.add(actual)

        # Mostrar exploración paso a paso
        af,ac = actual
        if (af,ac) not in (inicio,meta):
            mapa[af][ac] = VISITADO
        imprimir_mapa(mapa)
        time.sleep(0.05)   # pausa para animación
        #Fuera del if → animación fluida, siempre ves el mapa actualizado.
        #Dentro del if → animación parcial, solo ves cambios cuando se marcan celdas como
        
        if actual == meta:   # si nodo es la meta se reconstruye el camino con predecesores
            camino = reconstruir_camino(predecesor,inicio,meta)
            limpiar_camino(mapa)
            for (fi,ci) in camino:
                if (fi,ci) not in (inicio,meta):
                    mapa[fi][ci] = CAMINO
            imprimir_mapa(mapa)
            return True,f"Camino encontrado con {len(camino)-1} pasos"
        
        for nf,nc in vecinos(af,ac): # si no es la meta, se exploran los vecinos
            if not ( 0 <= nf<len(mapa) and 0 <= nc <len(mapa[0])): #validar que este dentro del mapa
                continue
            celda = mapa[nf][nc]  # si la celda es un impasable no se puede pasar
            if es_impasable(celda) and (nf,nc) != meta: #solo si es meta  
                continue
            costo = COSTO.get(celda,1) #calcular costos
            tentative_g = g_actual + costo #costo acumulado desde el inicio hasta ese vecino
            
            if tentative_g < g_score.get((nf,nc),float("inf")): # se compara, si el nuevo costo es menor, entonces se actualizan 
                predecesor[(nf,nc)] = actual
                g_score[(nf,nc)] = tentative_g #se actualiza valores de g y f
                f_total = tentative_g + heuristica((nf,nc),meta) #combina costo real y heuristica
                f_score[(nf,nc)] = f_total
                heapq.heappush(abiertos,(f_total,tentative_g,(nf,nc))) # se anhade a abierto
    return False,"No hay camino disponible"

def meta_final(mapa,simbolo,fila,columna): #para recalcular un nuevo camino cambiando inicio y fin y que no se dupliquen
    limpiar_camino(mapa)
    anterior = encontrar(mapa,simbolo) #busca inicio y meta en tiempo real
    if anterior:
        ai,aj = anterior
        mapa[ai][aj] = CELDA_VACIA #reemplaza para que quede limpio
    mapa[fila][columna] = simbolo #nueva pos para ini o meta

def desbloquear_zonas(mapa):
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if mapa[i][j] == BLOQUEADO:
                mapa[i][j] = CELDA_VACIA

def main():
    filas = int(input("Filas: "))
    columnas = int(input("Columnas: "))
    mapa = crear_mapa(filas,columnas)
    while True:
        imprimir_mapa(mapa)
        print("\nOpciones:")
        print("1) 🌊 Agua")
        print("2) 🏢 Edificio")
        print("3) ⛔ Zona bloqueada temporal")
        print("4) 🚩 Inicio")
        print("5) 🏁 Meta")
        print("6) Borrar")
        print("7) Calcular Camino")
        print("8) Desbloquear zonas ⛔")
        print("9) Salir")
        opcion = input("Elige: ").strip()
        if opcion=="9": break
        elif opcion=="1": objeto=AGUA
        elif opcion=="2": objeto=EDIFICIO
        elif opcion=="3": objeto=BLOQUEADO
        elif opcion=="4": objeto=INICIO
        elif opcion=="5": objeto=META
        elif opcion=="6": objeto=CELDA_VACIA
        elif opcion=="7":
            ok,msg = a_estrella(mapa)
            imprimir_mapa(mapa)
            print(msg)
            input("Enter para volver al menu")
            continue
        elif opcion=="8":
            desbloquear_zonas(mapa)
            print("Zonas ⛔ desbloqueadas.")
            input("Enter para volver al menu")
            continue
        else:
            continue
        try:
            x=int(input(f"Fila (1 a {filas-2}): "))
            y=int(input(f"Columna (1 a {columnas-2}): "))
            if 1<=x<=filas-2 and 1<=y<=columnas-2:
                if objeto in (INICIO,META):
                    if es_impasable(mapa[x][y]):
                        print("No puedes colocar inicio/meta sobre obstáculo")
                        input("Enter para volver al menu")
                        continue
                    meta_final(mapa,objeto,x,y)
                else:
                    limpiar_camino(mapa)
                    mapa[x][y]=objeto
        except: pass

main()
