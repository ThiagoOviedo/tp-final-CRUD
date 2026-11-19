# TP Final - Thiago Oviedo
# Sistema de stock por consola con Python y MySQL
# Tiene dos tablas: categorias y productos (cada producto tiene una categoría)

import mysql.connector

# me conecto a la base de datos stock (acá va la contraseña de MySQL de cada uno)
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="TU_CONTRASEÑA",
    database="stock"
)
cursor = conexion.cursor()

# así los cambios se guardan solos en la base
conexion.autocommit = True

# el menú se repite hasta que elijo salir
while True:
    print("STOCK - CRUD")
    print("1. Agregar categoría")
    print("2. Agregar producto")
    print("3. Listar productos")
    print("4. Modificar producto")
    print("5. Borrar producto")
    print("6. Borrar categoría")
    print("7. Listar categorías")
    print("8. Modificar categoría")
    print("9. Salir")
    opcion = input("Ingrese una opción: ")
    print("-----------------------------------------")

    # uso try/except para que si algo sale mal el programa no se cierre
    try:

        # agregar categoría
        if opcion == "1":
            nombre = input("Nombre de la categoría: ")
            cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre,))
            print("Categoría agregada")

        # agregar producto
        # primero muestro las categorías para saber qué ID puedo usar
        elif opcion == "2":
            cursor.execute("SELECT id_categoria, nombre FROM categorias")
            for fila in cursor.fetchall():
                print(fila[0], fila[1])
            nombre = input("Nombre del producto: ")
            precio = int(input("Precio: "))
            stock = int(input("Stock: "))
            id_categoria = int(input("ID de la categoría: "))
            consulta = "INSERT INTO productos (nombre, precio, stock, id_categoria) VALUES (%s, %s, %s, %s)"
            cursor.execute(consulta, (nombre, precio, stock, id_categoria))
            print("Producto agregado")

        # listar productos
        # con el JOIN junto las dos tablas para ver el nombre de la categoría
        elif opcion == "3":
            consulta = """SELECT productos.id_producto, productos.nombre, productos.precio,
                          productos.stock, categorias.nombre
                          FROM productos
                          JOIN categorias ON productos.id_categoria = categorias.id_categoria"""
            cursor.execute(consulta)
            for fila in cursor.fetchall():
                print(fila[0], fila[1], fila[2], fila[3], fila[4])

        # modificar producto (también se puede cambiar la categoría)
        elif opcion == "4":
            id_producto = int(input("ID del producto a modificar: "))
            # miro si el producto existe antes de pedir los datos nuevos
            cursor.execute("SELECT COUNT(*) FROM productos WHERE id_producto = %s", (id_producto,))
            if cursor.fetchone()[0] == 0:
                print("No existe un producto con ese ID")
            else:
                nombre = input("Nuevo nombre: ")
                precio = int(input("Nuevo precio: "))
                stock = int(input("Nuevo stock: "))
                cursor.execute("SELECT id_categoria, nombre FROM categorias")
                for fila in cursor.fetchall():
                    print(fila[0], fila[1])
                id_categoria = int(input("Nuevo ID de la categoría: "))
                consulta = "UPDATE productos SET nombre = %s, precio = %s, stock = %s, id_categoria = %s WHERE id_producto = %s"
                cursor.execute(consulta, (nombre, precio, stock, id_categoria, id_producto))
                print("Modificación exitosa")

        # borrar producto
        elif opcion == "5":
            id_producto = int(input("ID del producto a borrar: "))
            cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
            # rowcount me dice cuántas filas borró, si es 0 es que ese ID no existía
            if cursor.rowcount == 0:
                print("No existe un producto con ese ID")
            else:
                print("Borrado exitoso")

        # borrar categoría
        # si todavía tiene productos no la dejo borrar
        elif opcion == "6":
            cursor.execute("SELECT id_categoria, nombre FROM categorias")
            for fila in cursor.fetchall():
                print(fila[0], fila[1])
            id_categoria = int(input("ID de la categoría a borrar: "))
            cursor.execute("SELECT COUNT(*) FROM productos WHERE id_categoria = %s", (id_categoria,))
            cantidad = cursor.fetchone()[0]
            if cantidad > 0:
                print("No se puede borrar: hay", cantidad, "producto(s) en esa categoría")
            else:
                cursor.execute("DELETE FROM categorias WHERE id_categoria = %s", (id_categoria,))
                if cursor.rowcount == 0:
                    print("No existe una categoría con ese ID")
                else:
                    print("Categoría borrada")

        # listar categorías
        elif opcion == "7":
            cursor.execute("SELECT id_categoria, nombre FROM categorias")
            for fila in cursor.fetchall():
                print(fila[0], fila[1])

        # modificar el nombre de una categoría
        elif opcion == "8":
            cursor.execute("SELECT id_categoria, nombre FROM categorias")
            for fila in cursor.fetchall():
                print(fila[0], fila[1])
            id_categoria = int(input("ID de la categoría a modificar: "))
            cursor.execute("SELECT COUNT(*) FROM categorias WHERE id_categoria = %s", (id_categoria,))
            if cursor.fetchone()[0] == 0:
                print("No existe una categoría con ese ID")
            else:
                nombre = input("Nuevo nombre: ")
                cursor.execute("UPDATE categorias SET nombre = %s WHERE id_categoria = %s", (nombre, id_categoria))
                print("Modificación exitosa")

        # salir
        elif opcion == "9":
            print("GRACIAS")
            break

        else:
            print("Selección inválida")

    # si escribo letras donde va un número
    except ValueError:
        print("Error: tenés que ingresar un número entero donde se pide un número")

    # errores de la base de datos
    except mysql.connector.Error as error:
        if error.errno == 1452:
            # la categoría que puse no existe
            print("Error: esa categoría no existe")
        elif error.errno == 1062:
            # ya hay una categoría con ese nombre (por el UNIQUE)
            print("Error: ya existe una categoría con ese nombre")
        else:
            print("Error de base de datos:", error)

    print("-----------------------------------------")

# cierro la conexión al salir
conexion.close()
