from mrs.models import ProcessTypeStatus


def get_next_status(current_status_id):
    current_status = ProcessTypeStatus.objects.get(current_status_id)
    if not current_status.is_final:
        return ProcessTypeStatus.objects.filter(sequence_number=current_status.sequence_number + 1,
                                                process_type=current_status.process_type,
                                                project=current_status.project).first()
    else:
        return None
