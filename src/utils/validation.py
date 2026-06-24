def validate_pdf_file(
        file):

    if hasattr(
            file,
            "name"
    ):

        file_name = file.name

    else:

        file_name = str(
            file
        )

    if not file_name.lower().endswith(
            ".pdf"
    ):

        raise ValueError(
            "Only PDF files allowed"
        )

    return True