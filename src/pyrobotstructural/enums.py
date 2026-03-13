from .bootstrap import get_robotom


class _RobotEnumDescriptor:
    """Lazily fetches the real COM enum value from the owning class's _robot_enum_name."""

    def __init__(self, value_name: str):
        self.value_name = value_name

    def __set_name__(self, owner, name):
        self.owner = owner

    def __get__(self, obj, objtype=None):
        cls = objtype if objtype is not None else type(obj)
        rbt = get_robotom()
        return getattr(getattr(rbt, cls._robot_enum_name), self.value_name)


def com_member(value_name: str) -> _RobotEnumDescriptor:
    """Declare a COM enum com_member on a RobotEnum class."""
    return _RobotEnumDescriptor(value_name)


class LabelType:
    _robot_enum_name = "IRobotLabelType"
    NODE_RELEASE = com_member("I_LT_NODE_RELEASE")
    NODE_COMPATIBLE = com_member("I_LT_NODE_COMPATIBILITY")
    BAR_SECTION = com_member("I_LT_BAR_SECTION")
    BAR_RELEASE = com_member("I_LT_BAR_RELEASE")
    BAR_OFFSET = com_member("I_LT_BAR_OFFSET")
    BAR_CABLE = com_member("I_LT_BAR_CABLE")
    BRACKET_AT_BAR_END = com_member("I_LT_BAREND_BRACKET")
    PANEL_THICKNESS = com_member("I_LT_PANEL_THICKNESS")
    PANEL_REINFORCEMENT = com_member("I_LT_PANEL_REINFORCEMENT")
    SUPPORT = com_member("I_LT_SUPPORT")
    MATERIAL = com_member("I_LT_MATERIAL")
    LINEAR_RELEASE = com_member("I_LT_LINEAR_RELEASE")
    ELASTIC_GROUND = com_member("I_LT_BAR_ELASTIC_GROUND")
    NODE_RIGID_LINK = com_member("I_LT_NODE_RIGID_LINK")
    com_member_TYPE = com_member("I_LT_MEMBER_TYPE")
    VEHICLE = com_member("I_LT_VEHICLE")
    SOLID_PROPERTIES = com_member("I_LT_SOLID_PROPERTIES")
    BAR_GEO_IMPERFECTIONS = com_member("I_LT_BAR_GEO_IMPERFECTIONS")
    BAR_NONLINEAR_HINGE = com_member("I_LT_BAR_NONLINEAR_HINGE")
    CLADDING = com_member("I_LT_CLADDING")
    PANEL_CALCULATION_MODEL = com_member("I_LT_PANEL_CALC_MODEL")
    REINFORCEMENT_PARAMS = com_member("I_LT_MEMBER_REINFORCEMENT_PARAMS")


class CaseNature:
    _robot_enum_name = "IRobotCaseNature"
    PERMANENT = com_member("I_CN_PERMANENT")
    EXPLOITATION = com_member("I_CN_EXPLOATATION")
    WIND = com_member("I_CN_WIND")
    SNOW = com_member("I_CN_SNOW")
    TEMPERATURE = com_member("I_CN_TEMPERATURE")
    ACCIDENTAL = com_member("I_CN_ACCIDENTAL")
    SEISMIC = com_member("I_CN_SEISMIC")


class LoadRecordType:
    _robot_enum_name = "IRobotLoadRecordType"
    NODE_FORCE = com_member("I_LRT_NODE_FORCE")
    NODE_DISPLACEMENT = com_member("I_LRT_NODE_DISPLACEMENT")
    BAR_DILATATION = com_member("I_LRT_BAR_DILATATION")
    BAR_FORCE_CONENTRATED = com_member("I_LRT_BAR_FORCE_CONCENTRATED")


class CaseAnalizeType:
    _robot_enum_name = "IRobotCaseAnalizeType"
    COMB_LINEAR = com_member("I_CAT_COMB")
    COMB_BUCKLING = com_member("I_CAT_COMB_BUCKLING")
    COMB_NONLIN_BUCKLING = com_member("I_CAT_COMB_NONLINEAR_BUCKLING")
    COMB_NONLINEAR = com_member("I_CAT_COMB_NONLINEAR")
    STATIC_LINEAR = com_member("I_CAT_STATIC_LINEAR")
    STATIC_NONLINEAR = com_member("I_CAT_STATIC_NONLINEAR")
    STATIC_LINEAR_AUX = com_member("I_CAT_STATIC_LINEAR_AUXILIARY")
    DYNAMIC_MODAL = com_member("I_CAT_DYNAMIC_MODAL")
    DYNAMIC_SPECTRAL = com_member("I_CAT_DYNAMIC_SPECTRAL")
    DYNAMIC_SEISMIC = com_member("I_CAT_DYNAMIC_SEISMIC")
    DYNAMIC_HARMONIC = com_member("I_CAT_DYNAMIC_HARMONIC")
    MOBILE = com_member("I_CAT_MOBILE_MAIN")
    STATIC_BUCKLING = com_member("I_CAT_STATIC_BUCKLING")
    STATIC_NONLINEAR_BUCKLING = com_member("I_CAT_STATIC_NONLINEAR_BUCKLING")


class CombinationType:
    _robot_enum_name = "IRobotCombinationType"
    ULS = com_member("I_CBT_ULS")
    SLS = com_member("I_CBT_SLS")
    ALS = com_member("I_CBT_ALS")
    SLS_FREQ = com_member("I_CBT_SLS_EC_FRE")
    SLS_QPR = com_member("I_CBT_SLS_EC_QPR")
    SLS_RARE = com_member("I_CBT_SLS_EC_RAR")
    SPECIAL = com_member("I_CBT_SPC")


class SectionShapeType:
    """To add more enums see page 556 or section II.3.1.3.1 RobotAPI"""

    _robot_enum_name = "IRobotBarSectionShapeType"
    TUBE = com_member("I_BSST_USER_TUBE")
    RECT = com_member("I_BSST_USER_RECT")
    RECT_FILLED = com_member("I_BSST_RECT_FILLED")
    I_BEAM = com_member("I_BSST_USER_I_BISYM")
    I_BEAM_MONOSYM = com_member("I_BSST_USER_I_MONOSYM")
    T_SHAPE = com_member("I_BSST_USER_T_SHAPE")
    C_SHAPE = com_member("I_BSST_USER_C_SHAPE")
    CROSS = com_member("_BSST_USER_CROSS")
    WOOD_RECTANGLE = com_member("I_BSST_WOOD_RECT")
    WOOD_DOUBLE_RECTANGLE = com_member("I_BSST_WOOD_DRECT")
    STEEL_RECT_FILLED = com_member("I_BSST_RECT_FILLED")
    STEEL_CIRCLE_FILLED = com_member("I_BSST_CIRC_FILLED")


class SectionType:
    _robot_enum_name = "IRobotBarSectionType"
    STANDARD = com_member("I_BST_STANDARD")
    COMPLEX = com_member("I_BST_COMPLEX")
    JOIST = com_member("I_BST_JOIST")
    BOX = com_member("I_BST_NS_BOX")
    TUBE = com_member("I_BST_NS_TUBE")
    RECT = com_member("I_BST_NS_RECT")


class ThicknessType:
    _robot_enum_name = "IRobotThicknessType"
    HOMOGENEOUS = com_member("I_TT_HOMOGENEOUS")
    ORTHOTROPIC = com_member("I_TT_ORTHOTROPIC")
