use chrono::prelude::*;

pub fn curdate() -> [i32; 3] {
    let date: DateTime<Local> = Local::now();
    [date.month() as i32, date.day() as i32, date.year() as i32]
}

pub fn day() -> [i32; 12] {
    [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
}

pub fn month() -> [&'static str; 12] {
    [ "January", "February", "March",
    "April", "May", "June", "July",
    "August", "September", "October",
    "November", "December"]
}

pub fn leapyear(year: i32) -> bool {
    return year % 4 == 0 && year % 100 != 0 || year % 400 == 0;
}