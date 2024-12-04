import os
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

# Generar un análisis detallado
comments = []
comments.append(f"**Título del PR:** {pr_title}")
comments.append(f"**Descripción del PR:**\n{pr_body if pr_body else 'Sin descripción.'}\n")
comments.append("### Cambios identificados en los archivos:\n")

# Analizar cada archivo
for file in files:
    filename = file.filename
    patch = file.patch  # El diff del archivo

    if not patch:
        comments.append(f"- `{filename}`: Sin cambios relevantes en el contenido (e.g., renombrado o cambio de permisos).")
        continue

    comments.append(f"- **Archivo:** `{filename}`\n")

    # Analizar las líneas modificadas
    added_lines = []
    removed_lines = []
    for line in patch.split("\n"):
        if line.startswith("+") and not line.startswith("+++"):  # Líneas añadidas
            added_lines.append(line[1:])
        elif line.startswith("-") and not line.startswith("---"):  # Líneas eliminadas
            removed_lines.append(line[1:])

    # Resumir cambios
    if added_lines:
        comments.append(f"  - **Líneas añadidas:**\n\n    " + "\n    ".join(added_lines[:]) + "\n")
    if removed_lines:
        comments.append(f"  - **Líneas eliminadas:**\n\n    " + "\n    ".join(removed_lines[:]) + "\n")

# Publicar el comentario en el PR
final_comment = "\n".join(comments)
pr.create_issue_comment(final_comment)
print("Comentario publicado exitosamente.")

