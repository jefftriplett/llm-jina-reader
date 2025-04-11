@_default:
    just --list

@build:
    uv build

@demo:
    just demo-fragment
    just demo-template

@demo-fragment:
    llm --fragment jina:https://simonwillison.net/2025/Apr/7/long-context-llm/ "Please summarize this post in one sentence."

@demo-template:
    llm --template jina:https://simonwillison.net/2025/Apr/7/long-context-llm/ "Please summarize this post in one sentence."

@install:
    llm install -e /Users/jefftriplett/.virtualenvs/llm-filesystem/src/llm-jina-reader-git

@plugins:
    llm plugins

@publish:
    uv publish

@reinstall:
    just uninstall
    just install

@uninstall:
    llm uninstall --yes llm-jina-reader
