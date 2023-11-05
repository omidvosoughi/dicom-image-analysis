<template>
  <!-- Main container for the Vue application -->
  <div id="app">
    <!-- Title of the page -->
    <h1 class="display-1" style="text-align: center;">DICOM Image Upload</h1>

    <!-- vue-dropzone component for handling file uploads -->
    <vue-dropzone
      ref="myVueDropzone"
      id="dropzone"
      :options="dropzoneOptions"
      @vdropzone-file-added="fileAdded"
      @vdropzone-success="handleSuccess"
      style="margin: 25px; border-radius: 10px;"
    ></vue-dropzone>

    <!-- Status alerts for upload feedback -->
    <div class="row">
      <!-- Alert for showing the name of the uploaded file -->
      <div class="col">
        <b-alert v-if="uploadedFileName" variant="success" show style="text-align: center; margin: 25px;
        font-size: larger; font-weight: bold;">Uploaded File: {{ uploadedFileName }}</b-alert>        
      </div>
      <!-- Alert for displaying the calculated thresholded pixel volume -->
      <div class="col">
        <b-alert v-if="thresholdedPixelVolume" show
        style="text-align: center; margin: 25px; font-size: larger; font-weight: bolder;">Thresholded Pixel Volume: {{ thresholdedPixelVolume }} mm<sup>3</sup>
        </b-alert>
      </div>
    </div>
  </div>
</template>

<script>
// Import the vue2-dropzone component and its default styles
import vueDropzone from 'vue2-dropzone';
import 'vue2-dropzone/dist/vue2Dropzone.min.css';

export default {
  name: 'App',
  components: {
    vueDropzone // Register vueDropzone as a component for use in this Vue instance
  },
  data() {
    return {
      // Options configuration for vue-dropzone
      dropzoneOptions: {
        url: 'http://127.0.0.1:8000/upload', // The backend URL to which the files will be uploaded
        thumbnailWidth: 150,
        maxFilesize: 2, // Maximum file size for uploads in MB
        dictDefaultMessage: "<i class='fa fa-cloud-upload'></i>Drop DICOM images here or click to upload",
        acceptedFiles: 'image/dicom,.dcm', // File types accepted for upload
        addRemoveLinks: true, // Allows users to remove files after uploading
      },
      uploadedFileName: '',  // Variable to store the name of the uploaded file
      thresholdedPixelVolume: '', // Variable to store the calculated volume of thresholded pixels
    };
  },
  methods: {
    fileAdded(file) {
      // Method triggered when a file is added to the dropzone
      // Here we can add additional checks or logging
      console.log('Added file:', file);
    },
    handleSuccess(file, response) {
      // Method triggered when a file upload is successful
      // Here we update the data properties with the response from the server
      this.uploadedFileName = response.filename; // Update the filename from the server response
      this.thresholdedPixelVolume = response.pixelVolume; // Update the pixel volume from the server response
    },
  },
};
</script>

<style>
/* Import FontAwesome for using its icons */
@import url("https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css");
/* Additional custom styles can be added here */
</style>

