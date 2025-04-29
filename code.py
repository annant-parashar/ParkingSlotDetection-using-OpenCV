import cv2
import numpy as np

def detect_parking_slots(image_path):
    """
    Detect parking slots and calculate total, occupied, and empty slots.

    :param image_path: Path to the parking lot image.
    :return: Total slots, occupied slots, empty slots.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return 0, 0, 0

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding to create a binary image
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Invert the binary image to make the cars and slots more detectable
    binary = cv2.bitwise_not(binary)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize counters
    total_slots = 0
    occupied_slots = 0

    # Create a copy of the original image for visualization
    output_image = image.copy()

    # Loop through each contour
    for contour in contours:
        # Get the bounding rectangle for each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Filter by size (adjust based on the image)
        if 80 < w < 150 and 80 < h < 150:  # Update these thresholds based on slot size
            total_slots += 1

            # Extract the region of interest (ROI)
            roi = binary[y:y+h, x:x+w]

            # Check if the slot is occupied
            black_pixels = cv2.countNonZero(roi)
            total_pixels = w * h

            # If more than 50% of the slot area is black, it's considered occupied
            if black_pixels > total_pixels * 0.5:
                occupied_slots += 1
                # Draw a red rectangle for occupied slots
                cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(output_image, "Occupied", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            else:
                # Draw a green rectangle for empty slots
                cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(output_image, "Empty", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Calculate empty slots
    empty_slots = total_slots - occupied_slots

    # Display the processed image
    cv2.imshow("Parking Lot Detection", output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return total_slots, occupied_slots, empty_slots


def main():
    # Path to the input image
    image_path = r"D:\mini_project/parking_slot.jpeg"

    # Detect parking slots
    total, occupied, empty = detect_parking_slots(image_path)

if __name__ == "__main__":
    main()
