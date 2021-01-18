from datetime import timedelta

from mrs.models import Lift, MaintenancePlan, ScheduleEntry, Procedure


class MaintenanceService:
    def generate_plan(self, lift_id, name):
        lift = Lift.objects.get(id=lift_id)
        job = lift.job
        contract = job.contract
        days_frequency = contract.contract_mtn_frequency.days_frequency
        end_date = contract.end_datetime
        planed_date = contract.start_datetime

        # create plan
        maintenance_plan = MaintenancePlan(name=(name if name else lift.name),
                                           lift=lift,
                                           start_datetime=planed_date)
        maintenance_plan.save()

        days_delta = timedelta(days=days_frequency)
        while planed_date <= end_date:
            planed_date = planed_date + days_delta
            procedure = Procedure.objects.get(id=2)

            # add plan entry
            plan_entry = ScheduleEntry(maintenance_plan=maintenance_plan,
                                       procedure=procedure,
                                       schedule_date=planed_date)
            plan_entry.save()

        return days_frequency
