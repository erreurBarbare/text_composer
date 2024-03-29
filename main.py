import pyperclip
from jinja2 import Environment, PackageLoader, select_autoescape

import composer_utils as cu
import input_utils
import jinja_utils

SERIES = "series"
BLOCKS = "blocks"


def main():
    configs = cu.get_config()

    env = Environment(loader=PackageLoader("main"),
                      autoescape=select_autoescape())
    jinja_utils.setup(env)

    # load series
    series_json = cu.load_json_from_file(configs['Files']['PathSeries'])

    # select relevant series
    series_id = input_utils.get_relevant_series_id(series_json)

    # generate template from blocks
    blocks_paths = cu.get_attribute_of_single_object(series_json, SERIES, series_id, "source_files")
    blocks_json = cu.load_json_from_file(blocks_paths[str(0)])
    for i in range(1, len(blocks_paths)):
        blocks_i = cu.load_json_from_file(blocks_paths[str(i)])
        for key, value in blocks_i.items():
            if key in blocks_json:
                blocks_json[key].extend(value)
            else:
                blocks_json[key] = value
    series_relevant_blocks = cu.get_attribute_of_single_object(series_json, SERIES, series_id, "blocks")
    cu.generate_template(series_relevant_blocks, blocks_json,
                         configs['Files']['TemplateFolder'] + configs['Files']['Template'])
    template = env.get_template(configs['Files']['Template'])

    # define the variables values for the final text
    int_vars = cu.flatten(cu.get_attribute_of_all_objects(blocks_json, BLOCKS, "integer_vars"))
    date_vars = cu.flatten(cu.get_attribute_of_all_objects(blocks_json, BLOCKS, "date_vars"))
    time_vars = cu.flatten(cu.get_attribute_of_all_objects(blocks_json, BLOCKS, "time_vars"))
    enum_vars = cu.flatten(cu.get_attribute_of_all_objects(blocks_json, BLOCKS, "enum_vars"))
    optional_vars = cu.flatten(cu.get_attribute_of_all_objects(blocks_json, BLOCKS, "optional_vars"))
    series_vars = cu.get_attribute_of_single_object(series_json, SERIES, series_id, "variables")
    text_variables_values = input_utils.get_template_vars(env, series_vars, int_vars, date_vars, time_vars,
                                                          enum_vars, optional_vars)

    # generate final text
    content = template.render(text_variables_values)

    with open(configs['Files']['FolderOutput'] + configs['Files']['FilenameOutput'], mode='w',
              encoding='utf-8') as message:
        message.write(content)

    pyperclip.copy(content)


if __name__ == '__main__':
    main()
