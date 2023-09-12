from dearpygui import dearpygui as dpg
from peewee import *
from classes.tools  import elegant, Color
from classes.log    import Log

db = SqliteDatabase('ramon.db')


class DBTable:
    
    def __init__(self,name,fields=['id'],editable=[]):
        self.name       = name
        self.classname  = elegant(self.name)
        exec(f'from classes.{self.name} import {self.classname}')
        self.db         = eval(self.classname)
        self.tag        = f'table-{name}'
        self.fields     = fields
        self.editable   = editable
        self.rows       = self.getRows()
        self.render()

    def getRows(self):
        exec(f'from classes.{self.name} import {elegant(self.name)}')
        items = eval(f'{elegant(self.name)}.select().dicts()')
        rows = []
        for item in items:
            rows.append({ n : item[n] for n in self.fields })
        return rows
        
    def render(self):
        name        = self.name
        fields      = self.fields
        editable    = self.editable
        rows        = self.rows
      

        for index,row in enumerate(rows):
            with dpg.table_row(
                tag     = f'{self.tag}-row-{index}',
                parent  = f'table-{self.name}',                    
            ):
                for field_name in fields:
                    with dpg.table_cell():
                        if field_name in editable:
                            dpg.add_input_text( 
                                tag             = f"game:{field_name}:{row['id']}", 
                                default_value   = row[ field_name ], 
                                callback        = DBTable.updateField,
                                user_data       = row['id'],
                                on_enter        = True,
                                width           = 200,
                            )
                        else:
                            dpg.add_text(row[ field_name ], color=Color.lichi)

    def update(self):
        for index in range(0,len(self.rows)):
            dpg.delete_item(f'{self.tag}-row-{index}')
        self.rows = self.getRows()
        self.render()

    def updateField(sender, value, id):    
        instaname = sender.split(':')[0]
        classname = elegant(instaname)
        fieldname = sender.split(':')[1]
        try:
            exec(f'from classes.{instaname} import {classname}')
            exec(f'''{instaname} = {classname}.get(id={id})''')
            exec(f'''{instaname}.{fieldname}={ f'"{value}"' if isinstance(value, str) else value }''')
            exec(f'''{instaname}.save()''')
            Log.info("Stored data on DB")
        except Exception as E:
            Log.error("Cannot save data to DB", E)


    def create(name, fields=['id'], editable=[]):        
        with dpg.tab(label=elegant(name)+'s', tag=f"tab_database-{name}"):
            with dpg.child_window():
                with dpg.table(
                    show        = True, 
                    tag         = f'table-{name}',
                    resizable   = True, 
                    policy      = dpg.mvTable_SizingFixedFit,  
                    sortable    = True, 
                    callback    = None,
                ):                
                    for field in fields:
                        dpg.add_table_column(
                            label = elegant(field), 
                            parent = f'table-{name}',
                        )
                    table = DBTable(
                        name,
                        fields,
                        editable,
                    )
        return table

        