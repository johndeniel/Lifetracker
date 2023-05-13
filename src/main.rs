mod test;
mod driver;
mod scanner;
mod lifetracker;

fn main() {

    for number in driver::month().iter() {
        println!("{}", number);
    }
    
    let month = scanner::input("\nEnter Your Birth Month: ");
    let day = scanner::input("\nEnter Your Birth Day: ");
    let year = scanner::input("\nEnter Your Birth Year: ");   

    print!("\nYou are {} day old! ", lifetracker::computation(month, day, year, driver::curdate()));
}