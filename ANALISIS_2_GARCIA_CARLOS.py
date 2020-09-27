import csv
#menú de selección retornando valor elegido
def fbuscar():
    print("1.- Exportaciones ")
    print("2.- Importaciones ")
    print("3.- Exporaciones e importaciones ")
    print("4.- Salir")
    accion= input("Ingrese opción deseada: ")
    return accion


#Trabajando el archivo para conseguir una lista con los medios de transporte que se utilizan
with open("synergy_logistics_database.csv", "r") as archivo:
    lector= csv.reader(archivo)
    Lista_Transportes=[]#nombre del tranporte
    for i in lector:
        if i[7] not in Lista_Transportes:#si el transporte no esta en la lista, agregarlo
            Lista_Transportes.append(i[7])
    Lista_Transportes.pop(0)#Eliminando encabezados del csv    
#Creando lista con las rutas
with open("synergy_logistics_database.csv", "r") as archivo:
    lector= csv.reader(archivo)
    Lista_rutas_export=[]
    Lista_rutas_import=[]
    for i in lector:
        if i[1]=="Exports":
            if [i[2],i[3]] not in Lista_rutas_export:
                Lista_rutas_export.append([i[2],i[3]])
        if i[1]=="Imports":
            if [i[2],i[3]] not in Lista_rutas_import:
                Lista_rutas_import.append([i[2],i[3]])


with open("synergy_logistics_database.csv", "r") as archivo:
    lector= csv.reader(archivo)
    Lista_paises=[]
    for pais in lector:
        if pais[2] not in Lista_paises:
            Lista_paises.append(pais[2])
    Lista_paises.pop(0)
    

#se crea una lista con el contenido del csv para poder trabajarlo
with open("synergy_logistics_database.csv", "r") as archivo:
    lector= csv.reader(archivo)
    datos= list(lector)

    
#funcion contador valor por paises
def valor_pais():
    pais_total=[]
    acumPais=0
    for pais in Lista_paises:
        for buscar in datos:
            if pais==buscar[2]:
                acumPais+=int(buscar[9])
        pais_total.append([pais,acumPais])
        acumPais=0
    pais_total.sort(reverse=True, key= lambda x:x[1])
    return pais_total
#calculando el porcentaje
def porcentaje():
    Lista_porc=[]
    total=0
    Total_IyE=0
    for i in valor_pais():
        Total_IyE+=i[1]
    for total_porc in valor_pais():
        total+=total_porc[1]
        if total>Total_IyE*.8:
            break
        Lista_porc.append(total_porc)
    return Lista_porc


    
    
#contando medios de transporte
def contar_medios():
    medios_lista=[]
    cont_medios=0
    for medio in Lista_Transportes:
            for buscar in datos:
                if medio==buscar[7]:#direction determina si mostrar exportaciones,importaciones o ambas
                    cont_medios+=1
            medios_lista.append([medio, cont_medios])
            medios_lista.sort(reverse=True, key= lambda x:x[1])
            cont_medios=0
    return medios_lista
#funcion para contar rutas de importaciones
def contar_rutas_export():
    demanda_ruta=[]
    cont_ruta=0
    for ruta in Lista_rutas_export:
        for buscar in datos:
            if buscar[1]=="Exports":
                if ruta==[buscar[2],buscar[3]]:
                   cont_ruta+=1
        demanda_ruta.append([ruta,cont_ruta])
        cont_ruta=0
    demanda_ruta.sort(reverse=True, key= lambda x:x[1])
    return demanda_ruta
#funcion para contar rutas de importaciones
def contar_rutas_import():
    demanda_ruta=[]
    cont_ruta=0
    for ruta in Lista_rutas_export:
        for buscar in datos:
            if buscar[1]=="Imports":
                if ruta==[buscar[2],buscar[3]]:
                   cont_ruta+=1
        demanda_ruta.append([ruta,cont_ruta])
        cont_ruta=0
    demanda_ruta.sort(reverse=True, key= lambda x:x[1])
    return demanda_ruta        
#total exportaciones  e importaciones
def total_export_import():
    lista_resumen=[]#[[nombre_transporte, total exportación e importacion]]
    acum=0 #acumulador de valor
    for medio in Lista_Transportes:#iteracion en la lista transportes
        for buscar in datos:#iteracion en la lista datos
            if medio==buscar[7]: #si el primero medio es igual al indice 7 de la lista buscar
                acum+=int(buscar[9]) #el acumulador aumenta según el valor de buscar en el indice 9
        lista_resumen.append([medio, acum]) #agregar a la lista los valores del medio y el total de su acumulación
        lista_resumen.sort(reverse=True, key= lambda x:x[1])#ordenar de mayor a menor
        acum=0#reiniciar el acumulador
    
    return lista_resumen#retornar el valor de lista_resumen

#mismo funcionamiento que total_export
def transporte_utilizado():
    lista_resumen=[]
    cont=0
    direction=""#direction vacio como default
    inp=fbuscar()
    if inp=="1":#usando if para determinar segun el menu que valores mostrar
        print("\n VALOR TOTAL DE Exportaciones \n")
        direction="Exports"
    if inp=="2":
        print("\n VALOR TOTAL DE Importaciones \n")
        direction="Imports"
    if inp=="3":
        print("\n VALOR TOTAL DE Exportaciones e importaciones \n")
        lista_resumen=total_export_import()
    if inp=="4":
        print("Bye!")
    if direction != "":      
        for medio in Lista_Transportes:
            for buscar in datos:
                if medio==buscar[7] and buscar[1]==direction:#direction determina si mostrar exportaciones,importaciones o ambas
                    cont+=int(buscar[9])
            lista_resumen.append([medio, cont])
            lista_resumen.sort(reverse=True, key= lambda x:x[1])
            cont=0
    
    return lista_resumen


print("MEDIOS  DE TRANSPORTE \n")     
for i in transporte_utilizado():
    print("Medio de transporte: ", i[0], " Valor: ",i[1] )
    
    
print("\n DATOS DE USO DE CADA MEDIO DE TRANSPORTE")   
for cant_medios in contar_medios():
    print("Medio de transporte: ", cant_medios[0], "Veces utilizado: ", cant_medios[1])

print("\n  TOP 10 RUTAS EXPORTACIONES ")
cnt=1
for i in contar_rutas_export():
    print("Top ",cnt," RUTA  " , i[0], "veces utilizada ", i[1] )
    cnt+=1
    if cnt==11:
        break
print("\n  TOP 10 RUTAS IMPORTACIONES ")
cnt=1
for i in contar_rutas_import():
    print("Top ",cnt," RUTA  " , i[0], "veces utilizada ", i[1] )
    cnt+=1
    if cnt==11:
        break
print("\n Paises que aportan el 80% de ingresos")

for i in porcentaje():
    print("País ", i[0], "Valor ", i[1])

            
    
    
    



    
            
    
    
        
        
            
