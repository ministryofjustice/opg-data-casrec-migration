import click as click

from mapping_all_sheets import Mapping


@click.command()
@click.option(
    "--mapping_doc",
    prompt="path to the mapping spreadsheet",
    default="./docs/mapping_doc_mini.xlsx",
)
@click.option(
    "--output_dir", prompt="path to the output directory", default="./json_files"
)
def main(mapping_doc, output_dir):

    mapping = Mapping(excel_doc=mapping_doc, output_folder=output_dir)
    mapping.generate_json_files()


if __name__ == "__main__":

    main()

    print("All finished :)")
