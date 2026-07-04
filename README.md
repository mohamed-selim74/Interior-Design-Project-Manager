# 🏢 Interior Design Project Manager (IDMS PRO)

### Project Overview

I developed IDMS PRO, a desktop ERP application designed to streamline interior design project workflows.

A major focus of this project was designing and implementing a relational database from scratch, including ERD design, normalization to 3NF, and Oracle SQL implementation.

The project demonstrates the complete database development lifecycle—from conceptual database design to a fully functional desktop application with a Python GUI integrated with an Oracle Database.

<img width="1917" height="1018" alt="Screenshot 2026-07-04 125948" src="https://github.com/user-attachments/assets/c91d4844-c158-44a1-9b60-02725d60f15b" />

## ✨ Features
- Manage interior design projects.
- Store and manage client information.
- Manage contractors and their assigned projects.
- Track furniture items used in each project.
- Schedule project activities.
- Perform full CRUD operations through a desktop GUI.
- Oracle database integration with real-time updates.
- Database designed from an ERD and normalized to 3NF.


## 🛠️ Key Implementation Details

**1. Database Design:** 
Started with conceptualizing the Entity-Relationship Diagram (ERD) and mapping it into a 3NF relational schema.

<img width="1371" height="772" alt="Screenshot 2026-07-04 143837" src="https://github.com/user-attachments/assets/d053e5ee-bad3-401f-807e-dc026d74b28b" />

<img width="1370" height="792" alt="Screenshot 2026-07-04 143859" src="https://github.com/user-attachments/assets/a215fe17-34ec-4f38-8723-73bd60ea7eaf" />


**2. Database Creation:** 
Wrote the SQL DDL scripts to create tables, define primary/foreign keys, and apply constraints using Oracle Database.

**3. Python GUI:** 
Built a desktop interface using Python (Tkinter) to allow users to perform CRUD operations easily without writing SQL queries.

**4. Integration:** 
Successfully linked the Python application to the Oracle database using the `oracledb` driver to execute operations in real-time.

---
---

## 🛠️ Tech Stack

* **Frontend:** Python (Tkinter GUI with Custom Dark Theme)
* **Backend Database:** Oracle Database (XE)
* **Database Driver:** `oracledb`

## 📁 Repository Structure

* `/design` : Contains the Entity-Relationship Diagram (ERD) and official presentation.
* `/database` : Contains the production-ready DDL SQL scripts (`schema.sql`).
* `/src` : Contains the core Python application source code.

## 🔗 Project Resources

* 📊 **[View Project Presentation](https://drive.google.com/drive/folders/15WJMp6kx4XBw1ff72yvde1l6WFL1ioQ4?usp=sharing)**

## 🚀 How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohamed-selim74/Interior-Design-Project-Manager.git
   pip install oracledb
   python src/main.py
   ```
