use sdl2;

use ui;
use ui::Renderable;
use utils::units::Rect;

pub struct Ui {
    sdl: sdl2::Sdl,
    sdl_video: sdl2::VideoSubsystem,
    sdl_renderer: sdl2::render::Renderer<'static>,
    keyboard: ui::Keyboard,
}

impl Ui {
    pub fn new() -> Ui {
        let sdl_context = sdl2::init().unwrap();
        let sdl_video_context = sdl_context.video().unwrap();

        let mut window = match sdl_video_context.window("adusk", 960, 480)
                .position_centered()
                .borderless()
                .opengl()
                .build() {
            Ok(window) => window,
            Err(err) => panic!("failed to create window: {}", err),
        };

        window.show();

        let mut renderer = match window.renderer().accelerated().build() {
            Ok(renderer) => renderer,
            Err(err) => panic!("failed to create renderer: {}", err),
        };

        let keyboard = ui::Keyboard::new();

        Ui {
            sdl: sdl_context,
            sdl_video: sdl_video_context,
            sdl_renderer: renderer,
            keyboard: keyboard,
        }
    }

    pub fn keyboard_mut(&mut self) -> &mut ui::Keyboard {
        &mut self.keyboard
    }

    pub fn update(&mut self) -> bool {
        for event in self.sdl.event_pump().unwrap().poll_iter() {
            match event {
                sdl2::event::Event::Quit{..} => return false,
                _ => continue,
            }
        }

        let sdl_size = self.sdl_renderer.window().unwrap().size();

        self.sdl_renderer.set_draw_color(sdl2::pixels::Color::RGB(0, 0, 0));
        self.sdl_renderer.clear();

        let size = Rect {
            pos: (0.0, 0.0),
            size: (sdl_size.0 as f32, sdl_size.1 as f32),
        };
        self.keyboard.render(&mut self.sdl_renderer, &size);

        self.sdl_renderer.present();

        true
    }
}

struct UiLayout {

}

struct UiTheme {

}
