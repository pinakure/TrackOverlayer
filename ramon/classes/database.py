from dearpygui import dearpygui as dpg
from peewee import *
from classes.tools  import elegant, Color
from classes.log    import Log



def readonly(sender, value, user_data):
    dpg.set_value(sender, not value)


db = SqliteDatabase('ramon.db')
    
class DDBB(Model):

    version = DecimalField(max_digits=2, decimal_places=3, default=0.0)
    db      = db

    class Meta:
        database = db

    def init():        
        from classes.cheevo     import Cheevo
        from classes.game       import Game
        from classes.superchat  import Superchat
        from classes.ramon      import Ramon
        try:
            Log.info("Connecting DB...")
            DDBB.db.connect()
            DDBB.db.create_tables([DDBB, Game, Cheevo, Superchat ])
            try: 
                rows = [ x for x in DDBB.select().dicts()]
                if len(rows)>0:
                    row = rows[0]
                    r   = str(row['version'])
                    if r != str(Ramon.version):
                        a = 0/0
                    Log.info(f"Found v{r} database file")
            except Exception as E:
                Log.warning("Database file is incompatible, purging to fix structure...")
                # version didnt exist or file was corrupt
                Game.drop_table()
                Cheevo.drop_table()
                Superchat.drop_table()
                DDBB.db.create_tables([DDBB, Game, Cheevo, Superchat ])

            DDBB.truncate_table()
            cfg = DDBB(version=Ramon.version)
            # Re-set db version
            cfg.save()
            Log.info("DB connected.")
            
        except Exception as E:
            Log.warning(str(E))
        
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
                            if isinstance( row[ field_name ], str):
                                dpg.add_input_text( 
                                    tag             = f"{self.name}:{field_name}:{row['id']}", 
                                    default_value   = row[ field_name ], 
                                    callback        = DBTable.updateField,
                                    user_data       = row['id'],
                                    on_enter        = True,
                                    width           = 200,
                                )
                            if isinstance( row[ field_name ], bool):
                                dpg.add_checkbox( 
                                    tag             = f"{self.name}:{field_name}:{row['id']}", 
                                    default_value   = row[ field_name ], 
                                    callback        = DBTable.updateField,
                                    user_data       = row['id'],                                    
                                )

                        else:
                            if isinstance( row[ field_name ], bool):
                                dpg.add_checkbox( 
                                    tag             = f"{self.name}:{field_name}:{row['id']}", 
                                    default_value   = row[ field_name ], 
                                    callback        = readonly,
                                    user_data       = row['id'],
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
            #Database.db.close()
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
