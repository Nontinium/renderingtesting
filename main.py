import flet as ft
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from flet.matplotlib_chart import MatplotlibChart

plt.switch_backend('Agg')

dataframe = None
fig = None
def main(page: ft.Page):
    def pickfiles(e):
        pick_files_dialog.pick_files(allow_multiple=False, allowed_extensions= ["csv", "xlsx", "xls"])
         # Handle the selected file here

    def files_are_picked(e: ft.FilePickerResultEvent):
        global dataframe
        if e.files:
            print("Files picked:", e.files)
            file = e.files[0]
            file_path = file.path
            print("File path:", file_path)

            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.csv':
                dataframe = pd.read_csv(file_path)
                print(dataframe.head())
            elif file_extension in ['.xlsx', '.xls']:
                dataframe = pd.read_excel(file_path)
                print(dataframe.head())
            else:
                print("Unsupported file type")
                return
            
            x_axis.options = [ft.dropdown.Option(col) for col in dataframe.columns]
            y_axis.options = [ft.dropdown.Option(col) for col in dataframe.columns]
            page.update()
            

    def type_of_graph_rendered(e):
        global fig
        if dataframe is not None:
            if type_of_graph.value == "line plot":
                fig, ax = plt.subplots()
                sns.lineplot(data= dataframe, x = x_axis.value, y = y_axis.value, ax = ax)
                graph_container.content = MatplotlibChart(fig, expand=True)
                page.update()
            




    pick_files_dialog = ft.FilePicker(on_result=files_are_picked)
    page.overlay.append(pick_files_dialog)
    
    button = ft.IconButton(icon=ft.icons.ADD, on_click=pickfiles)



    type_of_data = ft.Dropdown(label =  "Type of Data",options=[
        ft.dropdown.Option("CSV"),
        ft.dropdown.Option("XLSX"),
        ft.dropdown.Option("XLS"),
    ])

    type_of_graph = ft.Dropdown(label =  "Type of Graph",options=[
        ft.dropdown.Option("line plot"),
        ft.dropdown.Option("scatter plot"),
        ft.dropdown.Option("bar plot"),
    ] ,on_change= type_of_graph_rendered)

    x_axis = ft.Dropdown(label =  "X axis",options=[], on_change= type_of_graph_rendered)
    y_axis = ft.Dropdown(label =  "Y axis",options=[], on_change= type_of_graph_rendered)

    x_axis_label = ft.TextField(label="X axis label", hint_text="Please enter the name of X axis")
    y_axis_label = ft.TextField(label="Y axis label", hint_text="Please enter the name of Y axis")


    graph_container = ft.Container(expand=True)

    page.add(ft.Column(controls=[button, type_of_graph, x_axis, y_axis, graph_container], expand= True, spacing=10))


ft.app(main)
