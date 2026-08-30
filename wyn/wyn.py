import reflex as rx
from .state import State
from .components import (
    theme_toggle_button,
    hero_section,
    stats_bar,
    timeline_view,
    highlights_view,
    memory_map_view,
    completed_view,
    plans_view,
    footer,
    gallery_modal,
    lightbox_modal,
    plan_modal,
    edit_date_modal,
    countdown_banner,
)
from .styles import styles, get_theme_vars

def theme_vars() -> dict:
    """CSS variables for dark and light themes."""
    return get_theme_vars(State.theme_mode)


def index() -> rx.Component:
    """Main page builder with a unified grid layout."""
    return rx.box(
        theme_toggle_button(),
        
        # Central layout container
        rx.vstack(
            hero_section(),
            stats_bar(),
            countdown_banner(),
            
            # Switch views dynamically based on State.active_tab
            rx.box(
                rx.cond(
                    State.active_tab == "timeline",
                    timeline_view(),
                    rx.cond(
                        State.active_tab == "highlights",
                        highlights_view(),
                        rx.cond(
                            State.active_tab == "map",
                            memory_map_view(),
                            rx.cond(
                                State.active_tab == "completed",
                                completed_view(),
                                plans_view(),
                            ),
                        ),
                    ),
                ),
                width="100%",
                min_height="40vh",
            ),
            
            footer(),
            
            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding_x=rx.breakpoints(initial="1.5rem", sm="3rem", md="4rem"),
            spacing="6",
            align="stretch",
        ),
        
        # Overlay Dialogs
        gallery_modal(),
        lightbox_modal(),
        plan_modal(),
        edit_date_modal(),
        
        style={**styles["bg_main"], **theme_vars()},
    )


# Configure Reflex App
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap",
    ],
    style=styles["bg_main"],
)
app.add_page(index, title="JHCWCH", on_load=State.load_data)
