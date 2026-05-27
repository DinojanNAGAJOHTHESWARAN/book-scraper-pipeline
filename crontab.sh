#min, hour, dayOfMonth, month, dayOfWeek, command

#field   allowed values
#-------- --------------
#minute   0-59
#hour     0-23
#dayOfMonth 1-31
#month    1-12
#dayOfWeek 0-6 (0 is Sunday)


#* * * * * echo "Hello World" >> /app/result.output 2>&1
#run a command every minute
#min, hour, dayOfMonth, month, dayOfWeek, command

* * * * * cd /app/App && /app/venv/bin/python -u main.py >> /app/data/result.output 2>&1
