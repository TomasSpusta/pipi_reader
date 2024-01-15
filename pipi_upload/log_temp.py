from datetime import datetime



def write_log_temp (log_message):
    temp_log_address = "/home/bluebox/pipi_reader/pipi_upload/log_temp.txt"
    #temp_log_address = "pipi_upload/temp_log.txt"
    f = open (temp_log_address, "a")
    f.write (str(datetime.now()))
    f.write ("\n")
    f.write (log_message)
    f.write ("\n")
    f.close()  
    
