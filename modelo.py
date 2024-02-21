#modelo
from tkinter import messagebox
import re
from peewee import *

"""Modelo: componentes que llevan la tarea de hacer funcionar la app (ejemplo “agregar empleados”, “hacer la suma del sueldo”, etc)"""

#Creacion de la db y tabla

database = SqliteDatabase("mybs.db")

class BaseModel(Model):
    class Meta:
        database = database

class Empleados(BaseModel):
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
        nombre.set("")
        edad.set("")
        area.set("")
        horas_diarias.set("0")
        pago_por_hora.set("0")
        dias_trabajados.set("0")

class Regex():
    def validar(self, nombre, area):
        regx = nombre.get()
        regx_2 = area.get()
        patron = "^[A-Za-záéíóú]*$"
        if (re.match(patron, regx) and re.match(patron, regx_2)):
            print("Todo se encuentra correcto en los campos de texto")
            return True
        else:
            messagebox.showerror("Error", "No se pueden ingresar numeros en los campos nombre y area")
            return False

class Operaciones():
    def alta(self, nombre, edad, area, horas_diarias, pago_por_hora, dias_trabajados, sueldo_men, planilla):
        regx = Regex()
        if not regx.validar(nombre, area):
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
        valor = planilla.selection()
        print(valor)
        item = planilla.item(valor)
        print(item)    
        print(item['text'])
        
        regx_m = Regex()
        if not regx_m.validar(nombre, area):
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
    records = mytreeview.get_children()
    for element in records:
        mytreeview.delete(element)   

    for fila in Empleados.select():
        mytreeview.insert("", 0, text=fila.id, values=(fila.nombre, fila.edad, fila.area, fila.horas_diarias, fila.pago_por_hora, fila.dias_trabajados))