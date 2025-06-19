from logcaster.discord_utils.discord_embed import DiscordEmbed


def test_add_embed_field():
    embed = DiscordEmbed()
    name = 'foo'
    value = 'bar'
    inline = True

    embed.add_embed_field(name, value, inline)

    assert embed.embed.fields[0].name == name
    assert embed.embed.fields[0].value == value
    assert embed.embed.fields[0].inline == inline


def test_set_author():
    embed = DiscordEmbed()
    author_name = 'foo'

    embed.set_author(name=author_name)

    assert embed.embed.author.name == author_name


def test_set_footer():
    embed = DiscordEmbed()
    footer_text='foo'

    embed.set_footer(text=footer_text)

    assert embed.embed.footer.text == footer_text


def test_embed_init():
    emb = DiscordEmbed()
    
    assert emb.embed.title == ''
    assert emb.embed.description == ''
