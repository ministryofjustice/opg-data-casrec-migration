import click as click

from mapping_all_sheets import Mapping


@click.command()
@click.option(
    "--mapping_doc",
    prompt="path to the mapping spreadsheet",
    default="./docs/Casrec_Mapping_Document_v0.1.xlsx",
)
@click.option(
    "--output_dir",
    prompt="path to the output directory",
    default="../../../migration_steps/transform_casrec/app/mapping_definitions",
)
def main(mapping_doc, output_dir):

    mapping = Mapping(excel_doc=mapping_doc, output_folder=output_dir)
    mapping.generate_json_files()


if __name__ == "__main__":

    main()

    print("All finished :)")
