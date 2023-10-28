from functools import lru_cache


def determine_client_scope(*, fixture_name, config):
    return config.getini("meilisearch_client_scope")


@lru_cache
def determine_clear_indexes(config):
    clear = config.getini("meilisearch_clear_indexes").lower()
    valid = ("none", "async", "sync")
    if clear not in valid:
        raise ValueError(
            f"'{clear}' is not a valid meilisearch_clear_indexes value. Valid values: none, async, or sync"
        )
    return clear
