# event-reminder
### Simple Python programme that shows messages at a specific date with crontab-like scheduling expressions.

Configure it to run periodically (e.g. at login, at a specific hour each day, etc.). **[TODO: provide .bat to enable on Windows Task Scheduler and .timer for Systemd]**  
Once run, this programme reads the text file set in *config.ini* (on Linux, it can also resolve symlinks) to find entries whose specified date matches the current one. Then, a popup shows up with their description.  
That's it.  

![popup_sample](https://user-images.githubusercontent.com/52630493/116807642-961c0580-ab34-11eb-8f44-b00ef24973f1.jpg)  

## Event file syntax
The syntax to use in the text file is similar to that of Crontab.  

`#` indicates a comment, everything after that will be ignored.

As the file is, ideally, checked daily, the only date values that can be specified are, in order, **day**, **month** and **weekday**.  

The entries **must** be separated by a blank space.  

Following the date values is the event description, which has the following structure `title; description[; more]`.  

For example, a reminder for Mr. Nobody's birthday, which happens on the 30th of February, could be the following:
```
30 2 * Mr. Nobody; happy birthday to Nobody! #this is a comment and will be ignored
```

## More details on date checks
The date checks can be specified as follows.  
1. A wildcard `*` to mean that any value is good.
1. A specific number `n`, which has to be in range (1-31 for days, 1-12 for months and 1-7 for weekdays).
1. A range of values `n-m`, where *n <= m*, to indicate any value in the interval *[n,m]* (*n* and *m* must be in range as specified above).
1. A congruence class `r/d`, where *r* is either a number between 0 and 99 or a wildcard \*, and *d* is a number between 1 and 99. A value *v* satisfies this requisite if *v mod d = r*, i.e. if the remainder of *v* divided by *d* is *r*. A value of \* for *r* is the same as 0 so that, for example, `*/2` is the same as `0/2` and is satisfied by every even number. With this syntax, for example, the usual Crontab way of specifying odd months becomes `1/2` instead of *1-11/2*.

Every entry may have multiple checks, separated by comma. In this case, a value passes if at least one of the checks is valid.  
Thus, an event happening every third month if it is not Wednesday or Sunday and the day is either odd or one of the first four, could be written as follows:
```
1/2,1-4 0/3 1-2,4-6 Event title; event description; even more text
```

More examples can be found in *events.sample* and in *eventreminder/tests/cron_events_test*.

If, during the execution, one or more badly-formatted lines are found, their index will be written on the log file.
