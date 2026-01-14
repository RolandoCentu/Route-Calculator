import os
import heapq
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
        linea = "".join(c for c in fila)
        print(linea)

def encontrar(mapa, simbolo):
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

def es_impasable(valor):
    return valor in (BORDE, EDIFICIO, BLOQUEADO)

def vecinos(f,c):
    return [(f-1,c),(f+1,c),(f,c-1),(f,c+1)]

def heuristica(a,b):
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

    abiertos = []
    g_score = {inicio:0}
    f_score = {inicio:heuristica(inicio,meta)}
    predecesor = {}
    cerrados = set()
    heapq.heappush(abiertos,(f_score[inicio],0,inicio))

    while abiertos:
        _,g_actual,actual = heapq.heappop(abiertos)
        if actual in cerrados: continue
        cerrados.add(actual)

        # Mostrar exploración paso a paso
        af,ac = actual
        if (af,ac) not in (inicio,meta):
            mapa[af][ac] = VISITADO
        imprimir_mapa(mapa)
        time.sleep(0.05)   # pausa para animación

        if actual == meta:
            camino = reconstruir_camino(predecesor,inicio,meta)
            limpiar_camino(mapa)
            for (fi,ci) in camino:
                if (fi,ci) not in (inicio,meta):
                    mapa[fi][ci] = CAMINO
            imprimir_mapa(mapa)
            return True,f"Camino encontrado con {len(camino)-1} pasos"
        
        for nf,nc in vecinos(af,ac):
            if not (0<=nf<len(mapa) and 0<=nc<len(mapa[0])): continue
            celda = mapa[nf][nc]
            if es_impasable(celda) and (nf,nc)!=meta: continue
            costo = COSTO.get(celda,1)
            tentative_g = g_actual + costo
            if tentative_g < g_score.get((nf,nc),float("inf")):
                predecesor[(nf,nc)] = actual
                g_score[(nf,nc)] = tentative_g
                f_total = tentative_g + heuristica((nf,nc),meta)
                f_score[(nf,nc)] = f_total
                heapq.heappush(abiertos,(f_total,tentative_g,(nf,nc)))
    return False,"No hay camino disponible"

def meta_final(mapa,simbolo,fila,columna):
    limpiar_camino(mapa)
    anterior = encontrar(mapa,simbolo)
    if anterior:
        ai,aj = anterior
        mapa[ai][aj] = CELDA_VACIA
    mapa[fila][columna] = simbolo

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

if __name__=="__main__":
    main()
