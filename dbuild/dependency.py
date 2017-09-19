import logging
import os

import dockerfile_parse as d_parser

logger = logging.getLogger(__name__)

_BASE_PATH = os.path.realpath(os.getcwd())


def get_dependencies(image, all_images):
    deps = []
    dockerfile = get_dockerfile(image)

    if not dockerfile:
        logging.warning('%s is not image home or '
                        'something went terribly wrong' % image)
        raise deps

    parent_image = dockerfile.baseimage
    # note(kornicameister) check if the parent image is part of the all modules
    # if so, traverse even deeper to reach
    if parent_image in all_images:
        deps.extend(get_dependencies(parent_image, all_images))

    # note(kornicameister) reverse the dependencies, we want to
    # have the grand elder to always be the first module that we build

    return deps[::-1]


def get_dockerfile(image):
    path_to_file = os.path.join(_BASE_PATH, image, 'Dockerfile')
    if os.path.exists(path_to_file):
        return d_parser.DockerfileParser(
            path=path_to_file,
            cache_content=True
        )
    return None
