import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os
from descriptive import *
from clustering import *
from hypothesis import *
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def connect():
    load_dotenv("passwords.env")

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    return conn

class App(ctk.CTk):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.title("Music Analysis Tool")
        self.geometry("1200x800")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


        # Button for the analysis of genre popularity
        self.btn_genre = ctk.CTkButton(self.sidebar, text="Genre Popularity", command=self.show_genre_graph)
        self.btn_genre.pack(pady=10, padx=10)

        # Button for the clustering analysis in 2D
        self.btn_clustering = ctk.CTkButton(self.sidebar, text="Clustering in 2D", command=self.show_clustering_2d)
        self.btn_clustering.pack(pady=10, padx=10)

        # Button for the clustering analysis in 3D
        self.btn_clustering_3d = ctk.CTkButton(self.sidebar, text="Clustering in 3D", command=self.show_clustering_3d)
        self.btn_clustering_3d.pack(pady=10, padx=10)

        # Button for user information
        self.btn_user = ctk.CTkButton(self.sidebar, text="User Management", command=self.show_user_management_view)
        self.btn_user.pack(pady=10, padx=10)

        self.container_frame = ctk.CTkFrame(self)
        self.container_frame.grid(row = 0, column=1, padx=20, pady=20, sticky="nsew")

        self.current_canvas = None

    def show_genre_graph(self):

        fig = genre_popularity(self.conn)

        self.draw_figure(fig)

    def show_user_management_view(self):

        for widget in self.container_frame.winfo_children():
            widget.destroy()

        total, max_id = get_users_stats(self.conn)

        ctk.CTkLabel(self.container_frame, text="User Management", font=("Arial", 24)).pack(pady=10)
        ctk.CTkLabel(self.container_frame, text=f"Total users: {total} | Max ID: {max_id}").pack(pady=5)

        view_frame = ctk.CTkFrame(self.container_frame)
        view_frame.pack(pady=20, padx=20, fill="x")

        self.user_id_entry = ctk.CTkEntry(view_frame, placeholder_text="Enter User ID")
        self.user_id_entry.pack(side="left", padx=10, pady=10)

        ctk.CTkButton(view_frame, text="View User", command=self.handle_view_user).pack(side="left", padx=10)

        create_frame = ctk.CTkFrame(self.container_frame)
        create_frame.pack(pady=20, padx=20, fill="x")

        self.new_name_entry = ctk.CTkEntry(create_frame, placeholder_text="Username")
        self.new_name_entry.pack(pady=5)

        self.sub_menu = ctk.CTkOptionMenu(create_frame, values=["free", "premium", "family"])
        self.sub_menu.pack(pady=5)

        ctk.CTkButton(create_frame, text="Create New User", fg_color="green", command=self.handle_create_user).pack(pady=10)

        self.result_box = ctk.CTkTextbox(self.container_frame, height=150)
        self.result_box.pack(pady=10, padx=20, fill="both", expand=True)

    def handle_view_user(self):
        uid = self.user_id_entry.get()
        df = get_user_info(self.conn, uid)
        self.result_box.delete("0.0", "end")
        if df.empty:
            self.result_box.insert("0.0", f"No user found with ID {uid}")
        else:
            self.result_box.insert("0.0", df.to_string(index=False))

    def handle_create_user(self):
        name = self.new_name_entry.get()
        sub = self.sub_menu.get()
        success, msg = create_a_user_gui(self.conn, name, sub)
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", msg)
        if success:
            self.new_name_entry.delete(0, "end")

    def show_clustering_2d(self):

        fig = behavior_analysis(self.conn)

        self.draw_figure(fig)

    def show_clustering_3d(self):

        fig = behavior_analysis_3d(self.conn)

        self.draw_figure(fig)



    def draw_figure(self, fig):

        for widget in self.container_frame.winfo_children():
            widget.destroy()

        self.current_canvas = FigureCanvasTkAgg(fig, master=self.container_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True)



if __name__ == "__main__":
    conn = connect()
    try:
        app = App(conn)
        app.mainloop()
    finally:
        if conn.is_connected():
            conn.close()
            print("Database connection closed.")