from form.build.map import ObjectMapper, TypeMap
from form.build.builders import DatasetBuilder, GroupBuilder
from form.build.map import BuildManager
import numpy as np
import os
from form.utils import docval, getargs, popargs, get_docval
from six import raise_from

class ObjectMapperLegacy(ObjectMapper):


    @ObjectMapper.constructor_arg('source')
    def source_gettr(self, builder, manager):

        if 'source' in builder.attributes:
            return builder.attributes['source']
        else:
            return 'No known source'


    @docval({'name': 'builder', 'type': (DatasetBuilder, GroupBuilder), 'doc': 'the builder to construct the Container from'},
            {'name': 'manager', 'type': BuildManager, 'doc': 'the BuildManager for this build'})
    def construct(self, **kwargs):
        ''' Construct an Container from the given Builder '''

        builder, manager = getargs('builder', 'manager', kwargs)
        cls = manager.get_cls(builder)

        subspecs = self.hack_get_subspec_values(builder, self.spec, manager)
        const_args = dict()
        for subspec, value in subspecs.items():
            const_arg = self.get_const_arg(subspec)
            if const_arg is not None:
                const_args[const_arg] = value

        args = list()
        kwargs = dict()
        for const_arg in get_docval(cls.__init__):
            argname = const_arg['name']
            override = self.__get_override_carg(argname, builder, manager)
            if override:
                val = override
            elif argname in const_args:
                val = const_args[argname]
            else:
                continue
            if 'default' in const_arg:
                kwargs[argname] = val
            else:
                args.append(val)

        try:
            obj = cls(*args, **kwargs)
        except Exception as ex:
            msg = 'Could not construct %s object' % cls.__name__
            raise_from(Exception(msg), ex)

        return obj

    def __get_override_carg(self, *args, **kwargs):
        return self.hack_get_override_carg(*args, **kwargs)

class TypeMapLegacy(TypeMap):

    def get_builder_dt(self, builder):    

        if builder.name == 'roi_ids':
            pass
        elif builder.name == 'root':
            return 'NWBFile'
        attrs = builder.attributes
        ndt = attrs.get('neurodata_type')
        if ndt == 'Module':
            return 'ProcessingModule'
        elif ndt == 'TimeSeries':
            ancestry = attrs['ancestry']
            if ancestry[-1] == 'TwoPhotonSeries' and builder.name == 'corrected':
                return 'ImageSeries'
            else:
                return ancestry[-1]

        elif ndt == 'Interface':
            return builder.name
        if ndt == 'Epoch':
            return 'Epoch'
        else:
            parent_ndt = self.get_builder_dt(builder.parent)
            if parent_ndt == 'Epoch':
                return 'EpochTimeSeries'
            if parent_ndt == 'MotionCorrection':
                return 'CorrectedImageStack'
            if parent_ndt == 'ImagingPlane' and isinstance(builder, GroupBuilder):
                return 'OpticalChannel'
            if parent_ndt == 'ImageSegmentation':
                if builder.name in ('roi_ids', 'cell_specimen_ids'):
                    return None
                else:
                    return 'PlaneSegmentation'

            else:
                if parent_ndt == 'PlaneSegmentation':
                    if builder.name in ('roi_list', 'imaging_plane_name'):
                        return None
                    else:
                        return 'ROI'

                parent_names = {'extracellular_ephys': 'ElectrodeGroup','intracellular_ephys': 'IntracellularElectrodeGroup',
                   'optophysiology': 'ImagingPlane',
                   'optogenetics': 'OptogeneticStimulusSite'
                   }
                return parent_names.get(builder.parent.name)
            return None

    def get_builder_ns(self, builder):
        return 'core'