from pelican import signals

from .copy_code import copy_static_files, process_code_blocks


def register():
    signals.content_object_init.connect(process_code_blocks)
    signals.finalized.connect(copy_static_files)
