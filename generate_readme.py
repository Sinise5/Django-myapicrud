import requests
import os
import django
from django.apps import apps

# Load Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapicrud.settings")  # Sesuaikan dengan nama proyekmu
django.setup()  # Inisialisasi Django

API_DOC_URL = "http://127.0.0.1:8000/swagger.json"

def fetch_api_schema():
    """Fetch API schema from Swagger JSON"""
    try:
        response = requests.get(API_DOC_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching API schema: {e}")
        return None

def get_models():
    """Retrieve all Django models and format as Markdown list"""
    model_list = ""
    for model in apps.get_models():
        model_list += f"- `{model.__name__}` (Table: {model._meta.db_table})\n"
    return model_list

def parse_api_schema(schema):
    """Parse Swagger schema into a formatted Markdown string"""
    readme_content = "# API Documentation\n\n"

    for path, methods in schema.get("paths", {}).items():
        readme_content += f"## `{path}`\n"
        for method, details in methods.items():
            # Pastikan `details` adalah dictionary, bukan list
            if isinstance(details, list):
                for detail in details:  # Iterasi jika berupa list
                    readme_content += parse_api_detail(method, detail)
            else:
                readme_content += parse_api_detail(method, details)

    return readme_content

def parse_api_detail(method, detail):
    """Helper function to parse API details"""
    content = f"### **{method.upper()}**\n"
    content += f"**Description:** {detail.get('summary', 'No description')}\n\n"

    # Tambahkan Parameters jika ada
    if "parameters" in detail:
        content += "**Parameters:**\n"
        for param in detail["parameters"]:
            content += f"- `{param['name']}`: {param.get('description', 'No description')}\n"
        content += "\n"

    # Tambahkan Responses jika ada
    if "responses" in detail:
        content += "**Responses:**\n"
        for status, response in detail["responses"].items():
            content += f"- **{status}**: {response.get('description', 'No description')}\n"
        content += "\n"

    return content


def generate_readme():
    """Generate README.md with API schema and model list"""
    schema = fetch_api_schema()
    if not schema:
        print("Skipping README generation due to missing API schema.")
        return

    if not os.path.exists("README_template.md"):
        print("Error: README_template.md not found.")
        return

    with open("README_template.md", "r") as file:
        template = file.read()

    # Masukkan daftar model dan API schema ke template
    readme_content = template.replace("{{MODELS}}", get_models())
    readme_content += "\n" + parse_api_schema(schema)

    with open("README.md", "w") as file:
        file.write(readme_content)

    print("README.md generated successfully!")

if __name__ == "__main__":
    generate_readme()
