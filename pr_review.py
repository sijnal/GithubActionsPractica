import os
import requests
from github import Github

# Configuración del cliente de GitHub
token = os.getenv("MY_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")
pr_number = int(os.getenv("PR_NUMBER"))

g = Github(token)
repo = g.get_repo(repo_name)
pr = repo.get_pull(pr_number)

# Obtener título y descripción del PR
pr_title = pr.title
pr_body = pr.body

# Obtener los cambios de los archivos
files = pr.get_files()

# Construir el contenido para enviar a Google AI Studio
def prepare_changes(files):
    changes = []
    for file in files:
        filename = file.filename
        patch = file.patch  # El diff del archivo
        changes.append({"filename": filename, "patch": patch or ""})
    return changes

# Enviar datos a la API de Google AI Studio
def analyze_with_google_ai(title, body, changes):
    payload = {
        "title": title,
        "description": body or "No description provided.",
        "changes": changes
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('GOOGLE_AI_API_KEY')}",
        "Content-Type": "application/json"
    }
    google_ai_api_url = os.getenv("GOOGLE_AI_API_URL")  # URL de la API desde la variable de entorno
    response = requests.post(google_ai_api_url, json=payload, headers=headers)
    response.raise_for_status()  # Lanza un error si la solicitud falla
    return response.json()

# Publicar un comentario en el PR
def post_comment(pr, comment):
    if comment:
        pr.create_issue_comment(comment)

if __name__ == "__main__":
    try:
        # Preparar los cambios para análisis
        changes = prepare_changes(files)

        # Enviar a la API de Google AI Studio para análisis
        analysis_result = analyze_with_google_ai(pr_title, pr_body, changes)

        # Procesar la respuesta de Google AI Studio
        google_comments = analysis_result.get("comments", [])
        if google_comments:
            # Unir los comentarios en un bloque único
            final_comment = "\n\n".join(google_comments)
            post_comment(pr, final_comment)
            print("Comentario publicado con éxito.")
        else:
            print("No se encontraron problemas relevantes en el análisis.")
    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API de Google AI Studio: {e}")
