import panel as pn
import pandas as pd
import os
import sys
import pymysql

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.append(script_dir)

from server import connection
from requests import PullData, InsertData

#table name is inventory for some Godforsaken reason
#fire whoever did that


# try:
#     cursor = connection.cursor()

#     #Insert code here
#     cursor.execute("""
#         CREATE TABLE inventory(
#             id VARCHAR(50) NOT NULL,
#             itemname VARCHAR(50) NOT NULL,
#             amount INT NOT NULL,
#             PRIMARY KEY (id)
            
#         )
#     """)

#     cursor.execute("""
#         CREATE TABLE user(
#             netid VARCHAR(50) NOT NULL,
#             id VARCHAR(50),
#             amount INT NOT NULL,
#             PRIMARY KEY (netid),
#             FOREIGN KEY (id) REFERENCES inventory (id)
#         )
#     """)


# #Don't touch
# finally:
#     connection.close()


def home_page(layout, db_value, host_value, port_value, user_value, password_value):
    try:
        server1 = connection(db_value, host_value, password_value, port_value, user_value)
        cursor1 = server1.cursor()
        cursor1.execute(PullData("inventory").get_query())
        df = pd.DataFrame(cursor1.fetchall())
        user_df = df.copy()
        df_panel = pn.pane.DataFrame(df, width=800, height=400)
        user_df_pane = pn.widgets.DataFrame(user_df, width=800, height=400)
        save_button = pn.widgets.Button(name="Save Changes", button_type="primary")
        history_log = pn.widgets.TextAreaInput(placeholder="History of changes will appear here...", width=800, height=200)
        def save_changes(event):
            try:
                changes = user_df.compare(df)
                queries = []
                for index, row in changes.iterrows():
                    set_clause = ', '.join([f"{col} = %s" for col in row.keys()])
                    where_clause = f"hash_key = {index}"
                    query = f"UPDATE inventory SET {set_clause} WHERE {where_clause};"
                    queries.append(query)
                for query in queries:
                    cursor1.execute(query, tuple(changes.loc[index].values))
                server1.commit()
                print("Changes saved successfully.")
                df[:] = user_df[:]
                history_log.value = ""

            except Exception as e:
                print(f"Error saving changes: {e}")
        save_button.on_click(save_changes)
        insert_form = pn.Column(
            pn.widgets.TextInput(name="Hash Key", placeholder="Enter hash key..."),
            pn.widgets.TextInput(name="Item", placeholder="Enter item name..."),
            pn.widgets.IntInput(name="Quantity", placeholder="Enter quantity..."),
            pn.widgets.TextInput(name="Location", placeholder="Enter location..."),
            pn.widgets.TextInput(name="Subteam", placeholder="Enter subteam..."),
            pn.widgets.IntInput(name="Reorder Quantity", placeholder="Enter reorder quantity..."),
            pn.widgets.TextInput(name="Order Link", placeholder="Enter order link..."),
            pn.widgets.Button(name="Insert Data", button_type="success")
        )
        def insert_data(event):
            try:
                new_row = {
                    "hash_key": insert_form[0].value,
                    "item": insert_form[1].value,
                    "quantity": insert_form[2].value,
                    "location": insert_form[3].value,
                    "subteam": insert_form[4].value,
                    "reorder_quantity": insert_form[5].value,
                    "order_link": insert_form[6].value,
                }
                user_df.loc[len(user_df)] = new_row
                user_df_pane.value = user_df
                history_log.value += f"Inserted row: {new_row}\n"
                for widget in insert_form[:-1]:
                    widget.value = ""

                print("Data inserted into user_df.")

            except Exception as e:
                print(f"Error inserting data: {e}")
        insert_form[-1].on_click(insert_data)
        changed_layout = pn.Column(
            pn.Row(df_panel, user_df_pane),
            save_button,
            insert_form,
            history_log
        )
        layout[:] = [changed_layout]

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if server1:
            server1.close()