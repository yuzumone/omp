import click

from omp.mstdn import mstdn  # type: ignore


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def main() -> None:
    pass


main.add_command(mstdn)


if __name__ == "__main__":
    main()
