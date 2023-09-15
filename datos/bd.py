import sqlite3

def crear_bd():
    """
    Descripción de la función:
    
    La funcion crea la base de datos llamada taller_bicicletas, se crea la tabla de la base de datos con sus campos.
    Se lleva a cabo la conexion con commit y luego cierra la base de datos.
    Todo se encierra en un try/except para manejar cualquier posible error.

    Se maneja el errror, si la tabla existe ya existe, con except sqlite3.OperationalError, 
    donde dara un mensaje de que la tabla ya existe.
    De la otra manera, un mensaje donde dice que la tabla se ha creado correctamente
    """
    try:
        conexion = sqlite3.connect('taller_bicicletas.db')
        cursor = conexion.cursor()      
      
        cursor.execute('''CREATE TABLE IF NOT EXISTS registro (
                            n_orden TEXT NOT NULL PRIMARY KEY AUTOINCREMENT,
                            fecha TEXT NOT NULL,
                            cliente TEXT NOT NULL,
                            email TEXT,
                            telefono INT NOT NULL,
                            dni TEXT,
                            vehiculo TEXT NOT NULL,
                            modelo TEXT NOT NULL,
                            status TEXT NOT NULL,
                            trabajo TEXT NOT NULL,
                            observaciones TEXT
                        )''')
        
        conexion.commit()
        conexion.close()
        print("La tabla se ha creado correctamente!")
    except sqlite3.OperationalError:
        print("La tabla ya existe!!!")

