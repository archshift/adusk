mod ui;
mod utils;

fn main() {
    let mut ui = ui::Ui::new();
    loop {
        if !ui.update() {
            break;
        }
    }
}
