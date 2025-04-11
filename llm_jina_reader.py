import httpx
import os
import yaml

from llm import Fragment
from llm import hookimpl
from llm import Template
from typing import List


@hookimpl
def register_fragment_loaders(register):
    register("jina", jina_reader_loader)


@hookimpl
def register_template_loaders(register):
    register("jina", file_template_loader)


def _get_jina_response(url_path: str) -> httpx.Response:
    token = os.environ.get("JINA_READER_TOKEN")
    if not token:
        raise ValueError("JINA_READER_TOKEN environment variable not set")

    if url_path.startswith(("http://", "https://")):
        jina_url = f"https://r.jina.ai/{url_path}"
    else:
        raise ValueError("INVALID url")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.get(jina_url, headers=headers)
        response.raise_for_status()
        return response
    except Exception as ex:
        raise ValueError(f"Could not load content {url_path} via Jina: {str(ex)}")


def jina_reader_loader(argument: str) -> List[Fragment]:
    response = _get_jina_response(argument)
    
    fragments = []
    fragments.append(
        Fragment(
            response.text,
            source=f"https://r.jina.ai/{argument}",
        )
    )
    return fragments


def file_template_loader(template_path: str) -> Template:
    response = _get_jina_response(template_path)

    system_content = response.text

    print(system_content)

    template_args = {
        "name": template_path,
        "system": system_content,
        # "user": "",
    }

    # try:
    # except yaml.YAMLError as ex:
    #     raise ValueError(f"Invalid YAML in template file: {ex}")

    return Template(**template_args)
