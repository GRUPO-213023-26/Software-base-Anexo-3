
import tkinter as tk
from tkinter import ttk, messagebox

from gestor_sistema import GestorSistema
from excepciones import ErrorSistemaFJ


class AplicacionFJ:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Software FJ / Estudiante: Carlos Andrés Cuervo Vergara")
        self.raiz.geometry("780x520")
        self.sistema = GestorSistema()

        # Notebook (pestañas)
        self.pestañas = ttk.Notebook(raiz)
        self.pestañas.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_clientes = ttk.Frame(self.pestañas)
        self.tab_servicios = ttk.Frame(self.pestañas)
        self.tab_reservas = ttk.Frame(self.pestañas)

        self.pestañas.add(self.tab_clientes, text="Clientes")
        self.pestañas.add(self.tab_servicios, text="Servicios")
        self.pestañas.add(self.tab_reservas, text="Reservas")

        self._construir_tab_clientes()
        self._construir_tab_servicios()
        self._construir_tab_reservas()

    # ------------------------------------------------------------------
    # PESTAÑA CLIENTES
    # ------------------------------------------------------------------
    def _construir_tab_clientes(self):
        frame = self.tab_clientes

        campos = ["ID Cliente", "Nombre", "Documento", "Telefono", "Email"]
        self.entradas_cliente = {}

        for i, etiqueta in enumerate(campos):
            tk.Label(frame, text=etiqueta + ":").grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entrada = tk.Entry(frame, width=35)
            entrada.grid(row=i, column=1, padx=5, pady=5)
            self.entradas_cliente[etiqueta] = entrada

        tk.Button(frame, text="Registrar Cliente", command=self._registrar_cliente_gui).grid(
            row=len(campos), column=0, columnspan=2, pady=10
        )

        tk.Label(frame, text="Clientes registrados:").grid(row=len(campos) + 1, column=0, columnspan=2, sticky="w", padx=5)
        self.lista_clientes = tk.Listbox(frame, width=90, height=10)
        self.lista_clientes.grid(row=len(campos) + 2, column=0, columnspan=2, padx=5, pady=5)

    def _registrar_cliente_gui(self):
        datos = {k: v.get().strip() for k, v in self.entradas_cliente.items()}
        try:
            id_cliente = int(datos["ID Cliente"])
            cliente = self.sistema.registrar_cliente(
                id_cliente, datos["Nombre"], datos["Documento"], datos["Telefono"], datos["Email"]
            )
        except ValueError:
            messagebox.showerror("Error", "El ID del cliente debe ser un numero entero.")
        except ErrorSistemaFJ as error:
            messagebox.showerror("Error de validacion", str(error))
        else:
            messagebox.showinfo("Exito", "Cliente registrado correctamente.")
            self.lista_clientes.insert(tk.END, cliente.mostrar_informacion())
            self._refrescar_combo_clientes()
        finally:
            pass  # aqui se podria limpiar los campos si se quiere

    # ------------------------------------------------------------------
    # PESTAÑA SERVICIOS
    # ------------------------------------------------------------------
    def _construir_tab_servicios(self):
        frame = self.tab_servicios

        tk.Label(frame, text="Tipo de servicio:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.combo_tipo_servicio = ttk.Combobox(
            frame, values=["Sala", "Equipo", "Asesoria"], state="readonly", width=32
        )
        self.combo_tipo_servicio.grid(row=0, column=1, padx=5, pady=5)
        self.combo_tipo_servicio.current(0)

        campos = ["ID Servicio", "Nombre", "Valor (hora/dia)", "Cantidad (horas/dias)",
                  "Deposito (solo equipos)", "Especialista (solo asesoria)"]
        self.entradas_servicio = {}

        for i, etiqueta in enumerate(campos, start=1):
            tk.Label(frame, text=etiqueta + ":").grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entrada = tk.Entry(frame, width=35)
            entrada.grid(row=i, column=1, padx=5, pady=5)
            self.entradas_servicio[etiqueta] = entrada

        fila_boton = len(campos) + 1
        tk.Button(frame, text="Crear Servicio", command=self._registrar_servicio_gui).grid(
            row=fila_boton, column=0, columnspan=2, pady=10
        )

        tk.Label(frame, text="Servicios registrados:").grid(row=fila_boton + 1, column=0, columnspan=2, sticky="w", padx=5)
        self.lista_servicios = tk.Listbox(frame, width=90, height=8)
        self.lista_servicios.grid(row=fila_boton + 2, column=0, columnspan=2, padx=5, pady=5)

    def _registrar_servicio_gui(self):
        tipo = self.combo_tipo_servicio.get()
        datos = {k: v.get().strip() for k, v in self.entradas_servicio.items()}
        try:
            id_servicio = int(datos["ID Servicio"])
            nombre = datos["Nombre"]
            valor = float(datos["Valor (hora/dia)"])
            cantidad = float(datos["Cantidad (horas/dias)"])

            if tipo == "Sala":
                servicio = self.sistema.registrar_servicio_sala(id_servicio, nombre, valor, cantidad)
            elif tipo == "Equipo":
                deposito_texto = datos["Deposito (solo equipos)"]
                deposito = float(deposito_texto) if deposito_texto else 0
                servicio = self.sistema.registrar_servicio_equipo(id_servicio, nombre, valor, cantidad, deposito)
            else:  # Asesoria
                especialista = datos["Especialista (solo asesoria)"]
                servicio = self.sistema.registrar_servicio_asesoria(id_servicio, nombre, valor, cantidad, especialista)

        except ValueError:
            messagebox.showerror("Error", "Verifica que ID, valor y cantidad sean numeros validos.")
        except ErrorSistemaFJ as error:
            messagebox.showerror("Error de validacion", str(error))
        else:
            messagebox.showinfo("Exito", "Servicio creado correctamente.")
            self.lista_servicios.insert(tk.END, servicio.describir_servicio())
            self._refrescar_combo_servicios()

    # ------------------------------------------------------------------
    # PESTAÑA RESERVAS
    # ------------------------------------------------------------------
    def _construir_tab_reservas(self):
        frame = self.tab_reservas

        tk.Label(frame, text="Cliente:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.combo_clientes = ttk.Combobox(frame, state="readonly", width=32)
        self.combo_clientes.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Servicio:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.combo_servicios = ttk.Combobox(frame, state="readonly", width=32)
        self.combo_servicios.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Duracion:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entrada_duracion = tk.Entry(frame, width=35)
        self.entrada_duracion.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="Crear Reserva", command=self._crear_reserva_gui).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        tk.Label(frame, text="Reservas:").grid(row=4, column=0, columnspan=2, sticky="w", padx=5)
        self.lista_reservas = tk.Listbox(frame, width=90, height=8)
        self.lista_reservas.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        frame_botones = tk.Frame(frame)
        frame_botones.grid(row=6, column=0, columnspan=2, pady=10)

        tk.Button(frame_botones, text="Confirmar seleccionada", command=self._confirmar_reserva_gui).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Cancelar seleccionada", command=self._cancelar_reserva_gui).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Procesar (calcular costo)", command=self._procesar_reserva_gui).pack(side="left", padx=5)

    def _refrescar_combo_clientes(self):
        valores = [f"{c.id_entidad} - {c.nombre}" for c in self.sistema.clientes]
        self.combo_clientes["values"] = valores
        if valores:
            self.combo_clientes.current(0)

    def _refrescar_combo_servicios(self):
        valores = [f"{s.id_servicio} - {s.nombre_servicio}" for s in self.sistema.servicios]
        self.combo_servicios["values"] = valores
        if valores:
            self.combo_servicios.current(0)

    def _crear_reserva_gui(self):
        try:
            if not self.combo_clientes.get() or not self.combo_servicios.get():
                raise ValueError("Debes seleccionar un cliente y un servicio.")

            id_cliente = int(self.combo_clientes.get().split(" - ")[0])
            id_servicio = int(self.combo_servicios.get().split(" - ")[0])
            duracion = float(self.entrada_duracion.get())

            reserva = self.sistema.crear_reserva(id_cliente, id_servicio, duracion)
        except ValueError as error:
            messagebox.showerror("Error", str(error))
        except ErrorSistemaFJ as error:
            messagebox.showerror("Error de validacion", str(error))
        else:
            messagebox.showinfo("Exito", "Reserva creada correctamente (queda en estado 'pendiente').")
            self.lista_reservas.insert(tk.END, reserva.mostrar_informacion())

    def _obtener_reserva_seleccionada(self):
        seleccion = self.lista_reservas.curselection()
        if not seleccion:
            messagebox.showwarning("Atencion", "Selecciona una reserva de la lista primero.")
            return None
        return self.sistema.reservas[seleccion[0]]

    def _refrescar_item_reserva(self, indice, reserva):
        self.lista_reservas.delete(indice)
        self.lista_reservas.insert(indice, reserva.mostrar_informacion())

    def _confirmar_reserva_gui(self):
        indice = self.lista_reservas.curselection()
        reserva = self._obtener_reserva_seleccionada()
        if reserva is None:
            return
        try:
            reserva.confirmar()
        except ErrorSistemaFJ as error:
            messagebox.showerror("Error", str(error))
        else:
            messagebox.showinfo("Exito", "Reserva confirmada.")
            self._refrescar_item_reserva(indice[0], reserva)

    def _cancelar_reserva_gui(self):
        indice = self.lista_reservas.curselection()
        reserva = self._obtener_reserva_seleccionada()
        if reserva is None:
            return
        try:
            reserva.cancelar()
        except ErrorSistemaFJ as error:
            messagebox.showerror("Error", str(error))
        else:
            messagebox.showinfo("Exito", "Reserva cancelada.")
            self._refrescar_item_reserva(indice[0], reserva)

    def _procesar_reserva_gui(self):
        reserva = self._obtener_reserva_seleccionada()
        if reserva is None:
            return
        try:
            costo = reserva.procesar()
        except ErrorSistemaFJ as error:
            messagebox.showerror("Error", str(error))
        else:
            messagebox.showinfo("Costo calculado", f"El costo total de la reserva es: ${costo:,.2f}")


def main():
    raiz = tk.Tk()
    app = AplicacionFJ(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
