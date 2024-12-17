def get_converted_file_name(converted_file_model):
    def inner(file_uuid):
        try:
            file_instance = converted_file_model.objects.get(uuid=file_uuid)

            return file_instance.name
        except Exception as err:
            print("Unnable to retrieve file: ",err)
            return None
        
    return inner