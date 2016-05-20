extern crate sdl2;
extern crate xdg;
extern crate yaml_rust;

use yaml_rust::yaml;

// mod resources;
mod ui;
mod utils;

fn create_kb(kb: &mut ui::Keyboard) {
    let yaml_docs = {
        let yaml_str = include_str!("../data/cfg/keyboard-layout.yaml");
        yaml::YamlLoader::load_from_str(yaml_str).unwrap()
    };
    let yaml_main = &yaml_docs[0];

    let mut key_rows = Vec::<Vec<ui::Key>>::new();

    for row in yaml_main["keys"].as_vec().unwrap() {
        let mut keys = Vec::<ui::Key>::new();

        for key in row.as_vec().unwrap() {
            let label = key["label"].as_str().unwrap_or("");
            let behavior = key["behavior"].as_str().unwrap_or("letter");
            let keycode = key["keycode"].as_str();
            let width_weight = key["width_weight"].as_f64().unwrap_or(1.0) as f32;

            let mut key = ui::Key::new(label.to_owned());
            key.set_width_weight(width_weight);
            keys.push(key);

            println!("label:{}, behavior:{}, keycode:{:?}, width_weight:{}",
                label, behavior, keycode, width_weight);
        }

        key_rows.push(keys);
    }

    kb.set_keys(key_rows);
}

fn main() {
    let mut ui = ui::Ui::new();

    create_kb(ui.keyboard_mut());

    loop {
        if !ui.update() {
            break;
        }
    }
}
