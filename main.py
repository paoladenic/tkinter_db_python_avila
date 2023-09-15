from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datos.bd import crear_bd
from tkcalendar import DateEntry


class Registros:
    """
    Descripción de la Clase:
    
    La clase Registros contiene las funcionalidades de los botones de la pantalla del Main.
    nuevo_registro
    buscar_registro
    editar_registro
    eliminar_registro
    informe

    Luego esta clase es llamada en los botones del main para acceder a cada una de las funconalidades del menu

    """
    def nuevo_registro():
        """
        Descripción de la Funcion:
        
        La funcion nuevo_registro, crea la interfaz grafica para solicitar los datos al usuario e ingresarlos en la base de datos.
        Estos registros se almacenan en la base de datos al clickar el boton de guardar.
        Con el Menu, ubicado en la parte superior de la ventana, se puede salir de la pantalla.

        """
        ventana_nuevo = Toplevel(ventana_principal) #redirige de la ventana del main
        ventana_nuevo.title('Gestión del Taller de AVILA BIKES')
        ventana_nuevo.attributes("-fullscreen", True)
        label = Label(ventana_nuevo, text= 'Gestión del Taller de AVILA BIKES', background="orange", justify= "center", fg="black", pady=10, font=("Arial, 16")).pack()
        label = Label(ventana_nuevo, text= '', background="orange").pack() #espacio

        menubar = Menu(ventana_nuevo)
        ventana_nuevo.config(menu = menubar, background="orange")   
        filemenu = Menu(menubar, tearoff = 0)
        filemenu.add_separator()
        filemenu.add_command(label='Volver al menú', command = ventana_nuevo.destroy, font=("Arial, 12")) #sale de la ventana abierta con destroy
        menubar.add_cascade(label = 'Opciones', menu = filemenu)

        label = Label(ventana_nuevo, text="----- RECEPCION DE NUEVO VEHICULO -----", fg="yellow", background="black", font=("Arial, 12"), pady=10, padx=70).pack()
        label = Label(ventana_nuevo, text= '', background="orange").pack()

        frame = Frame(ventana_nuevo) #se hace un frame para colocar en el las entradas de texto
        frame.config(bg='white', padx=150)
        frame.pack(fill = 'y')

        a = Label(frame, text = "Numero de orden*: ", fg="red", background= "white", font=("Arial, 11")).grid(row = 0,column = 0, padx=80, pady=30)
        a1 = Entry(frame) #campo de entrada de texto
        a1.grid(row = 0,column = 1) #matriz de posicion: fila y columna

        b = Label(frame ,text = "Fecha de recepcion*: ", fg="red", background= "white", font=("Arial, 11")).grid(row = 0,column = 2, padx=80, pady=30)
        b1 = DateEntry(frame, selectmode = 'day')
        b1.grid(row = 0,column = 3)

        #titulos de division 
        c = Label(frame ,text = "Datos del Cliente", fg="yellow", background= "black", font=("Arial, 11")).grid(row = 2,column = 0)
        d = Label(frame ,text = "Datos del Vehiculo", fg="yellow", background= "black", font=("Arial, 11")).grid(row = 2,column = 2)

        e = Label(frame ,text = "Nombre y Apellido/Razon Social*: ", fg="black", background= "white", font=("Arial, 11")).grid(row = 3,column = 0)
        e1 = Entry(frame)
        e1.grid(row = 3,column = 1)
        g = Label(frame ,text = "Email: ", fg="black", background= "white", font=("Arial, 11")).grid(row = 4,column = 0)
        g1 = Entry(frame)
        g1.grid(row = 4,column = 1)
        h = Label(frame ,text = "Telefono*: ", fg="black", background= "white", font=("Arial, 11")).grid(row = 5,column = 0)
        h1 = Entry(frame)
        h1.grid(row = 5,column = 1)
        i = Label(frame ,text = "NIF/NIE: ", fg="black", background= "white", font=("Arial, 11")).grid(row = 6,column = 0)
        i1 = Entry(frame)
        i1.grid(row = 6,column = 1)
        n = Label(frame ,text = "", background= "white", font=("Arial, 11")).grid(row = 7,column = 0)

        j = Label(frame, text = "Tipo de Vehiculo*: ", fg="black", background= "white", font=("Arial, 11")).grid(row = 3,column = 2)
        j1 = ttk.Combobox(frame, state="readonly", values=["Bicicleta", "Patinete", "Silla de Rueda", "Otro"])
        j1.grid(row = 3,column = 3)
        k = Label(frame, text = "Marca/Modelo*: ", fg="black", background= "white", font=("Arial, 11")).grid(row = 4,column = 2)
        k1 = Entry(frame)
        k1.grid(row = 4,column = 3)
        l = Label(frame, text = "Status*: ", fg="black", background= "white", font=("Arial, 11")).grid(row =6,column = 2)
        l1 = ttk.Combobox(frame, state="readonly", values=["Sin comenzar", "En Proceso", "Listo y Sin Retirar", "Retirado", "Cotizacion"])
        l1.grid(row = 6,column = 3)
        
        #cuadro de texto 
        label = Label(ventana_nuevo, text="---- Trabajo a realizar ----", fg="black", background="orange", font=("Arial, 12"), pady=10).pack()
        texto1 = Text(ventana_nuevo, width = 100, height = 8)
        texto1.pack()
        texto1.config(font=('Arial', 9),
                    border=8,
                    padx=5,
                    pady=5)

        label = Label(ventana_nuevo, text= '', background="orange").pack()

        label = Label(ventana_nuevo, text="---- Observaciones ----", fg="black", background="orange", font=("Arial, 12"), pady=10).pack()
        texto2 = Text(ventana_nuevo, width = 100, height = 8)
        texto2.pack()
        texto2.config(font=('Arial', 9),
                    border=8,
                    padx=5,
                    pady=5)
        
        #funcion que llama a la base de datos
        def guardar():
            """
            Descripción de la función:
            
            La funcion se conecta con la base de datos existente.
            con el metodo get, se obtiene los valores de los campos Entry de la interfaz grafica
            El If determina los campos que son obligatorios para poder prodecer, y si todos son rellenados, los introduce en la base de datos.

            Todo se encierra en un try/except para manejar el error.
            Se insertan los registros en la tabla. Se lleva a cabo la peticion con commit.
            con el metodo destroy, se sale de la ventana.
            Si falta completar algun registro, saltara un mensaje emergente indicando el error.

            todo esto se completa con el boton guardar que esta fuera de la funcion y pertenece al codigo de la interfaz grafica.

            """
            conexion = sqlite3.connect('taller_bicicletas.db')
            cursor = conexion.cursor()

            #se obtiene el valor del campo Entry con .get()
            n_orden = a1.get()
            fecha = b1.get()
            cliente = e1.get()
            email = g1.get()
            telefono = h1.get()
            dni = i1.get()
            vehiculo = j1.get()
            modelo = k1.get()
            status = l1.get()
            trabajo = texto1.get('1.0', 'end-1c')
            observaciones = texto2.get('1.0', 'end-1c')

            #este if determina los campos que son obligatorios para poder prodecer
            if n_orden and fecha and cliente and telefono and vehiculo and modelo and status and trabajo:
                try: #inserta los valores en la base de datos
                    cursor.execute("INSERT INTO registro VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (n_orden, fecha, cliente, email, telefono, dni, vehiculo, modelo, status, trabajo, observaciones))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Registro agregado correctamente.") #muestra el mesaje popup luego de haber realizado la accion
                    # ventana_nuevo.destroy() #sale de la ventana
                except:
                    messagebox.showerror("Error", "Por favor, completa todos los campos.")
            else:
                messagebox.showerror("Error", "Por favor, completa todos los campos.")

        #boton que al clickarlo referencia a la funcion guardar
        label = Label(ventana_nuevo, text= '', background="orange").pack()
        button = Button(ventana_nuevo, text = 'Guardar', fg="yellow", background="black", font=("Arial, 12"), width= 10, height= 1, pady=10, command = guardar)
        button.pack()
        label = Label(ventana_nuevo, text= '', background="orange").pack()


    def buscar_registro():
        """
        Descripción de la Funcion:
        
        La funcion buscar_registro, crea la interfaz grafica donde pide al usuario el nombre del cliente a buscar.
        Estos registros se muestran al clickar el boton de buscar y se muestran en la ventada del Treeview.
        Con el Menu, ubicado en la parte superior de la ventana, se puede salir de la pantalla.

        """
        ventana_buscar = Toplevel(ventana_principal)
        ventana_buscar.title('Gestión del Taller de AVILA BIKES')
        ventana_buscar.attributes("-fullscreen", True)
        label = Label(ventana_buscar, text= 'Gestión del Taller de AVILA BIKES', background="orange", justify= "center", fg="black", pady=10, font=("Arial, 16")).pack()
        label = Label(ventana_buscar, text= '', background="orange").pack()

        menubar = Menu(ventana_buscar)
        ventana_buscar.config(menu = menubar, background="orange")
        filemenu = Menu(menubar, tearoff = 0)
        filemenu.add_separator()
        filemenu.add_command(label='Volver al menú', command = ventana_buscar.destroy, font=("Arial, 12"))
        menubar.add_cascade(label = 'Opciones', menu = filemenu)

        label = Label(ventana_buscar, text="----- BUSCAR UN REGISTRO -----", fg="yellow", background= "black", font=("Arial, 12"), padx=70, pady=10).pack()
        label = Label(ventana_buscar, text= '', background="orange").pack()

        frame = Frame(ventana_buscar)
        frame.config(bg='white', padx=150)
        frame.pack(fill = 'y', anchor="center")

        a = Label(frame, text = "¿Qué quieres buscar?: ", fg="red", background= "white", font=("Arial, 12"))
        a.grid(row = 0,column = 0, padx=80, pady=30)
        a1 = Entry(frame, width= 40)
        a1.grid(row = 0,column = 1)

        def buscar():
            """
            Descripción de la función:
            
            La funcion se conecta con la base de datos.
            Todo se encierra en un try/except para manejar cualquier posible error.
            se obtiene la palabra_clave buscada con el metodo get.

            Se seleccionan todos los registros de la tabla registro con el SELECT * WHERE LIKE,
            el metodo get_children, nos permite eliminar algun registro viejo que tenga el Treeview.
            luego con el FOR, recorre estos registros, para finalmente insertarlos en el Treeview
            Se lleva a cabo la peticion con commit

            Se maneja el errror, si no hay registros para mostar, saltara un mensaje emergente indicando el error.

            """
            conexion = sqlite3.connect('taller_bicicletas.db')
            cursor = conexion.cursor()

            palabra_clave = a1.get().strip()
            try: 
                cursor.execute("SELECT * FROM registro WHERE n_orden LIKE ? OR fecha LIKE ? OR cliente LIKE ? OR email LIKE ? OR telefono LIKE ? OR dni LIKE ? OR vehiculo LIKE ? OR modelo LIKE ? OR status LIKE ? OR trabajo LIKE ? OR observaciones LIKE ?",
                            ('%' + palabra_clave + '%', '%' + palabra_clave + '%', '%' + palabra_clave + '%', '%' + palabra_clave + '%', '%' + palabra_clave + '%', '%' + palabra_clave + '%', '%' + palabra_clave + '%', '%' + palabra_clave + '%', '%' + palabra_clave + '%', '%' + palabra_clave + '%', '%' + palabra_clave + '%'))
                resultados = cursor.fetchall()
                tabla.delete(*tabla.get_children())  # Borra los registros existentes en el Treeview antes de agregar los nuevos
                if not resultados:
                    messagebox.showinfo("Información", "No se encontraron registros que coincidan con la palabra clave.")
                else:
                    for r in resultados:
                        tabla.insert("", "end", values=r)
                conexion.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al buscar registros: {e}")
            finally:
                conexion.close()

        a2 = Button(frame, text = 'Buscar', fg="yellow", background="black", font=("Arial, 12"), width= 10, height= 1, pady=10, command= buscar)
        a2.grid(row = 0,column = 2, padx=80, pady=30)
        label = Label(ventana_buscar, text= '', background="orange").pack()

        tabla = ttk.Treeview(ventana_buscar, height=25, columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11"))
        tabla.heading("#0",text="",anchor=CENTER)
        tabla.column("#0", width=20, anchor=CENTER)
        tabla.heading("#1",text="Numero de Orden",anchor=CENTER)
        tabla.column("#1", width=120, anchor=CENTER)
        tabla.heading("#2",text="Fecha de Recepción",anchor=CENTER)
        tabla.column("#2", width=130, anchor=CENTER)
        tabla.heading("#3",text="Nombre Cliente",anchor=CENTER)
        tabla.column("#3", width=140, anchor=CENTER)
        tabla.heading("#4",text="Email Cliente",anchor=CENTER)
        tabla.column("#4", width=130, anchor=CENTER)
        tabla.heading("#5",text="Telefono Cliente",anchor=CENTER)
        tabla.column("#5", width=110, anchor=CENTER)
        tabla.heading("#6",text="DNI Cliente",anchor=CENTER)
        tabla.column("#6", width=120, anchor=CENTER)
        tabla.heading("#7",text="Tipo Vehiculo",anchor=CENTER)
        tabla.column("#7", width=110, anchor=CENTER)
        tabla.heading("#8",text="Marca/Modelo",anchor=CENTER)
        tabla.column("#8", width=120, anchor=CENTER)
        tabla.heading("#9",text="- Status -",anchor=CENTER)
        tabla.column("#9", width=130, anchor=CENTER)
        tabla.heading("#10",text="Trabajo",anchor=CENTER)
        tabla.column("#10", width=220, anchor=CENTER)
        tabla.heading("#11",text="Observaciones",anchor=CENTER)
        tabla.column("#11", width=220, anchor=CENTER)
        tabla.pack()


    def editar_registro():
        """
        Descripción de la Funcion:
        
        La funcion editar_registro, crea la interfaz grafica donde pide al usuario el nombre del cliente a editar.
        Estos registros se muestran al clickar el boton de buscar y se muestran en la ventada del Treeview.
        Se selecciona el registro a editar y al clickar el boton editar registro, se muestra la ventana del formulario para editarlo.
        Con el Menu, ubicado en la parte superior de la ventana, se puede salir de la pantalla.

        """
        def editar_buscar():
            conexion = sqlite3.connect('taller_bicicletas.db')
            cursor = conexion.cursor()
            palabra_clave = a1.get()
            try:
                cursor.execute("SELECT * FROM registro WHERE cliente LIKE ?", ("%" + palabra_clave + "%",))
                resultados = cursor.fetchall()
                tabla.delete(*tabla.get_children())
                for r in resultados:
                    tabla.insert("", "end", values=r)
                conexion.commit()
            except:
                messagebox.showerror("Error", "Registro no encontrado.")
                
        ventana_editar1 = Toplevel(ventana_principal)
        ventana_editar1.title('Gestión del Taller de AVILA BIKES')
        ventana_editar1.attributes("-fullscreen", True)
        label = Label(ventana_editar1, text='Gestión del Taller de AVILA BIKES', background="orange", justify="center", fg="black", pady=10, font=("Arial, 16"))
        label.pack()
        label = Label(ventana_editar1, text='', background="orange")
        label.pack()

        menubar = Menu(ventana_editar1)
        ventana_editar1.config(menu=menubar, background="orange")
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_separator()
        filemenu.add_command(label='Volver al menú', command=ventana_editar1.destroy, font=("Arial, 12"))
        menubar.add_cascade(label='Opciones', menu=filemenu)

        label = Label(ventana_editar1, text="----- BUSCAR UN REGISTRO PARA EDITAR -----", fg="yellow", background="black", font=("Arial, 12"), padx=70, pady=10)
        label.pack()
        label = Label(ventana_editar1, text='', background="orange")
        label.pack()

        frame = Frame(ventana_editar1)
        frame.config(bg='white', padx=150)
        frame.pack(fill='y', anchor="center")

        a = Label(frame, text="Introduce el cliente a editar: ", fg="red", background="white", font=("Arial, 12"))
        a.grid(row=0, column=0, padx=80, pady=30)
        a1 = Entry(frame, width=40)
        a1.grid(row=0, column=1)

        a2 = Button(frame, text='Buscar', fg="yellow", background="black", font=("Arial, 12"), width=10, height=1, pady=10,
                    command=editar_buscar)
        a2.grid(row=0, column=2, padx=80, pady=30)
        label = Label(ventana_editar1, text='', background="orange")
        label.pack()

        tabla = ttk.Treeview(ventana_editar1, height=25,
                            columns=("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11"))
        tabla.heading("#0", text="", anchor=CENTER)
        tabla.column("#0", width=20, anchor=CENTER)
        tabla.heading("#1", text="Numero de Orden", anchor=CENTER)
        tabla.column("#1", width=120, anchor=CENTER)
        tabla.heading("#2", text="Fecha de Recepción", anchor=CENTER)
        tabla.column("#2", width=130, anchor=CENTER)
        tabla.heading("#3", text="Nombre Cliente", anchor=CENTER)
        tabla.column("#3", width=140, anchor=CENTER)
        tabla.heading("#4", text="Email Cliente", anchor=CENTER)
        tabla.column("#4", width=130, anchor=CENTER)
        tabla.heading("#5", text="Telefono Cliente", anchor=CENTER)
        tabla.column("#5", width=110, anchor=CENTER)
        tabla.heading("#6", text="DNI Cliente", anchor=CENTER)
        tabla.column("#6", width=120, anchor=CENTER)
        tabla.heading("#7", text="Tipo Vehiculo", anchor=CENTER)
        tabla.column("#7", width=110, anchor=CENTER)
        tabla.heading("#8", text="Marca/Modelo", anchor=CENTER)
        tabla.column("#8", width=120, anchor=CENTER)
        tabla.heading("#9", text="- Status -", anchor=CENTER)
        tabla.column("#9", width=130, anchor=CENTER)
        tabla.heading("#10", text="Trabajo", anchor=CENTER)
        tabla.column("#10", width=220, anchor=CENTER)
        tabla.heading("#11", text="Observaciones", anchor=CENTER)
        tabla.column("#11", width=220, anchor=CENTER)
        tabla.pack()

        def editar_registro():
            selected_item = tabla.selection()
            if selected_item:
                item_values = tabla.item(selected_item, 'values')
                ventana_nuevo = Toplevel(ventana_editar1)
                ventana_nuevo.title('Gestión del Taller de AVILA BIKES')
                ventana_nuevo.attributes("-fullscreen", True)
                label = Label(ventana_nuevo, text='Gestión del Taller de AVILA BIKES', background="orange", justify="center", fg="black", pady=10, font=("Arial, 16"))
                label.pack()
                label = Label(ventana_nuevo, text='', background="orange")
                label.pack()

                menubar = Menu(ventana_nuevo)
                ventana_nuevo.config(menu=menubar, background="orange")
                filemenu = Menu(menubar, tearoff=0)
                filemenu.add_separator()
                filemenu.add_command(label='Volver al menú', command=ventana_nuevo.destroy, font=("Arial, 12"))
                menubar.add_cascade(label='Opciones', menu=filemenu)

                label = Label(ventana_nuevo, text="----- EDITAR EL REGISTRO DE UN VEHICULO -----", fg="yellow", background="black", font=("Arial, 12"), pady=10, padx=70)
                label.pack()
                label = Label(ventana_nuevo, text='', background="orange")
                label.pack()

                frame = Frame(ventana_nuevo)
                frame.config(bg='white', padx=150)
                frame.pack(fill='y')

                a = Label(frame, text="Numero de orden*: ", fg="red", background="white", font=("Arial, 11"))
                a.grid(row=0, column=0, padx=80, pady=30)
                a1 = Entry(frame)
                a1.grid(row=0, column=1)
                a1.insert(0, item_values[0])

                b = Label(frame, text="Fecha de recepcion*: ", fg="red", background="white", font=("Arial, 11"))
                b.grid(row=0, column=2, padx=80, pady=30)
                b1 = DateEntry(frame, selectmode='day')
                b1.grid(row=0, column=3)
                b1.set_date(item_values[1])

                c = Label(frame, text="Datos del Cliente", fg="yellow", background="black", font=("Arial, 11"))
                c.grid(row=2, column=0)
                d = Label(frame, text="Datos del Vehiculo", fg="yellow", background="black", font=("Arial, 11"))
                d.grid(row=2, column=2)

                e = Label(frame, text="Nombre y Apellido/Razon Social*: ", fg="black", background="white", font=("Arial, 11"))
                e.grid(row=3, column=0)
                e1 = Entry(frame)
                e1.grid(row=3, column=1)
                e1.insert(0, item_values[2])

                g = Label(frame, text="Email: ", fg="black", background="white", font=("Arial, 11"))
                g.grid(row=4, column=0)
                g1 = Entry(frame)
                g1.grid(row=4, column=1)
                g1.insert(0, item_values[3])

                h = Label(frame, text="Telefono*: ", fg="black", background="white", font=("Arial, 11"))
                h.grid(row=5, column=0)
                h1 = Entry(frame)
                h1.grid(row=5, column=1)
                h1.insert(0, item_values[4])

                i = Label(frame, text="ID: ", fg="black", background="white", font=("Arial, 11"))
                i.grid(row=6, column=0)
                i1 = Entry(frame)
                i1.grid(row=6, column=1)
                i1.insert(0, item_values[5])

                n = Label(frame, text="", background="white", font=("Arial, 11"))
                n.grid(row=7, column=0)

                j = Label(frame, text="Tipo de Vehiculo*: ", fg="black", background="white", font=("Arial, 11"))
                j.grid(row=3, column=2)
                j1 = ttk.Combobox(frame, state="readonly", values=["Bicicleta", "Patinete", "Silla de Rueda", "Otro"])
                j1.grid(row=3, column=3)
                j1.set(item_values[6])

                k = Label(frame, text="Marca/Modelo*: ", fg="black", background="white", font=("Arial, 11"))
                k.grid(row=4, column=2)
                k1 = Entry(frame)
                k1.grid(row=4, column=3)
                k1.insert(0, item_values[7])

                l = Label(frame, text="Status*: ", fg="black", background="white", font=("Arial, 11"))
                l.grid(row=6, column=2)
                l1 = ttk.Combobox(frame, state="readonly",
                                values=["Sin comenzar", "En Proceso", "Listo y Sin Retirar", "Retirado", "Cotizacion"])
                l1.grid(row=6, column=3)
                l1.set(item_values[8])

                label = Label(ventana_nuevo, text="---- Trabajo a realizar ----", fg="black", background="orange",
                            font=("Arial, 12"), pady=10)
                label.pack()
                texto1 = Text(ventana_nuevo, width=100, height=8)
                texto1.pack()
                texto1.config(font=('Arial', 9), border=8, padx=5, pady=5)
                texto1.insert('1.0', item_values[9])

                label = Label(ventana_nuevo, text='', background="orange")
                label.pack()

                label = Label(ventana_nuevo, text="---- Observaciones ----", fg="black", background="orange",
                            font=("Arial, 12"), pady=10)
                label.pack()
                texto2 = Text(ventana_nuevo, width=100, height=8)
                texto2.pack()
                texto2.config(font=('Arial', 9), border=8, padx=5, pady=5)
                texto2.insert('1.0', item_values[10])

                def guardar():
                    n_orden = a1.get()
                    fecha = b1.get()
                    cliente = e1.get()
                    email = g1.get()
                    telefono = h1.get()
                    dni = i1.get()
                    vehiculo = j1.get()
                    modelo = k1.get()
                    status = l1.get()
                    trabajo = texto1.get('1.0', 'end-1c')
                    observaciones = texto2.get('1.0', 'end-1c')

                    if n_orden and fecha and cliente and telefono and vehiculo and modelo and status and trabajo:
                        try:
                            conexion = sqlite3.connect('taller_bicicletas.db')
                            cursor = conexion.cursor()
                            cursor.execute(
                                "UPDATE registro SET n_orden=?, fecha=?, cliente=?, email=?, telefono=?, dni=?, vehiculo=?, modelo=?, status=?, trabajo=?, observaciones=? WHERE n_orden=?",
                                (n_orden, fecha, cliente, email, telefono, dni, vehiculo, modelo, status, trabajo,
                                observaciones, item_values[0]))
                            conexion.commit()
                            messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
                            ventana_nuevo.destroy()
                            editar_buscar()  # Actualizar la tabla después de editar
                        except:
                            messagebox.showerror("Error", "Por favor, completa todos los campos.")

                label = Label(ventana_nuevo, text='', background="orange")
                label.pack()
                button = Button(ventana_nuevo, text='Guardar', fg="yellow", background="black", font=("Arial, 12"),
                                width=10, height=1, pady=10, command=guardar)
                button.pack()
                label = Label(ventana_nuevo, text='', background="orange")
                label.pack()

        editar_boton = Button(ventana_editar1, text="Editar Registro", fg="yellow", background="black", font=("Arial, 12"), width=17, height=1, pady=10, command=editar_registro)
        editar_boton.pack()


    def eliminar_registro():
        """
        Descripción de la Funcion:
        
        La funcion eliminar_registro, crea la interfaz grafica donde pide al usuario el nombre del cliente a eliminar.
        Estos registros se muestran al clickar el boton de buscar y se muestran en la ventana del Treeview.
        Se selecciona el registro a eliminar y al clickar el boton eeliminar registro, se muestra la confirmacion para eliminar el registro.
        Con el Menu, ubicado en la parte superior de la ventana, se puede salir de la pantalla.

        """
        def eliminar_buscar():
            conexion = sqlite3.connect('taller_bicicletas.db')
            cursor = conexion.cursor()
            palabra_clave = a1.get()
            try:
                cursor.execute("SELECT * FROM registro WHERE cliente LIKE ?", ("%" + palabra_clave + "%",))
                resultados = cursor.fetchall()
                tabla.delete(*tabla.get_children())
                for r in resultados:
                    tabla.insert("", "end", values=r)
                conexion.commit()
            except:
                messagebox.showerror("Error", "Registro no encontrado.")
                
        ventana_eliminar = Toplevel(ventana_principal)
        ventana_eliminar.title('Gestión del Taller de AVILA BIKES')
        ventana_eliminar.attributes("-fullscreen", True)
        label = Label(ventana_eliminar, text='Gestión del Taller de AVILA BIKES', background="orange", justify="center", fg="black", pady=10, font=("Arial, 16"))
        label.pack()
        label = Label(ventana_eliminar, text='', background="orange")
        label.pack()

        menubar = Menu(ventana_eliminar)
        ventana_eliminar.config(menu=menubar, background="orange")
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_separator()
        filemenu.add_command(label='Volver al menú', command=ventana_eliminar.destroy, font=("Arial, 12"))
        menubar.add_cascade(label='Opciones', menu=filemenu)

        label = Label(ventana_eliminar, text="----- BUSCAR UN REGISTRO PARA ELIMINAR -----", fg="yellow", background="black", font=("Arial, 12"), padx=70, pady=10)
        label.pack()
        label = Label(ventana_eliminar, text='', background="orange")
        label.pack()

        frame = Frame(ventana_eliminar)
        frame.config(bg='white', padx=150)
        frame.pack(fill='y', anchor="center")

        a = Label(frame, text="Introduce el cliente a eliminar: ", fg="red", background="white", font=("Arial, 12"))
        a.grid(row=0, column=0, padx=80, pady=30)
        a1 = Entry(frame, width=40)
        a1.grid(row=0, column=1)

        a2 = Button(frame, text='Buscar', fg="yellow", background="black", font=("Arial, 12"), width=10, height=1, pady=10,
                    command=eliminar_buscar)
        a2.grid(row=0, column=2, padx=80, pady=30)
        label = Label(ventana_eliminar, text='', background="orange")
        label.pack()

        tabla = ttk.Treeview(ventana_eliminar, height=25,
                            columns=("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11"))
        tabla.heading("#0", text="", anchor=CENTER)
        tabla.column("#0", width=20, anchor=CENTER)
        tabla.heading("#1", text="Numero de Orden", anchor=CENTER)
        tabla.column("#1", width=120, anchor=CENTER)
        tabla.heading("#2", text="Fecha de Recepción", anchor=CENTER)
        tabla.column("#2", width=130, anchor=CENTER)
        tabla.heading("#3", text="Nombre Cliente", anchor=CENTER)
        tabla.column("#3", width=140, anchor=CENTER)
        tabla.heading("#4", text="Email Cliente", anchor=CENTER)
        tabla.column("#4", width=130, anchor=CENTER)
        tabla.heading("#5", text="Telefono Cliente", anchor=CENTER)
        tabla.column("#5", width=110, anchor=CENTER)
        tabla.heading("#6", text="DNI Cliente", anchor=CENTER)
        tabla.column("#6", width=120, anchor=CENTER)
        tabla.heading("#7", text="Tipo Vehiculo", anchor=CENTER)
        tabla.column("#7", width=110, anchor=CENTER)
        tabla.heading("#8", text="Marca/Modelo", anchor=CENTER)
        tabla.column("#8", width=120, anchor=CENTER)
        tabla.heading("#9", text="- Status -", anchor=CENTER)
        tabla.column("#9", width=130, anchor=CENTER)
        tabla.heading("#10", text="Trabajo", anchor=CENTER)
        tabla.column("#10", width=220, anchor=CENTER)
        tabla.heading("#11", text="Observaciones", anchor=CENTER)
        tabla.column("#11", width=220, anchor=CENTER)
        tabla.pack()

        def eliminar():
            seleccion = tabla.selection()
            if seleccion:
                seleccion_id = tabla.item(seleccion)['values'][0]
                respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar este registro?")
                if respuesta:
                    conexion = sqlite3.connect('taller_bicicletas.db')
                    cursor = conexion.cursor()
                    cursor.execute("DELETE FROM registro WHERE n_orden=?", (seleccion_id,))
                    conexion.commit()
                    tabla.delete(seleccion)
                    messagebox.showinfo("Eliminación exitosa", "El registro ha sido eliminado correctamente.")

        eliminar_boton = Button(ventana_eliminar, text="Eliminar Registro", fg="yellow", background="black", font=("Arial, 12"), width=17, height=1, pady=10, command=eliminar)
        eliminar_boton.pack()


    def informes():
        """
        Descripción de la Funcion:
        
        La funcion informes, crea la interfaz grafica para mostrar TODOS los registros que contiene la base de datos.
        Estos registros se muestran al clickar el boton de generar informes.
        Con el Menu, ubicado en la parte superior de la ventana, se puede salir de la pantalla.

        """
        #lo redirige de la ventana principan
        ventana_informe = Toplevel(ventana_principal)
        ventana_informe.title('Gestión del Taller de AVILA BIKES')
        ventana_informe.attributes("-fullscreen", True)
        label = Label(ventana_informe, text= 'Gestión del Taller de AVILA BIKES', background="orange", justify= "center", fg="black", pady=10, font=("Arial, 16")).pack()
        label = Label(ventana_informe, text= '', background="orange").pack() #espaciado

        #el menu de las opciones
        menubar = Menu(ventana_informe)
        ventana_informe.config(menu = menubar, background="orange")
        filemenu = Menu(menubar, tearoff = 0)
        filemenu.add_separator()
        filemenu.add_command(label='Volver al menú', command = ventana_informe.destroy, font=("Arial, 12")) #sale de la ventana con destroy
        menubar.add_cascade(label = 'Opciones', menu = filemenu)

        label = Label(ventana_informe, text="----- INFORME VEHICULOS -----", fg="yellow", background= "black", font=("Arial, 12"), padx=70, pady=10).pack()
        label = Label(ventana_informe, text= '', background="orange").pack()
        label = Label(ventana_informe, text= '', background="orange").pack()
        
        #funcion que maneja la base de datos
        def informe():
            """
            Descripción de la función:
            
            La funcion se conecta con la base de datos.
            Todo se encierra en un try/except para manejar cualquier posible error.
            Se seleccionan todos los registros de la tabla registro con el SELECT *,
            luego con el FOR, recorre estos registros, para finalmente insertarlos en el Treeview
            Se lleva a cabo la peticion con commit

            Se maneja el errror, si no hay registros para mostar, saltara un mensaje emergente indicando el error.

            """
            conexion = sqlite3.connect('taller_bicicletas.db')
            cursor = conexion.cursor()

            try: 
                cursor.execute("SELECT * FROM registro")  # Busca todos los registros existentes
                resultados = cursor.fetchall()  # Los trae todos

                tabla.delete(*tabla.get_children()) # Borra los registros existentes en el Treeview antes de agregar los nuevos

                if not resultados:
                    messagebox.showinfo("Información", "No hay registros para mostrar.")
                else:
                    for r in resultados:  # Los recorre 
                        tabla.insert("", "end", values=r)  # Los inserta en la tabla de Treeview
                conexion.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al recuperar registros: {e}")
            finally:
                conexion.close()

        a2 = Button(ventana_informe, text = 'Generar Informe', fg="black", background="yellow", font=("Arial, 12"), width= 30, height= 1, pady=10, command = informe)
        a2.pack()
        label = Label(ventana_informe, text= '', background="orange").pack()

        #tabla de visualizacion de los datos, declaracion de las columnas, el ancho, el etiquetado, la alineacion
        tabla = ttk.Treeview(ventana_informe, height=25, columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11"))
        tabla.heading("#0",text="",anchor=CENTER)
        tabla.column("#0", width=20, anchor=CENTER)
        tabla.heading("#1",text="Numero de Orden",anchor=CENTER)
        tabla.column("#1", width=120, anchor=CENTER)
        tabla.heading("#2",text="Fecha de Recepción",anchor=CENTER)
        tabla.column("#2", width=130, anchor=CENTER)
        tabla.heading("#3",text="Nombre Cliente",anchor=CENTER)
        tabla.column("#3", width=140, anchor=CENTER)
        tabla.heading("#4",text="Email Cliente",anchor=CENTER)
        tabla.column("#4", width=130, anchor=CENTER)
        tabla.heading("#5",text="Telefono Cliente",anchor=CENTER)
        tabla.column("#5", width=110, anchor=CENTER)
        tabla.heading("#6",text="DNI Cliente",anchor=CENTER)
        tabla.column("#6", width=120, anchor=CENTER)
        tabla.heading("#7",text="Tipo Vehiculo",anchor=CENTER)
        tabla.column("#7", width=110, anchor=CENTER)
        tabla.heading("#8",text="Marca/Modelo",anchor=CENTER)
        tabla.column("#8", width=120, anchor=CENTER)
        tabla.heading("#9",text="- Status -",anchor=CENTER)
        tabla.column("#9", width=130, anchor=CENTER)
        tabla.heading("#10",text="Trabajo",anchor=CENTER)
        tabla.column("#10", width=220, anchor=CENTER)
        tabla.heading("#11",text="Observaciones",anchor=CENTER)
        tabla.column("#11", width=220, anchor=CENTER)
        tabla.pack()

#se llama a la funcion de crear la base de batos
crear_bd()

#se crea la interfaz grafica
ventana_principal = Tk()
ventana_principal.title('Gestión del Taller de AVILA BIKES') #titulo del documento
ventana_principal.attributes("-fullscreen", True) #que la pantalla sea pantalla completa
label = Label(ventana_principal, text= 'Gestión del Taller de AVILA BIKES', background="orange", justify= "center", fg="black", pady=10, font=("Arial, 16")).pack()

#el menu que nos dara opciones en la barra superior
menubar = Menu(ventana_principal) #se aloja en ventana principal
ventana_principal.config(menu = menubar, background="orange")
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_separator()
filemenu.add_command(label='Salir del Programa', command = ventana_principal.destroy, font=("Arial, 12")) #con destroy se sale del programa, ya que se eelimina la pantalla
menubar.add_cascade(label = 'Salir', menu = filemenu)

#coloco un frame para poner los botones y la foto
frame = Frame(ventana_principal)
frame.config(bg='white', padx=200, pady=40)
frame.pack(fill = 'both')

#se coloca la imagen
logo = PhotoImage(file="logo.png")
logo = logo.subsample(6) #se reduce el tamaño de la imagen
logo1 = Label(frame, image=logo) #alojamiento de la imagen 
logo1.pack(side = 'top', anchor = 'center') #posicion

#botones que llaman a las funciones por la clase Registros
boton_agregar = Button(frame, text = 'Nuevo Registro', command = Registros.nuevo_registro, font=("Arial, 12"), width= 15, height= 1).pack(side = 'top', anchor = 'center', padx=40, pady=25)
boton_buscar = Button(frame, text = 'Buscar Registro', command = Registros.buscar_registro, font=("Arial, 12"), width= 15, height= 1).pack(side = 'top', anchor = 'center', padx=40, pady=25)
boton_editar = Button(frame, text = 'Editar Registro', command = Registros.editar_registro, font=("Arial, 12"), width= 15, height= 1).pack(side = 'top', anchor = 'center', padx=40, pady=25)
boton_eliminar = Button(frame, text = 'Eliminar Registro', command = Registros.eliminar_registro, font=("Arial, 12"), width= 15, height= 1).pack(side = 'top', anchor = 'center', padx=40, pady=25)
boton_informe = Button(frame, text = 'Informes', command = Registros.informes, background="yellow", font=("Arial, 12"), width= 15, height= 1).pack(side = 'top', anchor = 'center', padx=40, pady=25,)

#mensaje de pie de pagina
label = Label(ventana_principal, text= '', background="orange").pack() #separador
mensaje = StringVar()
mensaje.set("Selecciona una opcion para continuar")
monitor = Label(ventana_principal, textvar = mensaje, justify= "center", background="black", fg="yellow", font=("Arial, 14")) #alojamiento del mensaje
monitor.pack(side = "top", padx=100)

#para que se ejecute la interfaz grafica
ventana_principal.mainloop()
