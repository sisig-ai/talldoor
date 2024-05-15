import os

from weaviate import Client

PAGE = {
    "class": "Page",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {"text2vec-openai": {}, "generative-openai": {}},
}


def init_datastore(client: Client):
    if client.schema.exists(PAGE["class"]):
        return
    client.schema.create_class(PAGE)


def load_tldr_pages(client: Client, should_reload: bool = False):
    if not should_reload:
        print("Skipping datastore load.")
        return
    tldr_directory = "tldr-pages"
    markdown_files = []
    for root, dirs, files in os.walk(tldr_directory):
        for file in files:
            if file in ["README.md", "LICENSE.md"]:
                continue
            if file.endswith(".md"):
                relative_path = os.path.join(root, file)
                with client.batch as batch, open(relative_path, "r") as f:
                    properties = {
                        "content": f.read(),
                        "command": file.replace(".md", ""),
                        "category": relative_path.split("/")[1],
                    }
                    print(f"Adding {relative_path} to datastore.")
                    batch.add_data_object(
                        data_object=properties, class_name=PAGE["class"]
                    )
    print(markdown_files)
    print(f"Found {len(markdown_files)} markdown files in {tldr_directory}.")
