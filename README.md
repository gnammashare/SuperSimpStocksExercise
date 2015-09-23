# SuperSimpStocksExercise
I created a simple 'server-side-feeling' application in python to implement the requirements. This includes a tester module to unit test (using pythons unit test packages) on the relevant functions/classes, checking that they deal adequately with incorrect types and/or invalid data. Due to the relatively small number of exception types,i've used existing exception classes in python and not subclassed/created my own.

The trades are stored in a sorted list ordered by timestamp, such that trade lookup and insert is sub-linear (log (n)), this means that the weighted-trade volume calculations (i.e. for the last n minutes) remains sub-linear.


Author: Sachi Arafat
