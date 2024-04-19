from src.database.local import PrefixesConnector


def determine_prefix(bot, message) -> str:
    custom_prefix = PrefixesConnector().get_prefix(message.author.id)
    if custom_prefix:
        return custom_prefix
    return "!"
