import tkinter as tk
from tkinter import ttk, messagebox
import oracledb
import os
from datetime import datetime


class DatabaseEngine:
    def __init__(self):
        self.lib_path = r"C:\oracle\instantclient_23_0" 
        self.config = {"user": "mohammed", "password": "123", "dsn": "localhost:1521/xe"}
        try:
            if os.path.exists(self.lib_path):
                oracledb.init_oracle_client(lib_dir=self.lib_path)
        except Exception as e: print(f"Oracle Client Notice: {e}")

    def execute(self, sql, params=(), fetch=False):
        conn = None
        try:
            conn = oracledb.connect(**self.config)
            cursor = conn.cursor()
            cursor.execute(sql, params)
            if fetch:
                res = cursor.fetchall()
                return res
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            messagebox.showerror("Database Error", f"exist technical error:\n{e}")
            return False
        finally:
            if conn: conn.close()

# ==========================================
# 2. THE ULTIMATE MASTER ERP SYSTEM
# ==========================================
class IDMS_Full_ERP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interior Design Project Manager")
        self.geometry("1450x850")
        self.db = DatabaseEngine()
        self.configure(bg="#1e1e1e")

        # Sidebar layout configuration
        self.sidebar = tk.Frame(self, bg="#121212", width=250)
        self.sidebar.pack_propagate(False) # Prevents the sidebar from resizing automatically
        self.sidebar.pack(side="left", fill="y")
        
        tk.Label(self.sidebar, text="IDMS PRO", font=("Segoe UI", 25, "bold"), 
                 bg="#121212", fg="#00d4ff").pack(pady=40)
        
        style = ttk.Style()
        style.theme_use("clam") # Enables better color customization options
        
        # Treeview (Table) styling
        style.configure("Treeview", background="#2d2d2d", foreground="white", 
                        fieldbackground="#2d2d2d", borderwidth=0, font=("Arial", 12))
        style.configure("Treeview.Heading", background="#3d3d3d", foreground="white", 
                        font=("Arial", 14, "bold"))
        style.map("Treeview", background=[('selected', '#0078d7')]) # Selection background color
        
        # Entry and LabelFrame styling
        style.configure("TLabelframe", background="#1e1e1e", foreground="white")
        style.configure("TLabelframe.Label", background="#1e1e1e", foreground="#00d4ff", font=("Arial", 12, "bold"))
        style.configure("TLabel", background="#1e1e1e", foreground="white")

        menu = [
            ("🏗️ Projects", self.show_projects),
            ("👷 Contractors", self.show_contractors),
            ("🛋️ Furniture", self.show_furniture),
            ("🧵 Fabrics (Swatches)", self.show_fabrics),
            ("📅 Schedule", self.show_schedule),
            ("🔗 Project_Furniture", self.show_proj_furn),
            ("👥 Project_Contractor", self.show_proj_cont),
            ("📱 Contractor_Phones", self.show_contractor_phones),
        ]
        
        for name, cmd in menu:
            tk.Button(self.sidebar, text=name, font=("Segoe UI", 12), 
                      bg="#1e1e1e", fg="#ecf0f1", activebackground="#00d4ff", 
                      activeforeground="black", relief="flat", cursor="hand2", 
                      anchor="w", padx=20, command=cmd).pack(fill="x", pady=5, padx=10, ipady=8)

        self.container = tk.Frame(self, bg="#1e1e1e")
        self.container.pack(side="right", fill="both", expand=True)
        self.show_projects()
    def clear(self):
        for w in self.container.winfo_children(): w.destroy()

    def create_table(self, parent, cols):
        f = tk.Frame(parent, bg="#1e1e1e") 
        f.pack(fill="both", expand=True, pady=10)
        
        # --- Layout adjustment: Create and pack the footer label at the bottom first ---
        count_lbl = tk.Label(f, text="Count: 0", font=("Arial", 11, "bold"), 
                             bg="#1e1e1e", fg="#00d4ff")
        count_lbl.pack(side="bottom", anchor="e", pady=5) 

        # --- Then place the treeview table above it ---
        tree = ttk.Treeview(f, columns=cols, show="headings")
        for c in cols: 
            tree.heading(c, text=c)
            tree.column(c, anchor="center")
            
        scroll = ttk.Scrollbar(f, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Bind the footer label to the treeview for dynamic row counting
        tree.footer_label = count_lbl 
        
        return tree
    
    # --- 🏗️ 1. PROJECTS CRUD ---
    def show_projects(self):
        self.clear()
        f = tk.Frame(self.container, bg="#1e1e1e") 
        f.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(f, text="Project Management ", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="#00d4ff").pack(pady=15)
        
        form = ttk.LabelFrame(f); form.pack(fill="x")
        
        lbl_font = ("Arial", 12, "bold")
        ent_font = ("Arial", 12)
        fields = ["ID", "Name", "Client", "Budget", "Date"]
        self.p_ents = {field: ttk.Entry(form, width=15) for field in fields}
        for i, (fld, ent) in enumerate(self.p_ents.items()):
            ttk.Label(form, text=fld).grid(row=0, column=i*2, padx=5, pady=10); ent.grid(row=0, column=i*2+1)
        btn_f = tk.Frame(form); btn_f.grid(row=1, column=0, columnspan=10, pady=10)
        # Professional buttons with distinct colors
        tk.Button(btn_f, text="+ Add", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.add_p).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="📝 Update", bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.upd_p).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="🗑️ Delete", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.del_p).pack(side="left", padx=5)
        self.p_tree = self.create_table(f, ("ID", "Name", "Client", "Budget", "Date"))
        self.p_tree.bind("<<TreeviewSelect>>", self.on_p_sel)
        self.ref_p()

    def ref_p(self):
        for r in self.p_tree.get_children(): self.p_tree.delete(r)
        d = self.db.execute("SELECT ProjectID, ProjectName, ClientName, Budget, TO_CHAR(StartDate, 'DD-MM-YYYY') FROM PROJECT", fetch=True)
        for x in d: self.p_tree.insert("", "end", values=x)
        total_rows = len(self.p_tree.get_children())
        self.p_tree.footer_label.config(text=f"Total Projects: {total_rows}")

    def add_p(self):
        v = [e.get() for e in self.p_ents.values()]
        if self.db.execute("INSERT INTO PROJECT VALUES (:1, :2, :3, :4, TO_DATE(:5, 'DD-MM-YYYY'))", v): 
            self.ref_p()
            messagebox.showinfo("Success", "Project Added Successfully! ✅")

    def upd_p(self):
        vals = (self.p_ents["Name"].get(), self.p_ents["Client"].get(), self.p_ents["Budget"].get(), self.p_ents["Date"].get(),  self.p_ents["ID"].get())
        sql = "UPDATE PROJECT SET ProjectName=:1, ClientName=:2, Budget=:3, StartDate=TO_DATE(:4, 'DD-MM-YYYY') WHERE ProjectID=:5"
        res = self.db.execute(sql, vals)
        # If res >= 1 (ID exists and record was updated)
        if isinstance(res, int) and res > 0:
            messagebox.showinfo("Success", "Project Updated Successfully ✅")
            self.ref_p()
        else:
            # If res == 0 (Oracle did not find this ID in the table)
            messagebox.showwarning("Warning", "ID NOT EXIST! ❌")

    def del_p(self):
        p_id = self.p_ents["ID"].get().strip()
        if not p_id: 
            messagebox.showwarning("Warning", "Please enter/select an ID to delete!")
            return
            
        if messagebox.askyesno("Confirm", f"Delete project {p_id} and all its related data?"):
            # 1. Delete dependent records in child tables
            self.db.execute("DELETE FROM SCHEDULE WHERE ProjectID=:1", (p_id,))
            self.db.execute("DELETE FROM PROJECT_FURNITURE WHERE ProjectID=:1", (p_id,))
            self.db.execute("DELETE FROM PROJECT_CONTRACTOR WHERE ProjectID=:1", (p_id,))
            
            res = self.db.execute("DELETE FROM PROJECT WHERE ProjectID=:1", (p_id,))
            
            if isinstance(res, int) and res > 0:
                messagebox.showinfo("Success", "Project Deleted Successfully! ✅")
                self.ref_p() # Refresh the table view
                # Clear entry fields after deletion
                for f in self.p_ents: 
                    self.p_ents[f].delete(0, 'end')
            else:
                messagebox.showwarning("Not Found", "This ID does not exist! ❌")

    def on_p_sel(self, e):
        s = self.p_tree.focus()
        if s:
            vals = self.p_tree.item(s)['values']
            for i, f in enumerate(self.p_ents): self.p_ents[f].delete(0, 'end'), self.p_ents[f].insert(0, vals[i])

    # --- 👷 2. CONTRACTORS CRUD ---
    def show_contractors(self):
        self.clear()
        f = tk.Frame(self.container, bg="#1e1e1e") 
        f.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(f, text="Contractor Management ", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="#00d4ff").pack(pady=15)
        
        form = ttk.LabelFrame(f); form.pack(fill="x")
        
        lbl_font = ("Arial", 12, "bold")
        ent_font = ("Arial", 12)
        fields = ["ID", "First", "Last", "Specialty"]
        self.c_ents = {field: ttk.Entry(form, width=15) for field in fields}
        for i, (fld, ent) in enumerate(self.c_ents.items()):
            ttk.Label(form, text=fld).grid(row=0, column=i*2, padx=5, pady=10); ent.grid(row=0, column=i*2+1)
        btn_f = tk.Frame(form); btn_f.grid(row=1, column=0, columnspan=10, pady=10)
        
        tk.Button(btn_f, text="+ Add", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.add_c).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="📝 Update", bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.upd_c).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="🗑️ Delete", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.del_c).pack(side="left", padx=5)
        self.c_tree = self.create_table(f, ("ID", "First", "Last", "Specialty"))
        self.c_tree.bind("<<TreeviewSelect>>", self.on_c_sel)
        self.ref_c()

    def ref_c(self):
        for r in self.c_tree.get_children(): self.c_tree.delete(r)
        d = self.db.execute("SELECT * FROM CONTRACTOR", fetch=True)
        for x in d: self.c_tree.insert("", "end", values=x)
        count = len(self.c_tree.get_children())
        self.c_tree.footer_label.config(text=f"Total Contractors: {count}")

    def add_c(self):
        v = [e.get() for e in self.c_ents.values()]
        if self.db.execute("INSERT INTO CONTRACTOR VALUES (:1, :2, :3, :4)", v):
            self.ref_c()
            messagebox.showinfo("Success", "CONTRACTOR Added Successfully! ✅")

    def upd_c(self):
        vals = (self.c_ents["First"].get(), self.c_ents["Last"].get(), self.c_ents["Specialty"].get(), self.c_ents["ID"].get())
        sql = "UPDATE CONTRACTOR SET FName=:1, LName=:2, Specialty=:3 WHERE ContractorID=:4"
        res = self.db.execute(sql, vals)
        if isinstance(res, int) and res > 0:
            messagebox.showinfo("Success", "CONTRACTOR Updated Successfully ✅")
            self.ref_c()
        else:
            # If res == 0 (Oracle did not find this ID in the table)
            messagebox.showwarning("Warning", "CONTRACTORID NOT EXIST! ❌")
            
    
    def del_c(self):
        c_id = self.c_ents["ID"].get()
        if not c_id:
            messagebox.showwarning("Warning", "Please enter/select an ID to delete!")
            return
        if messagebox.askyesno("Confirm", f"Delete CONTRACTOR  {c_id} and all its related data? "):
            self.db.execute("DELETE FROM CONTRACTOR_PHONE WHERE ContractorID=:1", (c_id,))
            self.db.execute("DELETE FROM PROJECT_CONTRACTOR WHERE ContractorID=:1", (c_id,))
            self.db.execute("DELETE FROM SCHEDULE WHERE ContractorID=:1", (c_id,))
            res = self.db.execute("DELETE FROM CONTRACTOR WHERE ContractorID=:1", (c_id,))
            if isinstance(res, int) and res > 0:
                messagebox.showinfo("Success", "CONTRACTOR Deleted Successfully! ✅")
                self.ref_c() # Refresh the table view
                # Clear entry fields after deletion
                for f in self.p_ents: 
                    self.p_ents[f].delete(0, 'end')
            else:
                messagebox.showwarning("Not Found", "This ID does not exist! ❌") 
                
          

    def on_c_sel(self, e):
        s = self.c_tree.focus()
        if s:
            vals = self.c_tree.item(s)['values']
            for i, f in enumerate(self.c_ents): self.c_ents[f].delete(0, 'end'), self.c_ents[f].insert(0, vals[i])

    # --- 🛋️ 3. FURNITURE CRUD ---
    def show_furniture(self):
        
        self.clear()
        f = tk.Frame(self.container, bg="#1e1e1e") 
        f.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(f, text="Furniture Controls ", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="#00d4ff").pack(pady=15)
        
        form = ttk.LabelFrame(f); form.pack(fill="x")
        
        lbl_font = ("Arial", 12, "bold")
        ent_font = ("Arial", 12)
        ttk.Label(form, text="SKU").grid(row=0, column=0); self.f_sku = ttk.Entry(form); self.f_sku.grid(row=0, column=1)
        ttk.Label(form, text="Desc").grid(row=0, column=2); self.f_desc = ttk.Entry(form); self.f_desc.grid(row=0, column=3)
        ttk.Label(form, text="Price").grid(row=1, column=0); self.f_pr = ttk.Entry(form); self.f_pr.grid(row=1, column=1, pady=10)
        ttk.Label(form, text="Fabric").grid(row=1, column=2); self.f_sw = ttk.Combobox(form, state="readonly"); self.f_sw.grid(row=1, column=3)
        btn_f = tk.Frame(form); btn_f.grid(row=2, column=0, columnspan=4, pady=10)
        
        tk.Button(btn_f, text="+ Add SKU", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.add_f).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="📝 Update", bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.upd_f).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="🗑️ Delete", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.del_f).pack(side="left", padx=5)
        self.f_tree = self.create_table(f, ("SKU", "Description", "Price", "SwatchID"))
        self.f_tree.bind("<<TreeviewSelect>>", self.on_f_sel)
        self.ref_f()

    def ref_f(self):
        for r in self.f_tree.get_children(): self.f_tree.delete(r)
        d = self.db.execute("SELECT * FROM FURNITURE", fetch=True)
        for x in d: self.f_tree.insert("", "end", values=x)
        sw = self.db.execute("SELECT SwatchID, MaterialType FROM FABRIC", fetch=True)
        self.f_sw['values'] = [f"{s[0]} - {s[1]}" for s in sw]
        count = len(self.f_tree.get_children())
        self.f_tree.footer_label.config(text=f"Total Furniture Items: {count}")

    def add_f(self):
        v = (self.f_sku.get(), self.f_desc.get(), self.f_pr.get(), self.f_sw.get().split(" - ")[0])
        if self.db.execute("INSERT INTO FURNITURE VALUES (:1, :2, :3, :4)", v): self.ref_f()

    def upd_f(self):
        sku = self.f_sku.get().strip()
        sw_id = self.f_sw.get().split(" - ")[0]
        vals = (self.f_desc.get(), self.f_pr.get(), sw_id, sku)
        sql = "UPDATE FURNITURE SET Description=:1, Price=:2, SwatchID=:3 WHERE SKU=:4"
        res = self.db.execute(sql, vals)
        
        # Immediately refresh the furniture table and combobox
        if isinstance(res, int) and res > 0:
            messagebox.showinfo("Success", "Furniture Updated Successfully ✅")
            self.ref_f() 
        else:
            # If res is 0, the specified SKU does not exist in the database
            messagebox.showwarning("Warning", "Furniture SKU Not Found! ❌")

    def del_f(self):
        # 1. Retrieve and strip the SKU field
        sku = self.f_sku.get().strip()
        
        # 2. Guard clause: exit if the SKU field is empty
        if not sku:
            messagebox.showwarning("Warning", "Please enter/select SKU to delete!")
            return

        # 3. Confirm deletion with the user
        if messagebox.askyesno("Confirm", f"Delete Furniture SKU: {sku} from all projects?"):
            
            # 4. Delete dependent records first to maintain referential integrity
            # Remove entries from the project-furniture intersection table
            self.db.execute("DELETE FROM PROJECT_FURNITURE WHERE SKU=:1", (sku,))
            
            # 5. Delete the parent record from the core Furniture table
            res = self.db.execute("DELETE FROM FURNITURE WHERE SKU=:1", (sku,))
            
            # 6. Validate operation using rowcount (res)
            if isinstance(res, int) and res > 0:
                messagebox.showinfo("Success", "Furniture Deleted Successfully ✅")
                self.ref_f() # Refresh the table view
                # Clear entry fields after deletion
                for f in [self.f_sku, self.f_desc, self.f_pr, self.f_sw]:
                    if hasattr(f, 'delete'): f.delete(0, 'end')
                    else: f.set('') # For Combobox widgets
            else:
                messagebox.showwarning("Not Found", "SKU does not exist! ❌")

    def on_f_sel(self, e):
        s = self.f_tree.focus()
        if s:
            v = self.f_tree.item(s)['values']
            self.f_sku.delete(0,'end'); self.f_sku.insert(0,v[0])
            self.f_desc.delete(0,'end'); self.f_desc.insert(0,v[1])
            self.f_pr.delete(0,'end'); self.f_pr.insert(0,v[2])

    # --- 🧵 4. FABRICS (SWATCHES) CRUD ---
    def show_fabrics(self):
        self.clear()
        f = tk.Frame(self.container, bg="#1e1e1e") 
        f.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(f, text="Fabric Controls ", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="#00d4ff").pack(pady=15)
        
        form = ttk.LabelFrame(f); form.pack(fill="x")
        
        lbl_font = ("Arial", 12, "bold")
        ent_font = ("Arial", 12)
        fields = ["ID", "Material", "Color"]
        self.sw_ents = {field: ttk.Entry(form) for field in fields}
        for i, (fld, ent) in enumerate(self.sw_ents.items()):
            ttk.Label(form, text=fld).grid(row=0, column=i*2, padx=5, pady=10); ent.grid(row=0, column=i*2+1)
        btn_f = tk.Frame(form); btn_f.grid(row=1, column=0, columnspan=6, pady=10)
        
        tk.Button(btn_f, text="+ Add Fabric", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.add_sw).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="📝 Update", bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.upd_sw).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="🗑️ Delete", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.del_sw).pack(side="left", padx=5)
        self.sw_tree = self.create_table(f, ("ID", "Material", "Color"))
        self.sw_tree.bind("<<TreeviewSelect>>", self.on_sw_sel)
        self.ref_sw()

    def ref_sw(self):
        for r in self.sw_tree.get_children(): self.sw_tree.delete(r)
        d = self.db.execute("SELECT * FROM FABRIC", fetch=True)
        for x in d: self.sw_tree.insert("", "end", values=x)
        count = len(self.sw_tree.get_children())
        self.sw_tree.footer_label.config(text=f"Total Fabrics: {count}")
    def add_sw(self):
        v = (self.sw_ents["ID"].get(), self.sw_ents["Material"].get(), self.sw_ents["Color"].get())
        if self.db.execute("INSERT INTO FABRIC VALUES (:1, :2, :3)", v): self.ref_sw()


    def upd_sw(self):
        # 1. Retrieve and strip the Swatch ID
        sw_id = self.sw_ents["ID"].get().strip()
        
        # 2. Prepare parameters tuple (vals) with updated records
        vals = (self.sw_ents["Material"].get(), 
                self.sw_ents["Color"].get(), 
                sw_id)
        
        # 3. Execute statement and capture response status (res)
        sql = "UPDATE FABRIC SET MaterialType=:1, ColorCode=:2 WHERE SwatchID=:3"
        res = self.db.execute(sql, vals)
        
        # 4. Standardized verification logic
        if isinstance(res, int) and res > 0:
            messagebox.showinfo("Success", "Fabric Swatch Updated Successfully ✅")
            self.ref_sw()  # Immediately refresh the table and associated menus
        else:
            # If Oracle did not find the specified SwatchID
            messagebox.showwarning("Warning", "Swatch ID Not Found! ❌")

    
    

    def del_sw(self):
        # 1. Retrieve and strip the Swatch ID
        sid = self.sw_ents["ID"].get().strip()
        
        # 2. Guard clause: Ensure the ID field is not empty
        if not sid:
            messagebox.showwarning("Warning", "Please enter/select a Swatch ID to delete!")
            return

        # 3. Confirm deletion prompt for the user
        if messagebox.askyesno("Confirm", f"Delete Fabric Swatch {sid}? \n(Note: Furniture using this fabric will be set to NULL)"):
            
            # 4. Decouple relationship: Set associated furniture fabric to NULL instead of cascading delete
            self.db.execute("UPDATE FURNITURE SET SwatchID = NULL WHERE SwatchID=:1", (sid,))
            
            # 5. Delete the fabric record from the FABRIC table
            res = self.db.execute("DELETE FROM FABRIC WHERE SwatchID=:1", (sid,))
            
            # 6. Validate execution via rowcount (res)
            if isinstance(res, int) and res > 0:
                messagebox.showinfo("Success", "Fabric Deleted Successfully ✅")
                self.ref_sw() # Refresh the table and associated menus
                # Clear entry fields
                for f in self.sw_ents: self.sw_ents[f].delete(0, 'end')
            else:
                messagebox.showwarning("Not Found", "Swatch ID does not exist! ❌")

    def on_sw_sel(self, e):
        s = self.sw_tree.focus()
        if s:
            v = self.sw_tree.item(s)['values']
            for i, f in enumerate(self.sw_ents): self.sw_ents[f].delete(0,'end'), self.sw_ents[f].insert(0,v[i])

    # --- 📅 5. SCHEDULE CRUD ---
    def show_schedule(self):
        
        self.clear()
        f = tk.Frame(self.container, bg="#1e1e1e") 
        f.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(f, text="Task Controls", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="#00d4ff").pack(pady=15)
        
        form = ttk.LabelFrame(f); form.pack(fill="x")
        
        lbl_font = ("Arial", 12, "bold")
        ent_font = ("Arial", 12)
        ttk.Label(form, text="T_ID").grid(row=0, column=0); self.s_id = ttk.Entry(form, width=10); self.s_id.grid(row=0, column=1)
        ttk.Label(form, text="Project").grid(row=0, column=2); self.s_p = ttk.Combobox(form, state="readonly"); self.s_p.grid(row=0, column=3)
        ttk.Label(form, text="Task").grid(row=1, column=0); self.s_ds = ttk.Entry(form); self.s_ds.grid(row=1, column=1, pady=5)
        ttk.Label(form, text="Date").grid(row=1, column=2); self.s_dt = ttk.Entry(form); self.s_dt.grid(row=1, column=3)
        ttk.Label(form, text="Status").grid(row=2, column=0); self.s_st = ttk.Combobox(form, values=["Pending", "In Progress", "Done"], state="readonly"); self.s_st.grid(row=2, column=1)
        ttk.Label(form, text="Contr.").grid(row=2, column=2); self.s_c = ttk.Combobox(form, state="readonly"); self.s_c.grid(row=2, column=3)
        btn_f = tk.Frame(form); btn_f.grid(row=3, column=0, columnspan=4, pady=10)
        
        tk.Button(btn_f, text="+ Add Task", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.add_s).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="📝 Update", bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.upd_s).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="🗑️ Delete", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=12, command=self.del_s).pack(side="left", padx=5)
        self.s_tree = self.create_table(f, ("T_ID", "P_ID", "Task", "Date", "Status", "C_ID"))
        self.s_tree.bind("<<TreeviewSelect>>", self.on_s_sel)
        self.ref_s()

    def ref_s(self):
        for r in self.s_tree.get_children(): self.s_tree.delete(r)
        d = self.db.execute("SELECT TaskID, ProjectID, TaskDescription, TO_CHAR(TaskDate, 'DD-MM-YYYY'), Status, ContractorID FROM SCHEDULE", fetch=True)
        for x in d: self.s_tree.insert("", "end", values=x)
        pr = self.db.execute("SELECT ProjectID, ProjectName FROM PROJECT", fetch=True); self.s_p['values'] = [f"{x[0]} - {x[1]}" for x in pr]
        co = self.db.execute("SELECT ContractorID, FName FROM CONTRACTOR", fetch=True); self.s_c['values'] = [f"{x[0]} - {x[1]}" for x in co]
        count = len(self.s_tree.get_children())
        self.s_tree.footer_label.config(text=f"Total Tasks: {count}")

    def add_s(self):
        v = (self.s_id.get(), self.s_p.get().split(" - ")[0], self.s_ds.get(), self.s_dt.get(), self.s_st.get(), self.s_c.get().split(" - ")[0])
        if self.db.execute("INSERT INTO SCHEDULE VALUES (:1, :2, :3, TO_DATE(:4, 'DD-MM-YYYY'), :5, :6)", v): self.ref_s()

    def upd_s(self):
        tid = self.s_id.get().strip()
        pid = self.s_p.get().split(" - ")[0]
        vals = (self.s_ds.get(), self.s_dt.get(), self.s_st.get(), self.s_c.get().split(" - ")[0], tid, pid)
        sql = "UPDATE SCHEDULE SET TaskDescription=:1, TaskDate=TO_DATE(:2, 'DD-MM-YYYY'), Status=:3, ContractorID=:4 WHERE TaskID=:5 AND ProjectID=:6"
        if self.db.execute(sql, vals): self.ref_s()

    def del_s(self):
        tid = self.s_id.get(); pid = self.s_p.get().split(" - ")[0]
        if self.db.execute("DELETE FROM SCHEDULE WHERE TaskID=:1 AND ProjectID=:2", (tid, pid)): self.ref_s()

    def on_s_sel(self, e):
        s = self.s_tree.focus()
        if s:
            v = self.s_tree.item(s)['values']
            self.s_id.delete(0,'end'); self.s_id.insert(0,v[0]); self.s_ds.delete(0,'end'); self.s_ds.insert(0,v[2])
            self.s_dt.delete(0,'end'); self.s_dt.insert(0,v[3]); self.s_st.set(v[4])

    # --- 🔗 6. PROJECT FURNITURE LINKER ---
    def show_proj_furn(self):
         self.clear()
         f = tk.Frame(self.container, bg="#1e1e1e") 
         f.pack(fill="both", expand=True, padx=20, pady=10)
        
         tk.Label(f, text="Quantity Of Furniture", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="#00d4ff").pack(pady=15)
        
         form = ttk.LabelFrame(f); form.pack(fill="x")
        
         lbl_font = ("Arial", 12, "bold")
         ent_font = ("Arial", 12)
        
         ttk.Label(form, text="Project").grid(row=0, column=0); self.pf_p = ttk.Combobox(form, state="readonly"); self.pf_p.grid(row=0, column=1, padx=10, pady=10)
         ttk.Label(form, text="Furniture").grid(row=0, column=2); self.pf_f = ttk.Combobox(form, state="readonly"); self.pf_f.grid(row=0, column=3, padx=10)
         ttk.Label(form, text="Quantity").grid(row=0, column=4); self.pf_q = ttk.Entry(form, width=10); self.pf_q.grid(row=0, column=5, padx=10)
         btn_f = tk.Frame(form); btn_f.grid(row=1, column=0, columnspan=7, pady=10)
         tk.Button(btn_f, text="🔗 Link", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=15, command=self.add_pf).pack(side="left", padx=5)
         tk.Button(btn_f, text="📝 Update Quantity", bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=15, command=self.upd_pf).pack(side="left", padx=5)
         tk.Button(btn_f, text="❌ Remove", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=15, command=self.del_pf).pack(side="left", padx=5)
         self.pf_tree = self.create_table(f, ("Project Name", "Furniture Describtion", "Quantity"))
         self.ref_pf()

    def ref_pf(self):
        for r in self.pf_tree.get_children(): self.pf_tree.delete(r)
        sql = "SELECT P.ProjectName, F.Description, PF.Quantity FROM PROJECT_FURNITURE PF JOIN PROJECT P ON PF.ProjectID = P.ProjectID JOIN FURNITURE F ON PF.SKU = F.SKU"
        d = self.db.execute(sql, fetch=True)
        for x in d: self.pf_tree.insert("", "end", values=x)
        pr = self.db.execute("SELECT ProjectID, ProjectName FROM PROJECT", fetch=True); self.pf_p['values'] = [f"{x[0]} - {x[1]}" for x in pr]
        fu = self.db.execute("SELECT SKU, Description FROM FURNITURE", fetch=True); self.pf_f['values'] = [f"{x[0]} - {x[1]}" for x in fu]
        count = len(self.pf_tree.get_children())
        self.pf_tree.footer_label.config(text=f"Total Linked Furniture: {count}")

    def add_pf(self):
        v = (self.pf_p.get().split(" - ")[0], self.pf_f.get().split(" - ")[0], self.pf_q.get())
        if self.db.execute("INSERT INTO PROJECT_FURNITURE VALUES (:1, :2, :3)", v): self.ref_pf()

    def upd_pf(self):
        pid = self.pf_p.get().split(" - ")[0]; sku = self.pf_f.get().split(" - ")[0]
        v = (self.pf_q.get(), pid, sku)
        if self.db.execute("UPDATE PROJECT_FURNITURE SET Quantity=:1 WHERE ProjectID=:2 AND SKU=:3", v): self.ref_pf()

    def del_pf(self):
        v = (self.pf_p.get().split(" - ")[0], self.pf_f.get().split(" - ")[0])
        if self.db.execute("DELETE FROM PROJECT_FURNITURE WHERE ProjectID=:1 AND SKU=:2", v): self.ref_pf()

    # --- 👥 7. PROJECT CONTRACTOR (TEAM) ---
    def show_proj_cont(self):
        
        self.clear()
        f = tk.Frame(self.container, bg="#1e1e1e") 
        f.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(f, text="Assign / Update Team", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="#00d4ff").pack(pady=15)
        
        form = ttk.LabelFrame(f); form.pack(fill="x")
        
        lbl_font = ("Arial", 12, "bold")
        ent_font = ("Arial", 12)
        ttk.Label(form, text="Project").grid(row=0, column=0); self.pc_p = ttk.Combobox(form, state="readonly"); self.pc_p.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(form, text="Contractor").grid(row=0, column=2); self.pc_c = ttk.Combobox(form, state="readonly"); self.pc_c.grid(row=0, column=3, padx=10)
        ttk.Label(form, text="Hours").grid(row=0, column=4); self.pc_h = ttk.Entry(form, width=10); self.pc_h.grid(row=0, column=5, padx=10)
        btn_f = tk.Frame(form); btn_f.grid(row=1, column=0, columnspan=7, pady=10)
        tk.Button(btn_f, text="➕ Assign Team", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=15, command=self.add_pc).pack(side="left", padx=5)
        tk.Button(btn_f, text="📝 Update Hours", bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=15, command=self.upd_pc).pack(side="left", padx=5)
        tk.Button(btn_f, text="❌ Remove", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", width=15, command=self.del_pc).pack(side="left", padx=5)
        self.pc_tree = self.create_table(f, ("Project Name", "Contractor", "Specialty", "Work Hours"))
        self.ref_pc()

    def ref_pc(self):
        for r in self.pc_tree.get_children(): self.pc_tree.delete(r)
        sql = "SELECT P.ProjectName, C.FName || ' ' || C.LName, C.Specialty, PC.WorkHours FROM PROJECT_CONTRACTOR PC JOIN PROJECT P ON PC.ProjectID = P.ProjectID JOIN CONTRACTOR C ON PC.ContractorID = C.ContractorID"
        d = self.db.execute(sql, fetch=True)
        for x in d: self.pc_tree.insert("", "end", values=x)
        pr = self.db.execute("SELECT ProjectID, ProjectName FROM PROJECT", fetch=True); self.pc_p['values'] = [f"{x[0]} - {x[1]}" for x in pr]
        co = self.db.execute("SELECT ContractorID, FName FROM CONTRACTOR", fetch=True); self.pc_c['values'] = [f"{x[0]} - {x[1]}" for x in co]
        count = len(self.pc_tree.get_children())
        self.pc_tree.footer_label.config(text=f"Total Team Assignments: {count}")

    def add_pc(self):
        v = (self.pc_p.get().split(" - ")[0], self.pc_c.get().split(" - ")[0], self.pc_h.get())
        if self.db.execute("INSERT INTO PROJECT_CONTRACTOR VALUES (:1, :2, :3)", v): self.ref_pc()

    def upd_pc(self):
        pid = self.pc_p.get().split(" - ")[0]; cid = self.pc_c.get().split(" - ")[0]
        v = (self.pc_h.get(), pid, cid)
        if self.db.execute("UPDATE PROJECT_CONTRACTOR SET WorkHours=:1 WHERE ProjectID=:2 AND ContractorID=:3", v): self.ref_pc()

    def del_pc(self):
        v = (self.pc_p.get().split(" - ")[0], self.pc_c.get().split(" - ")[0])
        if self.db.execute("DELETE FROM PROJECT_CONTRACTOR WHERE ProjectID=:1 AND ContractorID=:2", v): self.ref_pc()

    # --- 📱 8. CONTRACTOR PHONES SECTION ---
    def show_contractor_phones(self):
        self.clear()
        f = tk.Frame(self.container, bg="#1e1e1e") 
        f.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(f, text="Mangement Contractor Phones", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="#00d4ff").pack(pady=15)
        
        form = ttk.LabelFrame(f); form.pack(fill="x")
        
        lbl_font = ("Arial", 12, "bold")
        ent_font = ("Arial", 12)

        ttk.Label(form, text="Contractor:", font=lbl_font).grid(row=0, column=0, padx=10, pady=20)
        self.cp_c_cb = ttk.Combobox(form, state="readonly", width=35, font=ent_font); self.cp_c_cb.grid(row=0, column=1)
        
        ttk.Label(form, text="Phone Number:", font=lbl_font).grid(row=0, column=2, padx=10)
        self.cp_phone = ttk.Entry(form, width=20, font=ent_font); self.cp_phone.grid(row=0, column=3)
        
        btn_f = tk.Frame(form, bg="#1e1e1e"); btn_f.grid(row=1, column=0, columnspan=4, pady=15)
        
        # Add entry button
        tk.Button(btn_f, text="+ Add Phone", bg="#2ecc71", fg="white", font=("Arial", 12, "bold"),
                  relief="flat", width=15, command=self.add_cp).pack(side="left", padx=5)
        
        # Update entry button
        tk.Button(btn_f, text="📝 Update", bg="#f39c12", fg="white", font=("Arial", 12, "bold"),
                  relief="flat", width=15, command=self.upd_cp).pack(side="left", padx=5)
        
        # Delete/Remove entry button
        tk.Button(btn_f, text="🗑️ Remove", bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                  relief="flat", width=15, command=self.del_cp).pack(side="left", padx=5)

        self.cp_tree = self.create_table(f, ("ID", "Contractor Name", "Phone Number"))
        
        # Critical: Bind treeview row selection to form population method
        self.cp_tree.bind("<<TreeviewSelect>>", self.on_cp_sel)
        
        self.ref_cp()

    def ref_cp(self):
        for r in self.cp_tree.get_children(): self.cp_tree.delete(r)
        sql = """SELECT C.ContractorID, C.FName || ' ' || C.LName, CP.Phone 
                 FROM CONTRACTOR_PHONE CP JOIN CONTRACTOR C ON CP.ContractorID = C.ContractorID 
                 ORDER BY C.ContractorID"""
        data = self.db.execute(sql, fetch=True)
        for d in data: self.cp_tree.insert("", "end", values=d)
        c_list = self.db.execute("SELECT ContractorID, FName || ' ' || LName FROM CONTRACTOR", fetch=True)
        self.cp_c_cb['values'] = [f"{x[0]} - {x[1]}" for x in c_list]
        count = len(self.cp_tree.get_children())
        self.cp_tree.footer_label.config(text=f"Total Phone Numbers: {count}")

    def on_cp_sel(self, e):
        selected = self.cp_tree.focus()
        if selected:
            vals = self.cp_tree.item(selected)['values']
            # Populate the Combobox and Entry widgets
            self.cp_c_cb.set(f"{vals[0]} - {vals[1]}")
            self.cp_phone.delete(0, 'end')
            self.cp_phone.insert(0, vals[2])
            # Cache the old phone number to look up records during an update
            self.old_phone_val = vals[2]
    def add_cp(self):
        try:
            cid = self.cp_c_cb.get().split(" - ")[0]; phone = self.cp_phone.get()
            if cid and phone:
                if self.db.execute("INSERT INTO CONTRACTOR_PHONE VALUES (:1, :2)", (cid, phone)):
                    self.ref_cp(); self.cp_phone.delete(0, 'end')
        except: pass

    def upd_cp(self):
        try:
            selected = self.cp_tree.focus()
            if not selected:
                messagebox.showwarning("EROR❌","CHOOSE THE NUMBER FIRST")
                return
            
            cid = self.cp_c_cb.get().split(" - ")[0]
            new_phone = self.cp_phone.get()
            
            if cid and new_phone:
                # Update phone record matching both ContractorID and cached old number
                sql = "UPDATE CONTRACTOR_PHONE SET Phone=:1 WHERE ContractorID=:2 AND Phone=:3"
                if self.db.execute(sql, (new_phone, cid, self.old_phone_val)):
                    messagebox.showinfo("Success", "UPDATE COMPLETE  ✅")
                    self.ref_cp()
                    self.cp_phone.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"UPDATE FAILLED : {e}")    

    def del_cp(self):
        selected = self.cp_tree.focus()
        if selected:
            vals = self.cp_tree.item(selected)['values']
            if self.db.execute("DELETE FROM CONTRACTOR_PHONE WHERE ContractorID=:1 AND Phone=:2", (vals[0], vals[2])): self.ref_cp()

if __name__ == "__main__":
    app = IDMS_Full_ERP()
    app.mainloop()