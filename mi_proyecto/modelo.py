"""
Modelo: 
        componentes que llevan la tarea de hacer funcionar la app (ejemplo “agregar empleados”, “hacer la suma del sueldo”, etc)
"""
from tkinter import messagebox
import re
from peewee import *

#Creacion de la db y tabla

database = SqliteDatabase("mybs.db")

class BaseModel(Model):
    """
    Creamos la base de datos
    """
    class Meta:
        database = database

class Empleados(BaseModel):
    """
    Creamos la tabla y las columnas de la base de datos
    """
    nombre = CharField(unique=True)
    edad = FloatField()
    area = CharField()
    horas_diarias = FloatField()
    pago_por_hora = FloatField()
    dias_trabajados = FloatField()
    sueldo_mensual = CharField()
    
database.connect()
database.create_tables([Empleados])

#Definicion de clases y funciones 

class OperacionL():
    def limpiar(self, nombre, edad, area, horas_diarias, pago_por_hora, dias_trabajados):
        """
        Esta función se utiliza para limpiar los campos entry que se encuntran en nuestra ventana de tkinter
        """
        nombre.set("")
        edad.set("")
        area.set("")
        horas_diarias.set("0")
        pago_por_hora.set("0")
        dias_trabajados.set("0")

class Regex():
    def validar_nombre(self, nombre):
        """
        Esta función valida el campo de nombre, denegando asi el ingreso de numeros en el campo nombre.
        """
        regx = nombre.get()
        patron = "^[A-Za-záéíóú]*$"
        if (re.match(patron, regx)):
            print("Todo se encuentra correcto en el campo de texto")
            return True
        else:
            messagebox.showerror("Error", "No se pueden ingresar numeros en el campo nombre")
            return False
        
    def validar_area(self, area):
        """
        Esta función valida el campo area, denegando asi el ingreso de numeros en el campo area.
        """
        regx_2 = area.get()
        patron = "^[A-Za-záéíóú]*$"
        if (re.match(patron, regx_2)):
            print("Todo se encuentra correcto en el campo de texto")
            return True
        else:
            messagebox.showerror("Error", "No se pueden ingresar numeros en el campo area")
            return False   

class Operaciones():
    def alta(self, nombre, edad, area, horas_diarias, pago_por_hora, dias_trabajados, sueldo_men, planilla):
        """
        Esta función nos permite cargar los datos ingresados en la base de datos y de esa manera guardarlos.
        """
        regx = Regex()
        if not regx.validar_nombre(nombre) or not regx.validar_area(area):
            return
        
        empleado_existente = Empleados.select().where(Empleados.nombre == nombre.get()).first()

        if empleado_existente:
            messagebox.showerror("Error", "Ya existe un empleado con ese nombre en la base de datos.")
            return

        try:
            edad_val = int(edad.get())
            horas_diarias_val = int(horas_diarias.get())
            pago_por_hora_val = int(pago_por_hora.get())
            dias_trabajados_val = int(dias_trabajados.get())

            if not edad_val or not horas_diarias_val or not pago_por_hora_val or not dias_trabajados_val:
                raise ValueError("Edad, Horas diarias, pago por hora, y dias trabajados deben ser valores enteros y no pueden estar vacios.")
                        
            sueldo_men = (horas_diarias_val * pago_por_hora_val) * (dias_trabajados_val)
            empleado = Empleados()
            empleado.nombre = nombre.get()
            empleado.edad = edad_val
            empleado.area = area.get()
            empleado.horas_diarias = horas_diarias_val
            empleado.pago_por_hora = pago_por_hora_val
            empleado.dias_trabajados = dias_trabajados_val
            empleado.sueldo_mensual = sueldo_men
            empleado.save()

            actualizar_treeview(planilla)
            OperacionL.limpiar(self, nombre, edad, area, horas_diarias, pago_por_hora, dias_trabajados)

        except ValueError as e:
            messagebox.showerror("Error", e)

        else:
            messagebox.showinfo("Exito", "Empleado agregado.")
    
    def baja(self, planilla):
        """
        Esta función nos permite borrar un elemento de la tabla.
        """
        valor = planilla.selection()
        print(valor)
        item = planilla.item(valor)
        print(item)    
        print(item['text'])
        
        borrar = Empleados.get(Empleados.id == item["text"])
        borrar.delete_instance()

        planilla.delete(valor)

        messagebox.showinfo("Éxito", "Empleado dado de baja.")

    def modificar(self, nombre, edad, area, horas_diarias, pago_por_hora, dias_trabajados, planilla):
        """
        Esta función nos permite modificar los elementos ingresados en la tabla en caso de equivocacion.
        """
        valor = planilla.selection()
        print(valor)
        item = planilla.item(valor)
        print(item)    
        print(item['text'])
        
        regx_m = Regex()
        if not regx_m.validar_nombre(nombre) or not regx_m.validar_area(area):
            return   

        try:
            edad_nuevo = edad.get()
            horas_diarias_nuevo = horas_diarias.get()
            pago_por_hora_nuevo = pago_por_hora.get()
            dias_trabajados_nuevo = dias_trabajados.get()

            if not edad_nuevo or not horas_diarias_nuevo or not pago_por_hora_nuevo or not dias_trabajados_nuevo:
                raise ValueError("Debe realizar los cambios en todos los campos o que no esten vacios.")
            
            sueldo_men = (horas_diarias_nuevo * pago_por_hora_nuevo) * dias_trabajados_nuevo

            actualizar_datos = Empleados.update(nombre=nombre.get(), 
                                            edad=edad_nuevo, area=area.get(), 
                                            horas_diarias=horas_diarias_nuevo, pago_por_hora=pago_por_hora_nuevo, 
                                            dias_trabajados=dias_trabajados_nuevo, sueldo_mensual=sueldo_men).where(Empleados.id == item["text"])
            actualizar_datos.execute()
            
            messagebox.showinfo("Éxito", "Empleado actualizado con éxito")
            actualizar_treeview(planilla)
            OperacionL.limpiar(self, nombre, edad, area, horas_diarias, pago_por_hora, dias_trabajados)

        except ValueError as a:
            messagebox.showerror("Error", a)

def actualizar_treeview(mytreeview):
    """
    Esta función actualiza la planilla(treeview) que tenemos en nuestra ventana de tkinter.
    """
    records = mytreeview.get_children()
    for element in records:
        mytreeview.delete(element)   

    for fila in Empleados.select():
        mytreeview.insert("", 0, text=fila.id, values=(fila.nombre, fila.edad, fila.area, fila.horas_diarias, fila.pago_por_hora, fila.dias_trabajados))

def cargar_datos(treeview):
    """
    Esta función nos permite cargar los datos ingresados con anterioridad en la base de datos.
    """
    treeview.delete(*treeview.get_children())

    grabado = Empleados.select()

    for record in grabado:
        treeview.insert("", "end", text=record.id, values=(record.nombre, record.edad, record.area, record.horas_diarias, record.pago_por_hora, record.dias_trabajados))
    messagebox.showinfo("Exito", "Datos cargados")