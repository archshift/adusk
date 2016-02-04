extern crate sdl2;

mod ui;
mod utils;

use ui::keyboard::Keyboard;
use ui::renderable::Renderable;
use utils::units::Rect;

struct Screen {
    size: Rect,
}

impl Screen {
    fn new(width: i32, height: i32) -> Screen {
        Screen {
            size: Rect {
                pos: (0.0, 0.0),
                size: (width as f32, height as f32),
            },
        }
    }
}

fn main() {
    let sdl_context = sdl2::init().unwrap();
    let sdl_video_context = sdl_context.video().unwrap();

    let mut window = match sdl_video_context.window("adusk", 640, 480)
            .position_centered()
            .borderless()
            .opengl()
            .build() {
        Ok(window) => window,
        Err(err) => panic!("failed to create window: {}", err)
    };

    window.show();

    let mut renderer = match window.renderer().accelerated().build() {
        Ok(renderer) => renderer,
        Err(err) => panic!("failed to create renderer: {}", err)
    };

    let screen = Screen::new(640, 480);
    let keyboard = Keyboard::new();

    'event : loop {
        for event in sdl_context.event_pump().unwrap().poll_iter() {
            match event {
                sdl2::event::Event::Quit{..} => break 'event,
                _ => continue
            }
        }

        renderer.set_draw_color(sdl2::pixels::Color::RGB(0, 0, 0));
        renderer.clear();

        keyboard.render(&mut renderer, &screen.size);

        renderer.present();
    }
}
