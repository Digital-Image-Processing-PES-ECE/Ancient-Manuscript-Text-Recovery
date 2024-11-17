import cv2
import matplotlib
import numpy as np
from skimage import exposure, morphology
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from plantcv import plantcv as pcv

matplotlib.use('tkagg')


def display_image(title, image):
    filename = title.replace(" ", "_") + ".png"
    plt.imsave(filename, image, cmap='gray')
    print(f"{title} saved as {filename}")



def process_image(image_path, kernel):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    return processed


def compare_images(img1, img2, method):
    if method == 'mse':
        return np.mean((img1 - img2) ** 2)
    elif method == 'psnr':
        mse = np.mean((img1 - img2) ** 2)
        if mse == 0:
            return float('inf')
        return 20 * np.log10(255.0 / np.sqrt(mse))
    elif method == 'ssim':
        return ssim(img1, img2)


def main():
    image_path = 'data/image.png'
    image = cv2.imread(image_path)

    #grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_image('Grayscale Image', gray)

    #Histogram equalization
    equalized = exposure.equalize_hist(gray) * 255
    equalized = equalized.astype(np.uint8)
    display_image('Contrast Enhanced', equalized)

    #Gaussian blur
    blurred = cv2.GaussianBlur(equalized, (5, 5), 0)
    display_image('Gaussian Blurred', blurred)

    #Thresholding
    adaptive_thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 15, 10
    )
    display_image('Adaptive Thresholding', adaptive_thresh)

    #Morphological closing
    kernel = np.ones((2, 2), np.uint8)
    morph_text = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)
    display_image('Morphological Closing', morph_text)

    #Skeletonisation
    skeleton = morphology.skeletonize(morph_text // 255)
    skeleton = (skeleton * 255).astype(np.uint8)
    display_image('Skeletonized Text', skeleton)

    #Pruning
    pruned_skeleton, seg_img, seg_obj = pcv.morphology.prune(skeleton, size=0.5)
    cv2.imshow("Pruned_Skeleton", pruned_skeleton)


    #Hit or miss transform
    struct_elem = np.array([[0, 1, 0],
                            [1, 1, 1],
                            [0, 1, 0]], dtype=np.uint8)
    hit_or_miss = cv2.morphologyEx(pruned_skeleton, cv2.MORPH_HITMISS, struct_elem)
    display_image('Hit-or-Miss Transformation', hit_or_miss)

    combined = cv2.addWeighted(equalized, 0.5, hit_or_miss, 0.5, 0)
    display_image('Combined Enhanced Text', combined)
    cv2.imwrite("Processed_Image.jpg", combined)
    print("Processed image saved as Processed_Image.jpg")

    #-------------Quality Assurance Testing-----------------------
    ground_truth = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    structuring_elements = {
        'Rectangle': cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),
        'Cross': cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3)),
        'Ellipse': cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    }
    results = []
    for name, kernel in structuring_elements.items():
        processed_image = process_image(image_path, kernel)

        #Mean square error
        mse_value = compare_images(ground_truth, processed_image, method='mse')

        #Peak signal to noise ratio
        psnr_value = compare_images(ground_truth, processed_image, method='psnr')

        #Structural Similarity Index Measure
        ssim_value = compare_images(ground_truth, processed_image, method='ssim')

        results.append((name, processed_image, mse_value, psnr_value, ssim_value))

        print(f'Structuring Element: {name}')
        print(f'MSE: {mse_value}')
        print(f'PSNR: {psnr_value}')
        print(f'SSIM: {ssim_value}\n')

    max_mse_img = max(results, key=lambda item: item[2])[1]
    min_psnr_img = min(results, key=lambda item: item[3])[1]
    min_ssim_img = min(results, key=lambda item: item[4])[1]

    cv2.imwrite('max_mse_image.jpg', max_mse_img)
    cv2.imwrite('min_psnr_image.jpg', min_psnr_img)
    cv2.imwrite('min_ssim_image.jpg', min_ssim_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
