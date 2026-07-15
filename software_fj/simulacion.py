from gestor_sistema import GestorSistema
from excepciones import ErrorSistemaFJ


def separador(titulo):
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)


def ejecutar_operacion(numero, descripcion, funcion):
    """
    Ejecuta una operacion de la simulacion de forma segura.
    Si algo falla, se muestra el error en pantalla pero el
    programa sigue funcionando con la siguiente operacion.
    """
    print(f"\n--- Operacion {numero}: {descripcion} ---")
    try:
        resultado = funcion()
        print(f"OK -> {resultado}")
    except ErrorSistemaFJ as error:
        print(f"ERROR CONTROLADO -> {error}")
    except Exception as error:
        # Cualquier error no previsto tambien se controla, el programa no se cae
        print(f"ERROR INESPERADO -> {error}")


def main():
    sistema = GestorSistema()

    separador("REGISTRO DE CLIENTES")

    # 1. Cliente valido
    ejecutar_operacion(
        1, "Registrar cliente valido (Juan Perez)",
        lambda: sistema.registrar_cliente(1, "Juan Perez", "1010101010", "3001234567", "juan@correo.com")
    )

    # 2. Cliente valido
    ejecutar_operacion(
        2, "Registrar cliente valido (Maria Gomez)",
        lambda: sistema.registrar_cliente(2, "Maria Gomez", "2020202020", "3109876543", "maria@correo.com")
    )

    # 3. Cliente invalido: documento no numerico
    ejecutar_operacion(
        3, "Registrar cliente invalido (documento con letras)",
        lambda: sistema.registrar_cliente(3, "Carlos Ruiz", "abc123", "3001112233", "carlos@correo.com")
    )

    # 4. Cliente invalido: email sin formato correcto
    ejecutar_operacion(
        4, "Registrar cliente invalido (email mal formado)",
        lambda: sistema.registrar_cliente(4, "Ana Torres", "3030303030", "3005556677", "ana-correo-invalido")
    )

    separador("CREACION DE SERVICIOS")

    # 5. Servicio de sala valido
    ejecutar_operacion(
        5, "Crear servicio de sala valido",
        lambda: sistema.registrar_servicio_sala(101, "Sala de Juntas A", 50000, 3)
    )

    # 6. Servicio de equipo valido
    ejecutar_operacion(
        6, "Crear servicio de equipo valido",
        lambda: sistema.registrar_servicio_equipo(102, "Videobeam Epson", 30000, 2, deposito=50000)
    )

    # 7. Servicio de asesoria valido
    ejecutar_operacion(
        7, "Crear servicio de asesoria valido",
        lambda: sistema.registrar_servicio_asesoria(103, "Asesoria en Marketing Digital", 80000, 4, "Laura Diaz")
    )

    # 8. Servicio invalido: precio negativo
    ejecutar_operacion(
        8, "Crear servicio de sala invalido (precio negativo)",
        lambda: sistema.registrar_servicio_sala(104, "Sala VIP", -20000, 2)
    )

    # 9. Servicio invalido: falta el especialista
    ejecutar_operacion(
        9, "Crear servicio de asesoria invalido (sin especialista)",
        lambda: sistema.registrar_servicio_asesoria(105, "Asesoria Legal", 90000, 2, "")
    )

    separador("CREACION DE RESERVAS")

    # 10. Reserva exitosa (cliente 1, sala 101)
    ejecutar_operacion(
        10, "Crear reserva valida (Juan Perez - Sala de Juntas A)",
        lambda: sistema.crear_reserva(1, 101, 3)
    )

    # 11. Reserva exitosa (cliente 2, equipo 102)
    ejecutar_operacion(
        11, "Crear reserva valida (Maria Gomez - Videobeam)",
        lambda: sistema.crear_reserva(2, 102, 2)
    )

    # 12. Reserva fallida: cliente no existe
    ejecutar_operacion(
        12, "Crear reserva invalida (cliente inexistente)",
        lambda: sistema.crear_reserva(99, 101, 1)
    )

    # 13. Reserva fallida: servicio no existe
    ejecutar_operacion(
        13, "Crear reserva invalida (servicio inexistente)",
        lambda: sistema.crear_reserva(1, 999, 1)
    )

    separador("CONFIRMACION Y PROCESAMIENTO DE RESERVAS")

    # 14. Confirmar la reserva 1 (deberia existir en sistema.reservas[0])
    if len(sistema.reservas) >= 1:
        ejecutar_operacion(
            14, "Confirmar la primera reserva creada",
            lambda: (sistema.reservas[0].confirmar(), "Reserva confirmada")[1]
        )

        # 15. Procesar (calcular costo) de la primera reserva, con impuesto y descuento
        ejecutar_operacion(
            15, "Procesar la primera reserva (con impuesto 19% y descuento 10%)",
            lambda: sistema.reservas[0].procesar(impuesto=0.19, descuento=0.10)
        )

        # 16. Intentar confirmar de nuevo la misma reserva (ya confirmada -> error controlado)
        ejecutar_operacion(
            16, "Confirmar de nuevo la misma reserva (deberia fallar)",
            lambda: (sistema.reservas[0].confirmar(), "no deberia llegar aqui")[1]
        )

        # 17. Cancelar la reserva ya confirmada
        ejecutar_operacion(
            17, "Cancelar la primera reserva",
            lambda: (sistema.reservas[0].cancelar(), "Reserva cancelada")[1]
        )

        # 18. Intentar procesar una reserva ya cancelada (deberia fallar)
        ejecutar_operacion(
            18, "Procesar una reserva cancelada (deberia fallar)",
            lambda: sistema.reservas[0].procesar()
        )

    separador("RESUMEN FINAL DEL SISTEMA")

    print("\nClientes registrados:")
    for info in sistema.listar_clientes():
        print(" -", info)

    print("\nServicios registrados:")
    for info in sistema.listar_servicios():
        print(" -", info)

    print("\nReservas registradas:")
    for info in sistema.listar_reservas():
        print(" -", info)

    print("\nSimulacion terminada. Revisa el archivo 'logs.txt' para ver el detalle completo.")


if __name__ == "__main__":
    main()
