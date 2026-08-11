from celery import shared_task

from apps.imaging.services.dicom import (
    get_image_dimensions,
    get_transfer_syntax,
    read_dicom_metadata,
)


@shared_task(
    bind=True,
    name="apps.imaging.tasks.process_dicom",
)
def process_dicom(
    self,
    file_path,
):
    metadata = read_dicom_metadata(
        file_path
    )

    dimensions = get_image_dimensions(
        file_path
    )

    transfer_syntax = get_transfer_syntax(
        file_path
    )

    return {
        "status": "processed",
        "file_path": file_path,
        "metadata": metadata,
        "dimensions": dimensions,
        "transfer_syntax": transfer_syntax,
        "task_id": self.request.id,
    }