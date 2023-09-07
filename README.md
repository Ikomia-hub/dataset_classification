<div align="center">
  <img src="https://raw.githubusercontent.com/Ikomia-hub/dataset_classification/main/icons/icon.png" alt="Algorithm icon">
  <h1 align="center">dataset_classification</h1>
</div>
<br />
<p align="center">
    <a href="https://github.com/Ikomia-hub/dataset_classification">
        <img alt="Stars" src="https://img.shields.io/github/stars/Ikomia-hub/dataset_classification">
    </a>
    <a href="https://app.ikomia.ai/hub/">
        <img alt="Website" src="https://img.shields.io/website/http/app.ikomia.ai/en.svg?down_color=red&down_message=offline&up_message=online">
    </a>
    <a href="https://github.com/Ikomia-hub/dataset_classification/blob/main/LICENSE.md">
        <img alt="GitHub" src="https://img.shields.io/github/license/Ikomia-hub/dataset_classification.svg?color=blue">
    </a>    
    <br>
    <a href="https://discord.com/invite/82Tnw9UGGc">
        <img alt="Discord community" src="https://img.shields.io/badge/Discord-white?style=social&logo=discord">
    </a> 
</p>

This algorithm allows to load a classification dataset from a given folder. It can also split the dataset into train and validation folders. 

Any classification training algorithms from Ikomia HUB can be connected.


## :rocket: Use with Ikomia API

#### 1. Install Ikomia API

We strongly recommend using a virtual environment. If you're not sure where to start, we offer a tutorial [here](https://www.ikomia.ai/blog/a-step-by-step-guide-to-creating-virtual-environments-in-python).

```sh
pip install ikomia
```

#### 2. Create your workflow

```python
from ikomia.dataprocess.workflow import Workflow
from ikomia.utils import ik

# Init your workflow
wf = Workflow()

# Add the dataset loader to load your custom data and annotations
algo = wf.add_task(name="dataset_classification", auto_connect=False)

algo.set_parameters({"dataset_folder":"path/to/dataset/folder"})

# Add the training task to the workflow
resnet = wf.add_task(name="train_torchvision_resnet" , auto_connect=True)

# Launch your training on your data
wf.run()
```

## :sunny: Use with Ikomia Studio

Ikomia Studio offers a friendly UI with the same features as the API.

- If you haven't started using Ikomia Studio yet, download and install it from [this page](https://www.ikomia.ai/studio).

- For additional guidance on getting started with Ikomia Studio, check out [this blog post](https://www.ikomia.ai/blog/how-to-get-started-with-ikomia-studio).

## :pencil: Set algorithm parameters


- **dataset_folder** (str): Path to the dataset folder.

- **split_dataset** (bool, *optional*): If True, your dataset will be split into train and validation folders.
- **dataset_split_ratio** (float, *optional*) – default: '0.8': Divide the dataset into train and evaluation sets, ]0, 1[.
- **output_folder** (str, *optional*): Path to the output folder where the split dataset will be saved.
- **seed** (int, *optional*) - default '42': A seed value for the dataset slip. 


```python
import ikomia
from ikomia.dataprocess.workflow import Workflow

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="dataset_classification", auto_connect=False)

algo.set_parameters({
    "dataset_folder":"path/to/dataset/folder",
    "split_dataset": "True",
    "dataset_split_ratio": "0.9",
    "output_folder": "path/to/output/folder",
    "seed": "25"
})

# Add the training task to the workflow
resnet = wf.add_task(name="train_torchvision_resnet" , auto_connect=True)

# Launch your training on your data
wf.run()
```


## :fast_forward: Advanced usage 

The dataset_classification algorithm is designed to load datasets for training classification models from Ikomia HUB.

In addition to its primary purpose, this algorithm offers a convenient feature to effortlessly split the dataset into separate train and validation folders, adhering to the following organized structure:

```
Dataset_folder
├── train
│   ├── class-one
│   │   ├── IMG_1.jpg
│   │── class-two
│   │   ├── IMG_2.jpg
│   └── class-three
│       ├── IMG_3.jpg
├── val
│   ├── class-one
│   │   ├── IMG_4.jpg
│   │── class-two
│   │   ├── IMG_5.jpg
│   └── class-three
│       ├── IMG_6.jpg

```
