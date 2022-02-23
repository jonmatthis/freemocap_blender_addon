from . import abs_rigging
from ...cgt_naming import HAND
from .utils.drivers.hand_drivers import FingerDriverContainer


class RigifyHands(abs_rigging.BpyRigging):
    def __init__(self, armature, driver_objects):
        # driver to rigify cgt_rig transfer name references
        self.pose_bones = armature.pose.bones

        self.references = {
            HAND.wrist:                     "hand_ik",
            HAND.driver_thumb_cmc:          "thumb.01",
            HAND.driver_thumb_mcp:          "thumb.02",
            HAND.driver_thumb_ip:           "thumb.03",
            HAND.driver_thumb_tip:          "thumb.01",
            HAND.driver_index_finger_mcp:   "f_index.01",
            HAND.driver_index_finger_pip:   "f_index.02",
            HAND.driver_index_finger_dip:   "f_index.03",
            HAND.driver_index_finger_tip:   "f_index.01",
            HAND.driver_middle_finger_mcp:  "f_middle.01",
            HAND.driver_middle_finger_pip:  "f_middle.02",
            HAND.driver_middle_finger_dip:  "f_middle.03",
            HAND.driver_middle_finger_tip:  "f_middle.01",
            HAND.driver_ring_finger_mcp:    "f_ring.01",
            HAND.driver_ring_finger_pip:    "f_ring.02",
            HAND.driver_ring_finger_dip:    "f_ring.03",
            HAND.driver_ring_finger_tip:    "f_ring.01",
            HAND.driver_pinky_mcp:          "f_pinky.01",
            HAND.driver_pinky_pip:          "f_pinky.02",
            HAND.driver_pinky_dip:          "f_pinky.03",
            HAND.driver_pinky_tip:          "f_pinky.01",
        }

        finger_driver_references = {
            # provider              # target
            HAND.thumb_cmc:         HAND.driver_thumb_cmc,
            HAND.thumb_mcp:         HAND.driver_thumb_mcp,
            HAND.thumb_ip:          HAND.driver_thumb_ip,
            HAND.thumb_tip:         HAND.driver_thumb_tip,
            HAND.index_finger_mcp:  HAND.driver_index_finger_mcp,
            HAND.index_finger_pip:  HAND.driver_index_finger_pip,
            HAND.index_finger_dip:  HAND.driver_index_finger_dip,
            HAND.index_finger_tip:  HAND.driver_index_finger_tip,
            HAND.middle_finger_mcp: HAND.driver_middle_finger_mcp,
            HAND.middle_finger_pip: HAND.driver_middle_finger_pip,
            HAND.middle_finger_dip: HAND.driver_middle_finger_dip,
            HAND.middle_finger_tip: HAND.driver_middle_finger_tip,
            HAND.ring_finger_mcp:   HAND.driver_ring_finger_mcp,
            HAND.ring_finger_pip:   HAND.driver_ring_finger_pip,
            HAND.ring_finger_dip:   HAND.driver_ring_finger_dip,
            HAND.ring_finger_tip:   HAND.driver_ring_finger_tip,
            HAND.pinky_mcp:         HAND.driver_pinky_mcp,
            HAND.pinky_pip:         HAND.driver_pinky_pip,
            HAND.pinky_dip:         HAND.driver_pinky_dip,
            HAND.pinky_tip:         HAND.driver_pinky_tip,
        }

        left_finger_provider = [key + ".L" for key in finger_driver_references.keys()]
        right_finger_provider = [key + ".R" for key in finger_driver_references.keys()]
        left_finger_targets = [value + ".L" for value in finger_driver_references.values()]
        right_finger_targets = [value + ".R" for value in finger_driver_references.values()]

        self.left_finger_angle_drivers = FingerDriverContainer(
            left_finger_targets,
            left_finger_provider)

        self.right_finger_angle_drivers = FingerDriverContainer(
            right_finger_targets,
            right_finger_provider)

        # storing relations between rigify and driver cgt_rig (left / right hand)
        self.constraint_dict = {}
        self.set_relation_dict(driver_objects)
        self.apply_drivers()

    def get_reference_bone(self, key, extension):
        """ get reference bone by driver empty name. """
        if "TIP" in key:
            # rigify finger tip has .001 extension (why ever..)
            bone_name = self.references[key] + extension + ".001"
            return bone_name

        bone_name = self.references[key] + extension
        return bone_name

    def set_relation_dict(self, driver_objects):
        """ sets relation dict containing bone name and reference empty obj. """
        for empty in driver_objects:
            # can be left / right hand
            if ".L" in empty.name:
                extension = ".L"
            else:
                extension = ".R"

            # remove extension from driver name
            name = empty.name.replace(extension, "")
            try:
                bone_name = self.get_reference_bone(name, extension)
                self.constraint_dict[empty.name] = [bone_name, "COPY_ROTATION"]

            except KeyError:
                print("driver empty does not exist:", empty.name)

        self.set_single_prop_relation(
            [self.left_finger_angle_drivers, self.right_finger_angle_drivers],
            [obj.name for obj in driver_objects], driver_objects)
        self.set_constraint_relation(self.constraint_dict, [obj.name for obj in driver_objects], driver_objects)
