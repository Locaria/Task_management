import streamlit as st
import pandas as pd
import hashlib

# Função para gerar hash das senhas
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Banco de dados simples para usuários e projetos
users_db = {
    'IMC': {'password': hash_password('1234'), 'projects': {}}
}

# Função de login
def login():
    st.sidebar.title("Login")
    team_name = st.sidebar.text_input("Team Name")
    password = st.sidebar.text_input("Password", type='password')
    login_button = st.sidebar.button("Login")
    
    if login_button:
        if team_name in users_db and users_db[team_name]['password'] == hash_password(password):
            st.session_state['team'] = team_name
            st.session_state['logged_in'] = True
        else:
            st.sidebar.error("Invalid team name or password")

# Função de logout
def logout():
    st.session_state['logged_in'] = False
    st.session_state['team'] = None

# Função para criar novo projeto
def create_project():
    project_name = st.text_input("Project Name")
    create_button = st.button("Create Project")
    
    if create_button and project_name:
        if project_name not in users_db[st.session_state['team']]['projects']:
            users_db[st.session_state['team']]['projects'][project_name] = {'todo': [], 'in_progress': [], 'done': []}
            st.success(f"Project '{project_name}' created!")
        else:
            st.error(f"Project '{project_name}' already exists!")

# Função para adicionar tarefa ao projeto
def add_task(project_name):
    task = st.text_input("Task Description")
    add_task_button = st.button("Add Task")
    
    if add_task_button and task:
        users_db[st.session_state['team']]['projects'][project_name]['todo'].append(task)
        st.success(f"Task added to project '{project_name}'")

# Função para mover tarefa entre listas
def move_task(project_name, task, from_list, to_list):
    users_db[st.session_state['team']]['projects'][project_name][from_list].remove(task)
    users_db[st.session_state['team']]['projects'][project_name][to_list].append(task)

# Função para mostrar o quadro kanban
def show_kanban(project_name):
    st.header(f"Kanban for Project: {project_name}")
    
    cols = st.columns(3)
    
    with cols[0]:
        st.subheader("To Do")
        for task in users_db[st.session_state['team']]['projects'][project_name]['todo']:
            if st.button(f"Start {task}", key=f"start_{task}"):
                move_task(project_name, task, 'todo', 'in_progress')

    with cols[1]:
        st.subheader("In Progress")
        for task in users_db[st.session_state['team']]['projects'][project_name]['in_progress']:
            if st.button(f"Complete {task}", key=f"complete_{task}"):
                move_task(project_name, task, 'in_progress', 'done')

    with cols[2]:
        st.subheader("Done")
        for task in users_db[st.session_state['team']]['projects'][project_name]['done']:
            st.text(task)

# Main function
def main():
    st.title("Team Task Management Tool")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if st.session_state['logged_in']:
        st.sidebar.title("Menu")
        st.sidebar.button("Logout", on_click=logout)
        
        create_project()
        
        team_projects = users_db[st.session_state['team']]['projects']
        
        if team_projects:
            project_name = st.selectbox("Select Project", list(team_projects.keys()))
            add_task(project_name)
            show_kanban(project_name)
        else:
            st.write("No projects yet. Create a new project.")
    else:
        login()

if __name__ == "__main__":
    main()
