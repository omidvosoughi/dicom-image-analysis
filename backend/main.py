from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import magic
import os
from starlette.status import HTTP_400_BAD_REQUEST
import pydicom
import pydicom.data
import matplotlib.pyplot as plt
import numpy as np
from fastapi.staticfiles import StaticFiles

# Initialize the FastAPI app
app = FastAPI()

# Add CORS middleware to allow cross-origin requests from any origin
# This is useful during development or if the frontend is hosted separately
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the directory paths for uploads and plots
# Use os.makedirs to create these directories if they don't exist
UPLOAD_FOLDER = './uploads'
PLOT_DIRECTORY = "./plots"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_DIRECTORY, exist_ok=True)

# Function to check if the uploaded file is a DICOM file using the 'magic' library
def is_dicom_file(file_path):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    return 'dicom' in file_type

# Function to calculate the volume of pixels above a threshold in a DICOM file
def pixel_volume(file_path, threshold):
    # Read the DICOM file
    dataset = pydicom.dcmread(file_path)
    pixel_array = dataset.pixel_array

    # Obtain the slice thickness from the DICOM metadata
    slice_thickness = float(dataset.SliceThickness)

    # Normalize the pixel array to be between 0 and 1
    normalized = pixel_array.astype(np.float32) / pixel_array.max()

    # Initialize a selection matrix with the same dimensions as the normalized image
    # The matrix is filled with zeros and is of type 'float64'
    selection = np.zeros((normalized.shape[0],normalized.shape[1]), dtype='float64')

    # Iterate over each row of the normalized image matrix
    for row in range(0,(normalized.shape[0]-1)):
        # Iterate over each column in the current row
        for col in range(0,(normalized.shape[1]-1)):
            # Check if the pixel value exceeds the threshold
            if(normalized[row, col] > threshold):
                # If the condition is true, set the corresponding pixel in the selection matrix to 1
                selection[row, col] = 1
            else:
                # If the condition is false, set the corresponding pixel in the selection matrix to 0
                selection[row, col] = 0

    # Plot the various DICOM images and histograms
    plot_diagram(pixel_array, normalized, selection)

    # Calculate the volume by summing the non-zero pixels and multiplying by the slice thickness
    volume = sum(np.count_nonzero(selection, axis=0)) * slice_thickness

    return volume

# Function to plot and save diagrams of the DICOM image data
def plot_diagram(original_pixel, normalized_pixel, thresholded_pixel):
    # Set up a 2x2 grid of plots
    fig, axs = plt.subplots(2, 2)

    # Plot the original, normalized, and thresholded DICOM images and their histograms
    axs[0, 0].imshow(original_pixel, cmap='Greys_r')
    axs[0, 0].set_title('Original DICOM image')

    # Histogram of the grayscale normalized image
    normalized_histogram, normalized_bin_edges = np.histogram(normalized_pixel, bins=256, range=(0.0, 1.0))

    
    axs[0, 1].plot(normalized_bin_edges[0:-1], normalized_histogram)
    axs[0, 1].set_title('Grayscale normalized Histogram')

    axs[1, 0].imshow(thresholded_pixel, cmap='grey')
    axs[1, 0].set_title('Thresholded image')

    thresholded_histogram, thresholded_bin_edges = np.histogram(thresholded_pixel, bins=256, range=(0.0, 1.0))
    axs[1, 1].plot(thresholded_bin_edges[0:-1], thresholded_histogram)
    axs[1, 1].set_title('Binary thresholded Histogram')

    # Adjust the layout and save the figure
    fig.tight_layout()
    plt.savefig(f'{PLOT_DIRECTORY}/images.png')

# Define the FastAPI endpoint for uploading DICOM files
@app.post("/upload")
async def upload_dicom_file(file: UploadFile = File(...)):
    # Save the uploaded file to the uploads directory
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # Verify that the file is a DICOM file
    if not is_dicom_file(file_location):
        # Verify that the file is a DICOM file
        os.remove(file_location)
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="The uploaded file is not a valid DICOM file.")
    
    # Calculate the pixel volume with a given threshold
    volume = pixel_volume(file_location, 0.5055)
    # Return a JSON response with the status, filename, and calculated pixel volume
    return JSONResponse(status_code=200, content={"message": "File uploaded successfully", "filename": file.filename, "pixelVolume": f"{volume}"})

# Run the server using uvicorn if the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

