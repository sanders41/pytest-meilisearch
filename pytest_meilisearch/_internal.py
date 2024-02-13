from functools import lru_cache


def determine_client_scope(*, fixture_name, config):
    return config.getini("meilisearch_client_scope")


@lru_cache
def determine_clear(config):
    clear = config.getini("meilisearch_clear").lower()
    valid = ("none", "async_document", "async_index", "document", "index")
    if clear not in valid:
        raise ValueError(
            f"'{clear}' is not a valid meilisearch_clear value. Valid values: none, async_document, async_index, document, or index"
        )
    return clear
