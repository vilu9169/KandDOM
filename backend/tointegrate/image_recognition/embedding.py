from typing import Optional

import vertexai
from vertexai.vision_models import (
    Image,
    MultiModalEmbeddingModel,
    MultiModalEmbeddingResponse,
)


def get_image_embeddings(
    project_id: str,
    location: str,
    image_path: str,
    contextual_text: Optional[str] = None,
) -> MultiModalEmbeddingResponse:
    """Example of how to generate multimodal embeddings from image and text.

    Args:
        project_id: Google Cloud Project ID, used to initialize vertexai
        location: Google Cloud Region, used to initialize vertexai
        image_path: Path to image (local or Google Cloud Storage) to generate embeddings for.
        contextual_text: Text to generate embeddings for.
    """

    vertexai.init(project=project_id, location=location)

    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    image = Image.load_from_file(image_path)

    embeddings = model.get_embeddings(
        image=image,
        contextual_text=contextual_text,
    )
    print(f"Image Embedding: {embeddings.image_embedding}")
    print(f"Text Embedding: {embeddings.text_embedding}")


get_image_embeddings("robust-summit-417910", "europe-west4", "backend/tointegrate/multi_modal_processing/jpgs/page0.jpg")