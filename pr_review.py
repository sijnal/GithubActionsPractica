import openai
import os
import sys
from github import Github

# Configuración de OpenAI
#openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuración de GitHub
GITHUB_TOKEN = os.getenv("MY_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = int(os.getenv("PR_NUMBER"))

# Instanciar cliente de GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)
pr = repo.get_pull(PR_NUMBER)

# Obtener los cambios del PR
files = pr.get_files()
changed_files = [file.filename for file in files]

# Generar comentario con OpenAI
def get_openai_comment(changed_files):
    diff_text = "\n".join(changed_files)
    prompt = f"Here are some code changes:\n{diff_text}\nPlease review and provide feedback on potential issues or areas of improvement."

    #response = openai.Completion.create(
    #    engine="text-davinci-003",
    #    prompt=prompt,
    #    max_tokens=300
    #)

    return prompt
    #return response.choices[0].text.strip()

# Comentar en el PR
def post_comment(comment):
    pr.create_issue_comment(comment)

if __name__ == "__main__":
    comment = get_openai_comment(changed_files)
    post_comment(comment)
