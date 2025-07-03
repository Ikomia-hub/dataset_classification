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

import copy
import os
import random
import shutil
from datetime import datetime

from ikomia import core, dataprocess, utils
from ikomia.dnn import dataset, datasetio


# --------------------
# - Class to handle the process parameters
# - Inherits PyCore.CWorkflowTaskParam from Ikomia API
# --------------------
class DatasetClassificationParam(core.CWorkflowTaskParam):

    def __init__(self):
        core.CWorkflowTaskParam.__init__(self)
        # Place default value initialization here
        self.dataset_folder = ""
        self.dataset_split_ratio = 0.8
        self.split_dataset = False
        self.output_folder = ""
        self.seed = 42
        self.update = False

    def set_values(self, param_map):
        # Set parameters values from Ikomia application
        # Parameters values are stored as string and accessible like a python dict
        self.dataset_folder = param_map["dataset_folder"]
        self.dataset_split_ratio = float(param_map["dataset_split_ratio"])
        self.split_dataset = utils.strtobool(param_map["split_dataset"])
        self.output_folder = param_map["output_folder"]
        self.seed = int(param_map["seed"])
        self.update = True

    def get_values(self):
        # Send parameters values to Ikomia application
        # Create the specific dict structure (string container)
        param_map = {
            "dataset_folder": str(self.dataset_folder),
            "dataset_split_ratio": str(self.dataset_split_ratio),
            "split_dataset": str(self.split_dataset),
            "output_folder": str(self.output_folder),
            "seed": str(self.seed)
        }
        return param_map


# --------------------
# - Class which implements the process
# - Inherits PyCore.CWorkflowTask or derived from Ikomia API
# --------------------
class DatasetClassification(core.CWorkflowTask):

    def __init__(self, name, param):
        core.CWorkflowTask.__init__(self, name)
        # Add input/output of the process here
        self.add_output(dataprocess.CPathIO(core.IODataType.FOLDER_PATH))

        # Create parameters class
        if param is None:
            self.set_param_object(DatasetClassificationParam())
        else:
            self.set_param_object(copy.deepcopy(param))

        self.img_extension = ['.jpeg', '.jpg', '.png', '.bmp', '.tiff', '.tif', '.dib', '.jpe', '.jp2', '.webp', '.pbm', '.pgm', '.ppm', '.pxm', '.pnm', '.sr', '.ras', '.exr', '.hdr', '.pic']

    def get_progress_steps(self):
        # Function returning the number of progress steps for this process
        # This is handled by the main progress bar of Ikomia application
        return 1

    def run(self):
        # Core function of your process
        # Call begin_task_run() for initialization
        self.begin_task_run()

       # Get output :
        task_output = self.get_output(0)

        # Get parameters :
        param = self.get_param_object()

        # Split dataset into train and val folders
        if param.split_dataset:
            print("Splitting dataset...")
            input_folder = param.dataset_folder
            if param.output_folder:
                dataset_folder = os.path.join(param.output_folder)
            else:
                date_time = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                dataset_folder = os.path.join(
                    os.path.dirname(input_folder),
                    f"dataset_classification_{date_time}"
                )
            train_folder = os.path.join(dataset_folder, "train")
            val_folder = os.path.join(dataset_folder, "val")

            # Create folders if they don't exist
            os.makedirs(train_folder, exist_ok=True)
            os.makedirs(val_folder, exist_ok=True)

            # Get a list of subfolders in the dataset folder
            subfolders = [f.name for f in os.scandir(input_folder) if f.is_dir()]

            # Split the dataset for each subfolder
            for subfolder in subfolders:
                class_folder = os.path.join(input_folder, subfolder)
                train_class_folder = os.path.join(train_folder, subfolder)
                val_class_folder = os.path.join(val_folder, subfolder)

                # Create train and val subfolders for the current class if they don't exist
                os.makedirs(train_class_folder, exist_ok=True)
                os.makedirs(val_class_folder, exist_ok=True)

                # Get a list of images in the current class folder
                images = [f.name for f in os.scandir(class_folder) if f.is_file() and os.path.splitext(f.name)[1].lower() in self.img_extension]

                if len(images) == 0: 
                    print(f'NO IMAGE FOUND in {class_folder}, this might result ' \
                          'in an error if the dataset is use to train a classification algorithm')

                # Shuffle the images based on seed
                random.seed(param.seed)
                random.shuffle(images)

                # Split the images based on the split ratio
                split_index = int(len(images) * param.dataset_split_ratio)
                train_images = images[:split_index]
                val_images = images[split_index:]

                # Move the training images to the train folder
                for image in train_images:
                    src_path = os.path.join(class_folder, image)
                    dst_path = os.path.join(train_class_folder, image)
                    shutil.copy(src_path, dst_path)

                # Move the validation images to the val folder
                for image in val_images:
                    src_path = os.path.join(class_folder, image)
                    dst_path = os.path.join(val_class_folder, image)
                    shutil.copy(src_path, dst_path)

            print(f'Classification dataset created in {dataset_folder}')
        # Use the dataset folder as output
        else:
            dataset_folder = param.dataset_folder

        param.update = False

        # Set output
        task_output.set_path(dataset_folder)

        # Step progress bar (Ikomia Studio)
        self.emit_step_progress()

        # Call end_task_run() to finalize process
        self.end_task_run()


# --------------------
# - Factory class to build process object
# - Inherits PyDataProcess.CTaskFactory from Ikomia API
# --------------------
class DatasetClassificationFactory(dataprocess.CTaskFactory):

    def __init__(self):
        dataprocess.CTaskFactory.__init__(self)
        # Set process information as string here
        self.info.name = "dataset_classification"
        self.info.short_description = "Load classification dataset"
        # relative path -> as displayed in Ikomia application process tree
        self.info.path = "Plugins/Python/Dataset"
        self.info.version = "1.0.3"
        self.info.icon_path = "icons/icon.png"
        self.info.authors = "Ikomia team"
        self.info.article = ""
        self.info.journal = ""
        self.info.year = 2023
        self.info.license = "MIT License"
        # URL of documentation
        self.info.documentation_link = ""
        # Code source repository
        self.info.repository = "https://github.com/Ikomia-hub/dataset_classification"
        # Keywords used for search
        self.info.keywords = "Dataset, Data Loader, Classification"
        self.info.algo_type = core.AlgoType.DATASET
        self.info.algo_tasks = "CLASSIFICATION"

    def create(self, param=None):
        # Create process object
        return DatasetClassification(self.info.name, param)
