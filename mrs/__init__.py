import django

django.setup()

from mrs.tasks import master_programmed_task

#master_programmed_task(verbose_name="Programmed Tasks Master", repeat=5)
#master_programmed_task()
