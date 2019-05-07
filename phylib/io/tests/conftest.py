# -*- coding: utf-8 -*-

"""Test fixtures."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import logging
import os
import os.path as op
import shutil

from pytest import fixture


from phylib.utils._misc import _read_python
from ..model import TemplateModel
from phylib.io.datasets import download_test_file

logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------
# Fixtures
#------------------------------------------------------------------------------

_FILES = ['template/params.py',
          'template/sim_binary.dat',
          'template/spike_times.npy',
          'template/spike_templates.npy',
          'template/spike_clusters.npy',
          'template/amplitudes.npy',

          'template/cluster_group.tsv',

          'template/channel_map.npy',
          'template/channel_positions.npy',

          'template/templates.npy',
          # 'template/template_ind.npy',
          'template/similar_templates.npy',
          'template/whitening_mat.npy',

          'template/pc_features.npy',
          'template/pc_feature_ind.npy',

          'template/template_features.npy',
          'template/template_feature_ind.npy',

          ]


@fixture
def template_path(tempdir):
    # Download the dataset.
    paths = list(map(download_test_file, _FILES))
    # Copy the dataset to a temporary directory.
    for path in paths:
        to_path = op.join(tempdir, op.basename(path))
        logger.debug("Copying file to %s.", to_path)
        shutil.copy(path, to_path)
    template_path = op.join(tempdir, op.basename(paths[0]))
    return template_path


@fixture
def template_model(template_path):
    params = _read_python(template_path)
    params['dat_path'] = op.join(op.dirname(template_path), params['dat_path'])
    params['dir_path'] = op.dirname(template_path)
    model = TemplateModel(**params)
    return model


@fixture
def template_model_clean(template_path):
    os.remove(op.join(op.dirname(template_path), 'spike_clusters.npy'))
    os.remove(op.join(op.dirname(template_path), 'cluster_group.tsv'))
    return template_model(template_path)
