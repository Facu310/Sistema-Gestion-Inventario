import mysql.connector
"""
Módulo de conexión a la base de datos.
Este módulo proporciona la funcionalidad para establecer y cerrar conexiones a la base de datos.
"""
class GestionInventario:


    connection = None
    host = "localhost"
    port = 3306
    user = "root"
    password = "57110030"
    db = "inventario"

    @staticmethod
    def get_conexion():
        GestionInventario.connection = mysql.connector.connect(
        host=GestionInventario.host,
        port=GestionInventario.port,
        user=GestionInventario.user,
        password=GestionInventario.password,
        db=GestionInventario.db
        )
        return GestionInventario.connection


    @staticmethod
    def close_conexion():
        if GestionInventario.connection.is_connected():
            GestionInventario.connection.close()


    @staticmethod
    def add_producto(nom: str, descripcion: str,cat: str, precio: str, stock: str) -> object:
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_insert = ("INSERT INTO producto (`nombre`, `descripcion`, `categoria`, `precio`, `stock`) "
                              "VALUES (%s, %s, %s, %s, %s)")
                valores_insert = (nom, descripcion, cat, precio, stock)
                cursor.execute(sql_insert, valores_insert)
                connection.commit()
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")

        finally:
            GestionInventario.close_conexion()
    @staticmethod
    def show_prod_table():
        try:
            connection= GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_sentence = ("SELECT Producto.Id, Producto.nombre "
                                "FROM Producto "
                                "LEFT JOIN ProveedorProducto ON Producto.Id = ProveedorProducto.ProductoId "
                                "WHERE ProveedorProducto.ProductoId IS NULL;")
                cursor.execute(sql_sentence)
                result = cursor.fetchall()
                connection.commit()
                return result
        except mysql.connector.Error as e:
            print(f"Error de MYSQL:{e} ")
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def add_supplier_db(rut: str,nom: str,contacto: str,terminios_pago: str)-> object:
        try:
            connection= GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_sentence = ("INSERT INTO `inventario`.`proveedor` (`Id`,`nombre`, `contacto`, `terminos_pago`) VALUES (%s,%s,%s,%s)")
                valores_insert=(rut,nom,contacto,terminios_pago)
                cursor.execute(sql_sentence,valores_insert)
                connection.commit()
        except Exception as e:
            print("ha ocurrido un error con mysql:", e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def add_supplier_prod(rut:str,prod: list):
        try:
            connection= GestionInventario.get_conexion()
            with connection.cursor() as cursor:
               for product in prod:
                sql_sentence=("INSERT INTO  `inventario`.`ProveedorProducto`(`ProveedorId`,`ProductoId`) VALUES (%s,%s)")
                valores_insert=(rut,product[0])
                cursor.execute(sql_sentence,valores_insert)
                connection.commit()
        except Exception as e:
            print("ha ocurrido un error con mysql:", e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def show_supplier():
        try:
            connection= GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_sentence=("SELECT Id, nombre, contacto "
                              "FROM Proveedor;")
                cursor.execute(sql_sentence)
                result = cursor.fetchall()
                connection.commit()
                return result
        except Exception as e:
            print("ha ocurrido un error con mysql", e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def view_prod_with_name(name: str,sentence:str):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                cursor.execute(sentence, {'name': name})
                result = cursor.fetchall()
                connection.commit()
                return result
        except Exception as e:
            print("Ha ocurrido un error con MySQL:", e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def view_supier(rut:str):
            try:
                connection = GestionInventario.get_conexion()
                with connection.cursor() as cursor:
                    sql_sentence = "SELECT Id, nombre, contacto FROM Proveedor WHERE Id = %(rut)s"
                    cursor.execute(sql_sentence, {'rut': rut})
                    result = cursor.fetchall()
                    connection.commit()
                    return result
            except Exception as e:
                print("Ha ocurrido un error con MySQL:", e)
            finally:
                GestionInventario.close_conexion()

    @staticmethod
    def view_table(sentence_sql):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                cursor.execute(sentence_sql)
                result = cursor.fetchall()
                connection.commit()
                return result
        except mysql.connector.Error as e:
            print(f"Error de MYSQL:{e} ")
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def update_pord(prod:tuple):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_sentence = (
                    f"UPDATE producto SET `{prod[1]}` = %s WHERE (`Id` = %s)")
                cursor.execute(sql_sentence, (prod[2],prod[0]))
                connection.commit()
        except Exception as e:
            print("Ha ocurrido un error con MySQL:", e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def add_order(id_suppier,date_initial,date_delivery,price,state,description):
        try:
            connection= GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_sentence = ("INSERT INTO `inventario`.`ordendecompra` "
                                "(`proveedor_id`, `fecha_realiza`, `fecha_entrega`, `precio`, `estado`, `Descripcion`) "
                                "VALUES (%s,%s, %s, %s, %s, %s)")
                valores_insert=(id_suppier,date_initial,date_delivery,price,state,description)
                cursor.execute(sql_sentence,valores_insert)
                connection.commit()
        except Exception as e:
            print("ha ocurrido un error con mysql:", e)
        finally:
            GestionInventario.close_conexion()
    @staticmethod
    def add_order_prod(order_id,prod_id,cantidad):
        try:
            connection= GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_sentence = ("INSERT INTO `inventario`.`ordendecompraproducto` (`OrdenDeCompraId`, `ProductoId`, `cantidad`) VALUES (%s,%s,%s)")
                valores_insert=(order_id,prod_id,cantidad)
                cursor.execute(sql_sentence,valores_insert)
                connection.commit()
        except Exception as e:
            print("ha ocurrido un error con mysql:", e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def get_last_id(table):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT MAX(id) FROM {table}")
                last_inserted_id = cursor.fetchone()

            return last_inserted_id[0]

        except Exception as e:
            print("Ha ocurrido un error con MySQL:", e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def view_suppier_prod(rut):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_sentence = ("SELECT P.Id AS ProductoId, P.Nombre AS NombreProducto "
                                "FROM ProveedorProducto PP "
                                "JOIN Producto P ON PP.ProductoId = P.Id "
                                "WHERE PP.ProveedorId = %(rut)s")
                cursor.execute(sql_sentence, {'rut': rut})
                result = cursor.fetchall()
                connection.commit()
                return result
        except mysql.connector.Error as e:
            print(f"Error de MYSQL:{e} ")
        finally:
            GestionInventario.close_conexion()
    @staticmethod
    def elements_edit_order():
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_sentence = ("SELECT OrdenDeCompra.*, OrdenDeCompraProducto.ProductoId, OrdenDeCompraProducto.cantidad "
                                "FROM OrdenDeCompra "
                                "JOIN OrdenDeCompraProducto ON OrdenDeCompra.id = OrdenDeCompraProducto.OrdenDeCompraId "
                                "LEFT JOIN PedidosRealizados ON OrdenDeCompra.id = PedidosRealizados.orden_de_compra_id "
                                "WHERE PedidosRealizados.orden_de_compra_id IS NULL")
                cursor.execute(sql_sentence)
                result = cursor.fetchall()
                connection.commit()
                return result
        except mysql.connector.Error as e:
            print(f"Error de MYSQL:{e} ")
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def uptade_orders(column,new_value,id_order):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql = f"UPDATE OrdenDeCompra SET {column} = %(new_value)s WHERE id = %(id_order)s"

                cursor.execute(sql, {"new_value": new_value, "id_order": id_order})
                connection.commit()
        except Exception as e:
            print("Ha ocurrido un error con MySQL:", e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def uptade_orders_prod(column, new_value, id_order,id_prod):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql = f"UPDATE OrdenDeCompraProducto SET {column} = %(new_value)s WHERE OrdenDeCompraId = %(id_order)s AND ProductoId= %(id_prod)s"
                cursor.execute(sql, {"new_value": new_value, "id_order": id_order ,"id_prod": id_prod})
                connection.commit()
        except Exception as e:
            print("Ha ocurrido un error con MySQL:", e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def exist_id_order(id_order):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_sentence = "SELECT id FROM OrdenDeCompra WHERE id = %(id_order)s"
                cursor.execute(sql_sentence, {"id_order": id_order})
                result = cursor.fetchone()
                connection.commit()
                return result
        except Exception as e:
            print("Ha ocurrido un error con MySQL:", e)
        finally:
            GestionInventario.close_conexion()
    @staticmethod
    def add_orders_placed(id_order,payment_date):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_sentence = "INSERT INTO `inventario`.`pedidosrealizados` (`orden_de_compra_id`, `fecha_pago`) VALUES (%s,%s)"
                values_insert=(id_order,payment_date)
                cursor.execute(sql_sentence,values_insert)
                connection.commit()
        except Exception as e:
            print("Ha ocurrido un error con MySQL:",e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def delete_order(id_order):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_sentence = "DELETE FROM `inventario`.`ordendecompra` WHERE id = %(id_order)s"
                cursor.execute(sql_sentence, {"id_order": id_order})
                connection.commit()
        except Exception as e:
            print("Ha ocurrido un error con MySQL:", e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def add_sales_record(sale_date,total_amount):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_sentence = "INSERT INTO `inventario`.`Ventas` (`fecha_venta`, `monto_total`) VALUES (%s,%s)"
                values_insert = (sale_date, total_amount)
                cursor.execute(sql_sentence, values_insert)
                connection.commit()
        except Exception as e:
            print("Ha ocurrido un error con MySQL:", e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def add_sales_record_prod(VentaId,ProductoId,cantidad,precio_unitario):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql_sentence = "INSERT INTO `inventario`.`ventaproducto` (`VentaId`, `ProductoId`, `cantidad`, `precio_unitario`) VALUES (%s,%s,%s,%s)"
                values_insert =(VentaId,ProductoId,cantidad,precio_unitario)
                cursor.execute(sql_sentence, values_insert)
                connection.commit()
        except Exception as e:
            print("Ha ocurrido un error con MySQL:", e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def update_sale(id_sale, column, value):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                # Utilizamos `%s` como marcador de posición en la consulta SQL
                sql = f"UPDATE `inventario`.`ventas` SET `{column}` = %s WHERE (`id` = %s)"
                # Pasamos los valores a través de la función execute como una tupla
                cursor.execute(sql, (value, id_sale))
                connection.commit()
        except Exception as e:
            print("Ha ocurrido un error con MySQL update_sale:", e)
        finally:
            GestionInventario.close_conexion()


    @staticmethod
    def update_sale_prod(id_sale, id_prod, column, value):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                # Utiliza `%s` como marcador de posición en la consulta SQL
                sql = f"UPDATE `inventario`.`ventaproducto` SET `{column}` = %s WHERE (`VentaId` = %s) and (`ProductoId` = %s)"
                # Pasa los valores a través de la función execute como una tupla
                cursor.execute(sql, (value, id_sale, id_prod))
                connection.commit()
        except Exception as e:
            print("Ha ocurrido un error con MySQL update_sale_prod:", e)
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def elim_prod(id_prod):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql = "DELETE FROM `inventario`.`producto` WHERE (`Id` = %s)"
                cursor.execute(sql, (id_prod,))
                connection.commit()
                return "Eliminado Correctamente"
        except Exception as e:
            return "No se puede eliminar el prducto"
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def elim_order(id_orden):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql = "DELETE FROM `inventario`.`ordendecompra` WHERE (`id` = %s)"
                cursor.execute(sql, (id_orden,))
                connection.commit()
                return "Eliminado Correctamente"
        except Exception as e:
            return "No se puede eliminar la orden"
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def elim_order_prod(id_order,id_prod):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                if id_prod=="":
                    print("Entro aca")
                    sql = "DELETE FROM `inventario`.`ordendecompraproducto` WHERE (`OrdenDeCompraId` = %s)"
                    cursor.execute(sql, (id_order, ))
                else:
                    print("Entro en la otra")
                    sql = "DELETE FROM `inventario`.`ordendecompraproducto` WHERE (`OrdenDeCompraId` = %s) and (`ProductoId` = %s)"
                    cursor.execute(sql, (id_order,id_prod))
                connection.commit()
                return "orden Eliminada Correctamente"
        except Exception as e:
            print(e)
            return "No se puede eliminar la orden"
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def elim_suppier(id):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                sql = "DELETE FROM `inventario`.`proveedor` WHERE (`Id` = %s)"
                cursor.execute(sql, (id,))
                connection.commit()
                return "Orden Eliminada Correctamente"
        except Exception as e:
            return "No se puede eliminar la orden"
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def elim_supier_prod(id_supier,id_prod):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                if id_prod == "":
                    print("Entro aca")
                    sql = "DELETE FROM `inventario`.`proveedorproducto` WHERE (`ProveedorId` = %s) "
                    cursor.execute(sql, (id_supier,))
                else:
                    print("Entro en la otra")
                    sql = "DELETE FROM `inventario`.`proveedorproducto` WHERE (`ProveedorId` = %s) and (`ProductoId` = %s)"
                    cursor.execute(sql, (id_supier, id_prod))
                connection.commit()
                return "Proveedor Eliminado Correctamente"
        except Exception as e:
            print(e)
            return "No se puede eliminar el provedor"
        finally:
            GestionInventario.close_conexion()

    @staticmethod
    def elim_sale(id):
            try:
                connection = GestionInventario.get_conexion()
                with connection.cursor() as cursor:
                    sql = "DELETE FROM `inventario`.`ventas` WHERE (`id` = %s)"
                    cursor.execute(sql, (id,))
                    connection.commit()
                    return "Venta Eliminada Correctamente"
            except Exception as e:
                return "No se puede eliminar la Venta"
            finally:
                GestionInventario.close_conexion()
    @staticmethod
    def elim_sale_prod(id_sale,id_prod):
        try:
            connection = GestionInventario.get_conexion()
            with connection.cursor() as cursor:
                if id_prod == "":
                    print("Entro aca")
                    sql = "DELETE FROM `inventario`.`ventaproducto` WHERE (`VentaId` = %s)"
                    cursor.execute(sql, (id_sale,))
                else:
                    print("Entro en la otra")
                    sql = "DELETE FROM `inventario`.`ventaproducto` WHERE (`VentaId` = %s) and (`ProductoId` = %ss)"
                    cursor.execute(sql, (id_sale, id_prod))
                connection.commit()
                return "Venta Eliminada Correctamente"
        except Exception as e:
            print(e)
            return "No se puede eliminar la veenta"
        finally:
            GestionInventario.close_conexion()












