import click as click
import shutil
import os
from mapping_all_sheets import Mapping


steps_root = "../../../migration_steps/"
folder_name = "mapping_definitions"
steps_to_copy_to = ["transform_casrec", "acquire_target_ids"]


@click.command()
@click.option(
    "--mapping_doc",
    prompt="path to the mapping spreadsheet",
    default="./docs/Casrec_Mapping_Document_v0.1.xlsx",
)
@click.option(
    "--output_dir",
    prompt="path to the output directory",
    default="./docs/mapping_definitions",
)
@click.option(
    "--move_to_migration_steps",
    prompt=f"automatically copy to {', '.join(steps_to_copy_to)}?",
    default=True,
)
def main(mapping_doc, output_dir, move_to_migration_steps):

    mapping = Mapping(excel_doc=mapping_doc, output_folder=output_dir)
    mapping.generate_json_files()

    if move_to_migration_steps:
        for step in steps_to_copy_to:
            shutil.copytree(
                output_dir,
                os.path.join(steps_root, step, "app", folder_name),
                dirs_exist_ok=True,
            )


if __name__ == "__main__":

    main()
