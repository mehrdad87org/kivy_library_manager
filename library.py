import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class LibraryManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        sql_create_table_cmd = '''
CREATE TABLE IF NOT EXISTS library (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    bprice REAL,
    aprice REAL,
    inventario INTEGER
)'''
        self.cursor.execute(sql_create_table_cmd)
        self.conn.commit()

    def add_item(self, name, bprice, aprice, inventario):
        self.cursor.execute("INSERT INTO library (name, bprice, aprice, inventario) VALUES (?, ?, ?, ?)", (name, bprice, aprice, inventario))
        self.conn.commit()

    def search_item(self, item_id):
        self.cursor.execute("SELECT * FROM library WHERE id=?", (item_id,))
        return self.cursor.fetchone()

    def delete_item(self, item_id):
        self.cursor.execute("DELETE FROM library WHERE id=?", (item_id,))
        self.conn.commit()

    def edit_item(self, item_id, bprice, aprice, inventario):
        self.cursor.execute("UPDATE library SET bprice=?, aprice=?, inventario=? WHERE id=?", (bprice, aprice, inventario, item_id))
        self.conn.commit()

    def clear_database(self):
        self.cursor.execute("DELETE FROM library")
        self.conn.commit()

    def close(self):
        self.conn.close()

class LibraryApp(App):
    def build(self):
        self.manager = LibraryManager('library.db')

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.entry_id = TextInput(hint_text="ID")
        self.entry_name = TextInput(hint_text="Name product")
        self.entry_purchase_price = TextInput(hint_text="Purchase price")
        self.entry_selling_price = TextInput(hint_text="Selling price")
        self.entry_quantity = TextInput(hint_text="Quantity")

        button_layout_top = BoxLayout(spacing=10)
        button_layout_bottom = BoxLayout(spacing=10)

        add_button = Button(text="Add item", background_color=(0, 1, 0, 1))
        add_button.bind(on_press=self.add_item)

        search_button = Button(text="Search item", background_color=(1, 1, 0, 1))
        search_button.bind(on_press=self.search_item)

        delete_button = Button(text="Delete item", background_color=(0, 0, 1, 1))
        delete_button.bind(on_press=self.delete_item)

        edit_button = Button(text="Edit", background_color=(1, 0.5, 0, 1))
        edit_button.bind(on_press=self.edit_item)

        clear_db_button = Button(text="Delete all", background_color=(0.5, 0, 0.5, 1))
        clear_db_button.bind(on_press=self.clear_database)

        quit_button = Button(text="Quit", background_color=(1, 0, 0, 1))
        quit_button.bind(on_press=self.stop)

        button_layout_top.add_widget(add_button)
        button_layout_top.add_widget(search_button)
        button_layout_top.add_widget(delete_button)

        button_layout_bottom.add_widget(edit_button)
        button_layout_bottom.add_widget(clear_db_button)
        button_layout_bottom.add_widget(quit_button)

        main_layout.add_widget(self.entry_id)
        main_layout.add_widget(self.entry_name)
        main_layout.add_widget(self.entry_purchase_price)
        main_layout.add_widget(self.entry_selling_price)
        main_layout.add_widget(self.entry_quantity)
        main_layout.add_widget(button_layout_top)
        main_layout.add_widget(button_layout_bottom)

        return main_layout

    def clear_fields(self):
        self.entry_id.text = ""
        self.entry_name.text = ""
        self.entry_purchase_price.text = ""
        self.entry_selling_price.text = ""
        self.entry_quantity.text = ""

    def add_item(self, instance):
        name = self.entry_name.text
        purchase_price = float(self.entry_purchase_price.text)
        selling_price = float(self.entry_selling_price.text)
        quantity = int(self.entry_quantity.text)
        self.manager.add_item(name, purchase_price, selling_price, quantity)
        self.clear_fields()

    def search_item(self, instance):
        item_id = self.entry_id.text
        item = self.manager.search_item(item_id)
        if item:
            print(f"ID: {item[0]}, commodity: {item[1]}, purchase price : {item[2]}, Selling price: {item[3]}, inventario : {item[4]}")
        else:
            print("Product not found!")

    def delete_item(self, instance):
        item_id = self.entry_id.text
        self.manager.delete_item(item_id)
        self.clear_fields()

    def edit_item(self, instance):
        item_id = self.entry_id.text
        purchase_price = float(self.entry_purchase_price.text)
        selling_price = float(self.entry_selling_price.text)
        quantity = int(self.entry_quantity.text)
        self.manager.edit_item(item_id, purchase_price, selling_price, quantity)
        self.clear_fields()

    def clear_database(self, instance):
        self.manager.clear_database()

    def on_stop(self):
        self.manager.close()

if __name__ == '__main__':
    LibraryApp().run()
