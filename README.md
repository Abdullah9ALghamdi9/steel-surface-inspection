# Steel Surface Inspection

### AI-Powered Steel Defect Classification System

An end-to-end Deep Learning project designed to automatically classify surface defects in steel using Convolutional Neural Networks (CNNs).

The system integrates a trained PyTorch model with a FastAPI backend and a modern web interface, allowing users to upload steel surface images and receive classification results and inspection recommendations.

## Project Overview

Steel surface defects can affect product quality and manufacturing efficiency. Manual inspection can be time-consuming and inconsistent.

This project explores how Deep Learning can support automated industrial quality inspection by identifying six types of steel surface defects.

## Dataset

**Dataset:** NEU Surface Defect Database (NEU-CLS)

- 1,800 original grayscale images
- 1,799 images after removing one exact duplicate
- 6 defect categories
- Image resolution: 200 × 200 pixels
- Nearly balanced class distribution

### Defect Categories

1. Crazing (Cr)
2. Inclusion (In)
3. Pitted Surface (PS)
4. Patches (Pa)
5. Rolled-in Scale (RS)
6. Scratches (Sc)

## Deep Learning Models

Three CNN architectures were developed and compared:

- **Model 1: Baseline CNN** — A simple convolutional neural network.
- **Model 2: Improved CNN** — A CNN using Batch Normalization and Dropout.
- **Model 3: Residual CNN** — A deeper CNN incorporating residual connections.

## Model Performance

| Model | Validation Macro F1 |
|---|---:|
| Baseline CNN | 53.69% |
| Improved CNN | 94.40% |
| Residual CNN | 97.77% |

### Final Test Results

The selected Residual CNN achieved:

- **Test Accuracy:** 100%
- **Test Macro F1:** 100%
- **Correct Predictions:** 180/180

These results were obtained on the NEU-CLS held-out test split. Performance on new industrial images may differ, and further testing is necessary before real-world deployment.

## Web Application

The web application allows users to:

- Upload steel surface images.
- Automatically classify the detected defect type.
- View prediction scores across six defect categories.
- Receive a brief inspection recommendation.

The system uses **FastAPI** to connect the PyTorch model to the web interface.

## Technologies Used

- Python
- PyTorch
- Torchvision
- NumPy
- Pandas
- Scikit-learn
- Matplotlib
- FastAPI
- HTML, CSS, JavaScript
- Jupyter Notebook

## Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Place the trained model weights (`steel_residual_best.pth`) in the application's `models` directory.

Start the FastAPI server from the application directory:

```bash
python -m uvicorn main:app --reload
```

Open:

http://127.0.0.1:8000

## Limitations

- The model is trained to classify six known defect categories.
- It does not independently verify whether a steel surface is defect-free.
- The dataset does not provide ground-truth defect severity labels.
- Prediction scores do not represent actual defect size or severity.
- Further testing on independent industrial data is required.

## Future Improvements

- Expand the training dataset.
- Add defect localization using object detection.
- Develop severity assessment using appropriately labeled data.
- Improve performance on real-world industrial images.
- Deploy the application online.

## Project Goal

This project was developed primarily for educational purposes to strengthen practical skills in Deep Learning
