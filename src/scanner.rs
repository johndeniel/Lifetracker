use std::io::{self, BufRead};

pub fn input(ask: &str) -> i32 {
    println!("{}", ask);
    loop {
        let input: Result<i32, std::num::ParseIntError> = io::stdin()
            .lock()
            .lines()
            .next()
            .expect("Failed to read line")
            .expect("No input provided")
            .trim()
            .parse::<i32>();

        match input {
            Ok(num) => return num,
            Err(_) => println!("Invalid input, please enter an integer:"),
        };
    }
}