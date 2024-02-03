import datetime
from pathlib import Path

import click
from bs4 import BeautifulSoup
from mastodon import Mastodon


@click.command("mastodon")
@click.option("--base-url", envvar="MASTODON_BASE_URL")
@click.option("--client-id", envvar="MASTODON_CLIENT_ID")
@click.option("--client-secret", envvar="MASTODON_CLIENT_SECRET")
@click.option("--access-token", envvar="MASTODON_ACCESS_TOKEN")
@click.option("--date", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--file", type=click.Path(exists=True, resolve_path=True, path_type=Path))
def mstdn(base_url: str, client_id: str, client_secret: str, access_token: str, date: datetime.datetime, file: Path) -> None:
    mastodon = Mastodon(
        api_base_url=base_url,
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
    )
    me = mastodon.me()
    statuses = mastodon.account_statuses(me.id, limit=50)
    end_date = date + datetime.timedelta(days=1)
    targets = [x for x in statuses if date.astimezone() < x.created_at.astimezone() and x.created_at.astimezone() < end_date.astimezone()]
    body = [f"* {date.strftime('%A, %d %B %Y')}"]
    for x in targets:
        tmp = [
            f"** {x.created_at.astimezone().strftime('%H:%M')}",
            f""":PROPERTIES:
:URL: {x.url}
:END:""",
            BeautifulSoup(x.content, "html.parser").get_text(),
        ]
        body.extend(tmp)
    content = file.read_text() + "\n".join(body) + "\n"
    file.write_text(content)
