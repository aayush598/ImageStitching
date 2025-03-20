import cv2
import numpy as np
import os

def stitch_images_sift():
    folder = "extracted_frames"
    output_image = "stitched_image.jpg"

    # Get sorted list of image files
    image_files = sorted([f for f in os.listdir(folder) if f.endswith(('.jpg', '.png'))])

    # Check if enough images exist
    if len(image_files) < 2:
        print("Need at least two images for stitching.")
        return

    # Read all images
    images = [cv2.imread(os.path.join(folder, img)) for img in image_files]

    # Initialize SIFT
    sift = cv2.SIFT_create()
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    stitched_image = images[0]  # Start with first image

    for i in range(1, len(images)):
        img1 = stitched_image
        img2 = images[i]

        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Detect keypoints and descriptors
        kp1, des1 = sift.detectAndCompute(gray1, None)
        kp2, des2 = sift.detectAndCompute(gray2, None)

        # Match descriptors
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        # Get keypoints from matches
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        # Compute homography
        H, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC)

        # Warp the second image
        height, width = img1.shape[:2]
        img2_warped = cv2.warpPerspective(img2, H, (width + img2.shape[1], height))

        # Place first image on the stitched canvas
        img2_warped[0:height, 0:width] = img1

        # Update stitched image
        stitched_image = img2_warped

    # Save the final stitched image
    cv2.imwrite(output_image, stitched_image)
    print(f"Stitched image saved as {output_image}")

# Run stitching function
stitch_images_sift()
