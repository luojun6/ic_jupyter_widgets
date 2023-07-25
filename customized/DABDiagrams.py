from common.UIImage import ImageDisplayer
from utils.files_mgmt import res_dir

import os

DAB_THEORY = "DAB Basic Theory"
DAB_HARDWARE_BLOCK_Diagram = "DAB Hardware Block Diagram"

DIAGRAMS_DICT = {
    DAB_THEORY: os.path.join(res_dir, "images/DAB_example.jpg"),
    DAB_HARDWARE_BLOCK_Diagram: os.path.join(res_dir, "images/DAB_HW.drawio.png"),
}


dab_pm_diagrams = ImageDisplayer(
    img_dict=DIAGRAMS_DICT, label="DAB Power Management Diagrams"
)
