from common.UIImage import ImageDisplayer
from utils.files_mgmt import res_dir

import os

IVI_AVM_CAMERA_PM_HW_BLOCK_DIAGRAM = "Hardware Block Diagram"
IVI_AVM_CAMERA_INTEGRATED_PM_SEQUENCE = "Integrated Solution Sequence Diagram"

DIAGRAMS_DICT = {
    IVI_AVM_CAMERA_PM_HW_BLOCK_DIAGRAM: os.path.join(res_dir, "images/ic_avm_camera_pm_hw.drawio.png"),
    IVI_AVM_CAMERA_INTEGRATED_PM_SEQUENCE: os.path.join(res_dir, "images/IVIIntegratedAVM360CamerasPMSequence.png")
    
}


ivi_avm_pm_diagrams = ImageDisplayer(
    img_dict=DIAGRAMS_DICT,
    label="IVI AVM Cameras Power Management Diagrams"
)

