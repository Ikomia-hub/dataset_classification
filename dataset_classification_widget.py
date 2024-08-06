# Copyright (C) 2021 Ikomia SAS
# Contact: https://www.ikomia.com
#
# This file is part of the IkomiaStudio software.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ikomia import core, dataprocess
from ikomia.utils import pyqtutils, qtconversion
from dataset_classification.dataset_classification_process import DatasetClassificationParam

# PyQt GUI framework
from PyQt5.QtWidgets import *


# --------------------
# - Class which implements widget associated with the process
# - Inherits PyCore.CWorkflowTaskWidget from Ikomia API
# --------------------
class DatasetClassificationWidget(core.CWorkflowTaskWidget):

    def __init__(self, param, parent):
        core.CWorkflowTaskWidget.__init__(self, parent)

        if param is None:
            self.parameters = DatasetClassificationParam()
        else:
            self.parameters = param

        # Create layout : QGridLayout by default
        self.grid_layout = QGridLayout()

        self.browse_dataset_folder = pyqtutils.append_browse_file(
            self.grid_layout,
            label="Dataset folder",
            file_filter="",
            path=self.parameters.dataset_folder,
            mode=QFileDialog.Directory
        )

        # Split dataset
        split_data = bool(self.parameters.split_dataset)
        self.check_split_data = QCheckBox("Split dataset")
        self.check_split_data.setChecked(split_data)
        self.grid_layout.addWidget(
            self.check_split_data, self.grid_layout.rowCount(), 0, 1, 2)

        self.check_split_data.stateChanged.connect(self.on_split_dataset_changed)

        # Split ratio
        self.spin_dataset_split_ratio = pyqtutils.append_double_spin(
                                                    self.grid_layout, "Split train/val",
                                                    self.parameters.dataset_split_ratio,
                                                    min=0.01,
                                                    max=1.0,
                                                    step=0.05,
                                                    decimals=2
        )

        self.spin_dataset_split_ratio.setVisible(split_data)

        # Seed
        self.spin_seed = pyqtutils.append_spin(
                                        self.grid_layout,
                                        "Seed",
                                        self.parameters.seed,
                                        step=1)
 
        self.spin_seed.setVisible(split_data)

        # Output folder
        self.browse_out_folder = pyqtutils.append_browse_file(
            self.grid_layout,
            label="Output folder (optional)",
            path=self.parameters.output_folder,
            tooltip="Select folder",
            mode=QFileDialog.Directory
        )

        self.browse_out_folder.setVisible(split_data)

        # PyQt -> Qt wrapping
        layout_ptr = qtconversion.PyQtToQt(self.grid_layout)

        # Set widget layout
        self.set_layout(layout_ptr)


    def on_split_dataset_changed(self, int):
        self.spin_dataset_split_ratio.setVisible(self.check_split_data.isChecked())
        self.browse_out_folder.setVisible(self.check_split_data.isChecked())
        self.spin_seed.setVisible(self.check_split_data.isChecked())

    def on_apply(self):
        # Apply button clicked slot
        self.parameters.dataset_folder = self.browse_dataset_folder.path
        self.parameters.split_dataset = self.check_split_data.isChecked()
        self.parameters.dataset_split_ratio = self.spin_dataset_split_ratio.value()
        self.parameters.output_folder = self.browse_out_folder.path
        self.parameters.seed = self.spin_seed.value()
        self.parameters.update = True

        # Send signal to launch the process
        self.emit_apply(self.parameters)


# --------------------
# - Factory class to build process widget object
# - Inherits PyDataProcess.CWidgetFactory from Ikomia API
# --------------------
class DatasetClassificationWidgetFactory(dataprocess.CWidgetFactory):

    def __init__(self):
        dataprocess.CWidgetFactory.__init__(self)
        # Set the name of the process -> it must be the same as the one declared in the process factory class
        self.name = "dataset_classification"

    def create(self, param):
        # Create widget object
        return DatasetClassificationWidget(param, None)
