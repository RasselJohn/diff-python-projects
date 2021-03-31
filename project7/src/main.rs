// hide console
#![windows_subsystem = "windows"]

mod game;
mod generator;


use fltk::*;

use game::Game;


fn main() {
    let app = app::App::default();
    let mut main_window = Game::new();

    main_window.game_window.end();
    main_window.game_window.show();

    main_window.add_events();
    main_window.add_button_events();

    while app.wait() {
        main_window.check_event_loop();
    }
}
