from locust import HttpUser, task
from PIL import Image
import numpy as np

# Helper function to preprocess images
def preprocess_image(image_path):
    img = Image.open(image_path).convert("L")
    img = img.resize((256, 256))
    img_array = np.array(img).flatten()
    return img_array.tolist()

class LoadTestUser(HttpUser):
    host = "https://project-qmijp.northeurope.inference.ml.azure.com"

    @task
    def make_inference(self):
        # Preprocess a sample image
        image_data = preprocess_image("/Users/finn/Documents/practical-3-finn-murray/production/sample.jpg")
        
        # Define the payload
        payload = {
            "input_data": {
                "columns": [f"pixel_{i}" for i in range(256 * 256)],
                "data": [image_data]
            },
            "params": {}
        }

        # Replace <your-api-key> with the actual API key
        headers = {
            "Authorization": "Bearer F8oQ31PQ2jzMKIByblfbGm3EFLokYQUf",  # Replace <your-api-key> with the Primary Key
            "Content-Type": "application/json"
        }

        # Send the POST request to the scoring endpoint
        response = self.client.post(
            "/score",
            json=payload,
            headers=headers
        )

        # Log the response for debugging
        print(f"Response status: {response.status_code}, Response body: {response.text}")



