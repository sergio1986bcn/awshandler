from utils.repositories.github import github

def crear_repositorio_github():
    repo_name = input("Nombre del repositorio: ")
    description = input("Descripción (opcional): ")
    private_str = input("¿Es privado? (s/n): ").lower()
    private = private_str == "s"

    resp = github().create_repo(repo_name, description, private)

    if resp.status_code == 201:
        print(f"Repositorio creado: {resp.json().get('html_url')}")
    else:
        print(f"Error ({resp.status_code}): {resp.text}")

    input("Pulsa ENTER para continuar...")
