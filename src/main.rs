use colored::*;
use std::time::Instant;
mod helpers;
mod day_01;


fn print_divider_green(day: String, p1_result: String, p2_result: String) {
    println!("{}", "-----------------------".bright_green());
    println!("{} {}", "Day ".bright_green(), day.bright_green());
    println!("{}", "-----------------------".bright_green());
    println!("{}\n{}", p1_result, p2_result);
}

fn print_divider_red(day: String, p1_result: String, p2_result: String) {
    println!("{}", "-----------------------".bright_red());
    println!("{} {}", "Day ".bright_red(), day.bright_red());
    println!("{}", "-----------------------".bright_red());
    println!("{}\n{}", p1_result, p2_result);
}

fn main() {
    let sum_time = Instant::now();
    println!("\n{}", "Advent of Code 2021".bright_white());
    // Day 1
    let start = Instant::now();
    let p1 = day_01::part_1(helpers::read_file_ints("./inputs/day_01.txt").unwrap());
    let p2 = day_01::part_2(helpers::read_file_ints("./inputs/day_01.txt").unwrap());
    print_divider_green(format!("01 - {:?}", start.elapsed()), p1, p2);

    // Sum
    println!(
        "\nTotal run time: {}",
        format!("{:?}", sum_time.elapsed()).bright_white()
    );
}
