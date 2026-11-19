import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""ACA_VA_TU_CONTRASENA"",
    database="stock"
)
cursor = conexion.cursor()
conexion.autocommit = True

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

    if opcion == "1":
        nombre = input("Nombre de la categoría: ")
        consulta = "INSERT INTO categorias (nombre) VALUES (%s)"
        cursor.execute(consulta, (nombre,))
        conexion.commit()
        print("Categoría agregada")

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
        conexion.commit()
        print("Producto agregado")

    elif opcion == "3":
        consulta = """SELECT productos.id_producto, productos.nombre, productos.precio,
                      productos.stock, categorias.nombre
                      FROM productos
                      JOIN categorias ON productos.id_categoria = categorias.id_categoria"""
        cursor.execute(consulta)
        for fila in cursor.fetchall():
            print(fila[0], fila[1], fila[2], fila[3], fila[4])

    elif opcion == "4":
        id_producto = int(input("ID del producto a modificar: "))
        nombre = input("Nuevo nombre: ")
        precio = int(input("Nuevo precio: "))
        stock = int(input("Nuevo stock: "))
        consulta = "UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id_producto = %s"
        cursor.execute(consulta, (nombre, precio, stock, id_producto))
        conexion.commit()
        print("Modificación exitosa")

    elif opcion == "5":
        id_producto = int(input("ID del producto a borrar: "))
        consulta = "DELETE FROM productos WHERE id_producto = %s"
        cursor.execute(consulta, (id_producto,))
        conexion.commit()
        print("Borrado exitoso")

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
            consulta = "DELETE FROM categorias WHERE id_categoria = %s"
            cursor.execute(consulta, (id_categoria,))
            conexion.commit()
            print("Categoría borrada")

    elif opcion == "7":
        cursor.execute("SELECT id_categoria, nombre FROM categorias")
        for fila in cursor.fetchall():
            print(fila[0], fila[1])

    elif opcion == "8":
        cursor.execute("SELECT id_categoria, nombre FROM categorias")
        for fila in cursor.fetchall():
            print(fila[0], fila[1])
        id_categoria = int(input("ID de la categoría a modificar: "))
        nombre = input("Nuevo nombre: ")
        consulta = "UPDATE categorias SET nombre = %s WHERE id_categoria = %s"
        cursor.execute(consulta, (nombre, id_categoria))
        conexion.commit()
        print("Modificación exitosa")

    elif opcion == "9":
        print("GRACIAS")
        break

    else:
        print("Selección inválida")

    print("-----------------------------------------")

conexion.close()
