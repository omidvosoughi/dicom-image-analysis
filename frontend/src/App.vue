<template>
  <!-- Main container for the Vue application -->
  <div id="app">
    
    <!-- Title of the page, centered at the top -->
    <h1 class="display-1" style="text-align: center;">DICOM Image Analysis</h1>

    <!-- Layout for file upload and configuration options -->
    <div class="row">
      <div class="col">
        <!-- Dropzone component for file uploads (DICOM images) -->
        <vue-dropzone ref="myVueDropzone" id="dropzone" :options="dropzoneOptions" style="margin: 25px; border-radius: 10px;"></vue-dropzone>
      </div>

      <div id="config" class="col">
        <!-- UI for entering the threshold value -->
        <div class="row">
          <b-alert show variant="secondary">Enter Threshold Value</b-alert>
        </div>
        <div class="row">
          <!-- Numeric input for setting the threshold value -->
          <b-form-input type="number" v-model="threshold" step="0.0001" min="0" max="1"></b-form-input>
        </div>
        <div class="row">
          <!-- Button to trigger the file upload process -->
          <b-button variant="primary" @click="processUpload">Upload File</b-button>
        </div>
      </div>
    </div>

    <!-- Section to display upload status and results -->
    <div class="row">
      <div class="col">
        <!-- Alert showing the name of the uploaded file -->
        <b-alert v-if="uploadedFileName" variant="success" show style="text-align: center; margin: 25px; font-size: larger; font-weight: bold;">Uploaded File: {{ uploadedFileName }}</b-alert>

        <!-- Alert displaying the calculated thresholded pixel volume -->
        <b-alert v-if="thresholdedPixelVolume" show style="text-align: center; margin: 25px; font-size: larger; font-weight: bolder;">Thresholded Pixel Volume: {{ thresholdedPixelVolume }} mm<sup>3</sup></b-alert>
      </div>

      <!-- Section to display the generated image plot -->
      <div id="plot" class="col">
        <img v-if="uploadedImageUrl" :src="uploadedImageUrl" alt="Image Analysis" />
      </div>
    </div>
  </div>
</template>

### Vue Component Script
```javascript
<script>
// Imports
import vueDropzone from 'vue2-dropzone'; // Importing the vue2-dropzone component
import 'vue2-dropzone/dist/vue2Dropzone.min.css'; // Importing default styles for vue2-dropzone
import axios from 'axios'; // Importing axios for HTTP requests

export default {
  name: 'App', // Component name
  components: {
    vueDropzone // Registering vueDropzone as a component
  },
  data() {
    return {
      // Dropzone configuration options
      dropzoneOptions: {
        url: 'http://127.0.0.1:8000/upload', // Backend URL for file uploads
        maxFilesize: 2, // Max file size in MB
        maxFiles: 1, // Max number of files
        dictDefaultMessage: "<i class='fa fa-cloud-upload'></i>Drop DICOM images here or click to upload", // Custom message
        acceptedFiles: 'image/dicom,.dcm', // Accepted file types
        addRemoveLinks: true, // Enable file removal option
        autoProcessQueue: false, // Disable auto-processing to allow manual upload trigger
      },
      // Reactive properties to store file info and analysis results
      uploadedFileName: '',
      thresholdedPixelVolume: '',
      uploadedImageUrl: null,
      threshold: 0.5055, // Default threshold value
      pngFilename: '',
    };
  },
  methods: {
    // Method to handle the upload process
    processUpload() {
      if (this.$refs.myVueDropzone) {
        const files = this.$refs.myVueDropzone.getAcceptedFiles();
        if (files.length > 0) {
          let formData = new FormData();
          files.forEach((file) => {
            formData.append('file', file); // Append file to FormData
          });
          formData.append('threshold', this.threshold.toString()); // Append threshold value

          // Making a POST request to the server with the FormData
          axios.post('http://127.0.0.1:8000/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          .then(response => {
            // Handling server response
            this.uploadedFileName = response.data.filename;
            this.thresholdedPixelVolume = response.data.pixelVolume;
            this.pngFilename = response.data.plotDirectory;
            this.uploadedImageUrl = 'http://127.0.0.1:8000/get-image/' + this.pngFilename;
          })
          .catch(error => {
            console.error('Error:', error);
          });
        } else {
          console.log('No files to upload');
        }
      }
      else {
        console.error('Dropzone is not initialized');
      }
    },
  },
};
</script>

### CSS Styles
```css
<style>
/* Importing FontAwesome for icons */
@import url("https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css");
/* Custom styles for the application */
body {
  background-color: rgba(0, 0, 0, 0.718) !important;
}
.display-1 {
  color: white; /* White color for the main title */
}
#plot img {
  margin: 25px;
  border-radius: 10px; /* Rounded corners for images */
}
#config {
  margin: 20px;
}
#config .row {
  padding: 5px;
  text-align: center;
  font-weight: bold; /* Bold text for config options */
}
.alert {
  margin-bottom: 0px !important;
}
#config input {
  text-align: center;
  font-weight: bold; /* Bold text for input fields */
}
#config button {
  font-weight: bold; /* Bold text for buttons */
}
</style>
