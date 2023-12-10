from datetime import datetime, timedelta


class Util:
    
    @staticmethod   
    def add_duration(start_time, duration_minutes):
        # Convert the start time to a datetime object
        
        input_time = start_time
        time_obj = datetime.strptime(input_time, '%H:%M:%S')
        start_datetime = time_obj.strftime('%I:%M %p')

        # Add the duration in minutes
        end_datetime = start_datetime + timedelta(minutes=int(duration_minutes))

        # Format the end time
        end_time = end_datetime.strftime("%I:%M %p")

        return end_time