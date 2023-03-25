# Subcommands -- Tasks that are chained onto main commands.

from core.gui.main.components import convert_widget


# Expects integer in range (0,2)
def auto_download_hr(output_mode_index):
    # get the output mode value corresponding to provided index
    output_value = ['Video', 'Audio', 'Mute Video'][output_mode_index]
    # update the string var
    convert_widget.output_mode.set(output_value)
    # update output settings
    convert_widget.update_output_mode(output_value)
    # automatically download the file
    convert_widget.execute_download()

