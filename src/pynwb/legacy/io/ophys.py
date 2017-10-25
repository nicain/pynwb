from .. import ObjectMapper
from pynwb.legacy import register_map
from pynwb.ophys import PlaneSegmentation, ImageSegmentation, ROI, TwoPhotonSeries
import numpy as np

@register_map(PlaneSegmentation)
class PlaneSegmentationMap(ObjectMapper):

    # This might be needed for 2.0 as well
    def __init__(self, spec):
        super(PlaneSegmentationMap, self).__init__(spec)
        roi_spec = self.spec.get_neurodata_type('ROI')
        self.map_spec('roi_list', roi_spec)

        reference_images_spec = self.spec.get_group('reference_images').get_neurodata_type('ImageSeries')
        self.map_spec('reference_images', reference_images_spec)

#    I think we can delete this
#    @ObjectMapper.constructor_arg('roi_list')
#    def carg_roi_list(self, builder):
#        return builder.get('rois')

    @ObjectMapper.constructor_arg('imaging_plane')
    def carg_imaging_plane(self, *args):
        builder = args[0]
        if len(args) < 2:
            return builder.name # I think this is the hack you had in there before
        manager = args[1]
        root = builder
        parent = root.parent
        while parent is not None:
            root = parent
            parent = root.parent
        ip_name = builder['imaging_plane_name']['data']
        ip_builder = root['general/optophysiology/%s' % ip_name]
        imaging_plane = manager.construct(ip_builder)
        return imaging_plane

    # @ObjectMapper.constructor_arg('reference_images')
    # def carg_reference_images(self, builder):
    #     return builder.get('image_series') # builder.get('reference_images')

    # @ObjectMapper.constructor_arg('reference_images')
    # def carg_reference_images(self, builder):
    #     return builder.get('image_series') # builder.get('reference_images')

@register_map(TwoPhotonSeries)
class TwoPhotonSeriesMap(ObjectMapper):

    @ObjectMapper.constructor_arg('data')
    def carg_data(self, *args):
        builder = args[0]
        if builder.name in ('2p_image_series',):
            return np.array([-1.])

    @ObjectMapper.constructor_arg('unit')
    def carg_unit(self, *args):
        builder = args[0]
        if builder.name in ('2p_image_series',):
            return 'None'


@register_map(ROI)
class ROIMap(ObjectMapper):

    @ObjectMapper.constructor_arg('reference_images')
    def carg_reference_images(self, *args):
        return 'None'

    @ObjectMapper.constructor_arg('name')
    def carg_name(self, *args):
        builder = args[0]
        return builder.name

    # @ObjectMapper.constructor_arg('source')
    # def source_gettr(self, builder):

    #     if 'source' in builder.attributes:
    #         return builder.attributes['source']
    #     else:
    #         return 'None2'


    # def __get_override_carg(self, *args, **kwargs):
    #     return self.hack_get_override_carg(*args, **kwargs)

    # @ObjectMapper.constructor_arg('imaging_plane')
    # def carg_imaging_plane(self, builder):
    #     return 'imaging_plane_1' #builder.get('imaging_plane')

    # @ObjectMapper.constructor_arg('reference_images')
    # def carg_reference_images(self, builder):
    #     return builder.get('image_series') # builder.get('reference_images')