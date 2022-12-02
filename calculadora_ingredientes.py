import pandas as pd
import re

def extract():
    df_order_details = pd.read_csv('order_details.csv',sep=',',encoding='LATIN_1')
    df_pizzas = pd.read_csv('pizzas.csv',sep=',',encoding='LATIN_1')
    df_types = pd.read_csv('pizza_types.csv',sep=',',encoding='LATIN_1')
    return df_order_details, df_pizzas, df_types

    #Se extraen los csv con los pedidos, pizzas e ingredientes.

def transform(df_order_details,df_pizzas,df_types):
    cantidad_pizzas_anuales = 0
    for order in range(len(df_order_details)):
        fila = df_order_details.iloc[order]                        
        cantidad_pizzas_anuales += int(fila['quantity'])
    
    cantidad_pizzas_semanales = cantidad_pizzas_anuales // 52       

    #Se calcula el número de pizzas semanales sumando fila por fila las pizzas
    #pedidas en un año (order_details.csv) y dividiendo por las 52 semanas del año. 
    
    pedidos_semanales = pd.DataFrame(columns=['Nombre de la pizza','Número de pizzas'])
    for order in range(cantidad_pizzas_semanales):
        numero_pizzas = df_order_details.loc[order,'quantity']
        pizza_id = df_order_details.loc[order,'pizza_id']

        for j in range(len(df_pizzas.axes[0])):
            fila = df_pizzas.iloc[j]
            if re.search(pizza_id,str(fila),re.IGNORECASE):     #cambiar nombre pizzas
                nombre_pizza = fila['pizza_type_id']
                size = fila['size']
                if size == "L":                             #Dos porciones estándar
                    porciones = 2
                elif size == "M":                           #Una porción estándar
                    porciones = 1
                else:
                    porciones = 0.5                         #La mitad una porción estándar



        #Crear dataframe con los datos de los pedidos semanales
        try:
            
            if len(pedidos_semanales) == 0:                                             
                pedidos_semanales.loc[0] = (nombre_pizza, porciones*numero_pizzas)

            else: 
                nuevo_pedido = False                                                  
                for pedido in range(len(pedidos_semanales)):
                    fila = pedidos_semanales.iloc[pedido]

                    if re.search(nombre_pizza, str(fila)):

                        sumar_pedido = fila['Número de pizzas'] + porciones*numero_pizzas
                        pedidos_semanales.loc[pedido,'Número de pizzas'] = sumar_pedido
                        nuevo_pedido = True
                        break                                                          

                if nuevo_pedido == False:
                    pedidos_semanales.loc[len(pedidos_semanales)] = (nombre_pizza,porciones*numero_pizzas)
        except:
            pass

    print(pedidos_semanales)

    #Hacer dataframe con los ingredientes que hay que pedir --> pizzas semanales + ingredientes de cada pizza

    pedido_ingredientes = pd.DataFrame(columns=['Ingrediente','Porciones'])
    for pedido in range(len(pedidos_semanales)):                                
        nombre_pizza = pedidos_semanales.loc[pedido,'Nombre de la pizza']
        ingredientes_pizza = []                                            #Recorre la primera semana de pedidos
        lista = []
        for i in range(len(df_types.axes[0])):
            row = df_types.iloc[i]                                        #Recorre cada tipo de pizza hasta que encuentra la pizza
            
            if re.search(str(nombre_pizza),str(row),re.IGNORECASE) != None:  
                ingredientes_pizza = str(fila['ingredients'])                
                lista = ingredientes_pizza.split(",")                       #Separa los ingredientes por comas
                print(ingredientes_pizza)
        print(lista)
        
        for ingrediente in lista:
            if len(pedido_ingredientes) == 0:
                pedido_ingredientes.loc[0] = (ingrediente,pedidos_semanales.loc[pedido,'Número de pizzas'])
            else:
                nuevo_ingrediente = True
                for j in range(len(pedido_ingredientes)):
                    nuevo_ingrediente = True
                    fila = pedido_ingredientes.iloc[j]                 
                    if re.search(ingrediente,str(fila)):
                        anterior = fila['Porciones']
                        new = anterior + pedidos_semanales.loc[pedido,'Número de pizzas']
                        pedido_ingredientes.loc[j,'Porciones'] = new
                        nuevo_ingrediente = False
                        break

                if nuevo_ingrediente == True:
                    pedido_ingredientes.loc[len(pedido_ingredientes)] = (ingrediente,pedidos_semanales.loc[pedido,'Número de pizzas'])

            print(pedido_ingredientes)
    print(pedido_ingredientes)
    return pedido_ingredientes


def load(data):
    print(data)
    data.to_csv('pedido_semanal_ingredientes.csv')
                    

if __name__ == "__main__":

    df_order_details, df_pizzas, df_types = extract()
    data = transform(df_order_details, df_pizzas, df_types)
    load(data)

