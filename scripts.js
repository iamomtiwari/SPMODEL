function upload() {

    const fileUploadInput = document.querySelector('.file-uploader');
  
    /// TEST CASES ///
  
    if (!fileUploadInput.value) {
      return;
    }
    // using index [0] to take the first file from the array
    const image = fileUploadInput.files[0];
    // Test 1:  if the file selected is not an image file
    if (!image.type.includes('image')) {
      return alert('Please choose an Image file');
    }
    // Test 2:  if size (in bytes) exceeds 10 MB
    if (image.size > 10_000_000) {
      return alert('The Image should be less than 10MB');
    }
  
    /// Display Image ///
  
    const fileReader = new FileReader();
    fileReader.readAsDataURL(image);
  
    fileReader.onload = (fileReaderEvent) => {
      const profilePicture = document.querySelector('.profile-picture');
      profilePicture.style.backgroundImage = `url(${fileReaderEvent.target.result})`;
    }
  
  }
