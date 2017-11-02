from .. import ObjectMapper
from pynwb.legacy import register_map
from pynwb.icephys import PatchClampSeries

@register_map(PatchClampSeries)
class PatchClampSeriesMap(ObjectMapper):

    @ObjectMapper.constructor_arg('electrode')
    def carg_imaging_plane(self, *args):
        builder = args[0]
        manager = args[1]
        root = builder
        parent = root.parent
        while parent is not None:
            root = parent
            parent = root.parent
        elec_name = builder['electrode_name']['data']
        elec_builder = root['general/intracellular_ephys/%s' % elec_name]
        electrode = manager.construct(elec_builder)
        return electrode
