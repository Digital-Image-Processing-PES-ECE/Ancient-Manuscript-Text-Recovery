# Ancient Manuscript Text Recovory
### Project Description:
#### Summary - 
An image processing project focused on enhancing and analyzing historical text documents through various image processing techniques making it sompler for any OCR to then recognise the text

#### Course concepts used - 
1. Adaptive Thresholding
2. Morphological Operations which include Closing and Hit or miss transforms
3. Image enhancement using Histogram equalization
4. Gaussian Blur for Noise Reduction
5. Skeletonization of The text for better charchter recognition

#### Additional concepts used -
1. We use Peak Signal to Noise Ratio and Mean square error to compare images and test their quality
2. Image Pruning using PlantCV for better enhancment of text
   
#### Dataset - 
We used images from two websites
https://digi.vatlib.it/view/MSS_Vat.lat.3225
https://www.roger-pearse.com/weblog/2018/10/29/fragments-of-a-4th-century-manuscript-of-cyprians-letters/

#### Novelty - 
1. Integration of multiple image processing techniques in a sequential manner
2. Implementation of quality metrics for comparing processing results
   
### Contributors:
1. Harshith PVS (PES1UG22EC087)
2. Manu L (PES1UG22EC155)
3. Pradyumn Prashant Prabhu (PES1UG22EC195)

### Steps:
1. Clone Repository
```
git clone https://github.com/Digital-Image-Processing-PES-ECE/project-name.git
```
2. Install Dependencies
```
pip install -r requirements.txt

```
3. Run the Code
```
python DIP_Project.py
```

### Outputs:
These our are final output images:

All outputs are automatically saved as PNG files

### References:

   
### Limitations and Future Work:
1. Current implementation is limited to grayscale processing
2. Fixed parameters for adaptive thresholding and morphological operations
3. Limited to specific image format and size

Future Improvements:
1. Adaptive parameter selection based on input image 
2. Addition of OCR capabilities for text extraction
3. Batch processing capabilities for multiple documents