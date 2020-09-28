from datetime import datetime


def get_age_in_secs(birth_time_utc):
  if type(birth_time_utc) is int:
    while birth_time_utc > 9999999999:
      birth_time_utc = int(birth_time_utc / 1000)
    bt = datetime.fromtimestamp(birth_time_utc)
    now = datetime.now()
    age_in_sec = (now - bt).total_seconds()
    return age_in_sec
  else:
    raise Exception("Expected timestamp " + str(birth_time_utc) + " to be of type int but is " + str(type(birth_time_utc)))
