import reflex as rx
from .state import State
from .styles import (
    styles,
    ACCENT_COLOR,
    ACCENT_DARK,
    ACCENT_LIGHT,
    TEXT_MUTED,
    TEXT_WHITE,
    TEXT_SOFT,
    BORDER_COLOR,
    BORDER_COLOR_HOVER,
    SHADOW_GLOW,
    CARD_SHADOW,
    FONT_HEADING,
    FONT_BODY,
    BG_GRADIENT,
    get_theme_vars,
)

def theme_toggle_button() -> rx.Component:
    """Small floating theme switcher."""
    return rx.box(
        rx.icon_button(
            rx.cond(
                State.theme_mode == "dark",
                rx.icon("sun", size=18),
                rx.icon("moon", size=18),
            ),
            on_click=lambda: State.toggle_theme(),
            variant="soft",
            color_scheme="purple",
            size="3",
            border_radius="999px",
            cursor="pointer",
            box_shadow=SHADOW_GLOW,
            background_color=rx.cond(State.theme_mode == "dark", "rgba(24, 15, 46, 0.72)", "rgba(255, 250, 255, 0.9)"),
            color=rx.cond(State.theme_mode == "dark", "#e9d5ff", "#7c3aed"),
            border=f"1px solid {BORDER_COLOR}",
            _hover={"transform": "translateY(-1px)", "border_color": BORDER_COLOR_HOVER},
        ),
        position="fixed",
        top=rx.breakpoints(initial="1rem", sm="1.25rem"),
        right=rx.breakpoints(initial="1rem", sm="1.5rem"),
        z_index="100",
    )


def hero_section() -> rx.Component:
    """The clean intro banner with Days Together romantic counter."""
    return rx.vstack(
        rx.heading(
            "JHCWCH",
            size="9",
            style=styles["gradient_text"],
            align="center",
            text_align="center",
            width="100%",
            margin="0 auto",
            padding_top=rx.breakpoints(initial="3rem", sm="3.5rem"),
            padding_bottom="0.5rem",
        ),
        # Days Together Love Counter Badge
        rx.hstack(
            rx.icon("heart", size=15, color="#ec4899"),
            rx.text(
                rx.text.strong(State.days_together.to(str), color="#f472b6", font_weight="800"),
                " Days Together",
                font_size=rx.breakpoints(initial="0.82rem", sm="0.95rem"),
                font_weight="600",
                color=rx.cond(State.theme_mode == "dark", "#f1f5f9", "#334155"),
            ),
            padding="6px 18px",
            border_radius="999px",
            background=rx.cond(
                State.theme_mode == "dark",
                "rgba(244, 114, 182, 0.12)",
                "rgba(244, 114, 182, 0.18)"
            ),
            border="1px solid rgba(244, 114, 182, 0.3)",
            backdrop_filter="blur(10px)",
            box_shadow="0 4px 15px rgba(236, 72, 153, 0.15)",
            align="center",
            spacing="2",
            margin_bottom="1.5rem",
        ),
        align="center",
        width="100%",
    )


def stats_bar() -> rx.Component:
    """Counters and tabs for timeline, highlights, map, completed, and plans."""
    return rx.grid(
        # Trips
        rx.box(
            rx.vstack(
                rx.icon("plane", size=22, color=ACCENT_COLOR),
                rx.heading(State.total_past.to(str), size="5", font_family=FONT_HEADING),
                rx.text("Timeline", font_size="0.8rem", color=TEXT_MUTED, font_weight="600"),
                spacing="1",
                align="center",
            ),
            style=styles["stat_card"],
            _hover=styles["glass_card_hover"],
            border=rx.cond(State.active_tab == "timeline", f"1px solid {ACCENT_COLOR}", f"1px solid {BORDER_COLOR}"),
            box_shadow=rx.cond(State.active_tab == "timeline", f"0 0 16px rgba(168, 85, 247, 0.35)", "none"),
            cursor="pointer",
            on_click=lambda: State.set_tab("timeline"),
        ),
        # Highlights
        rx.box(
            rx.vstack(
                rx.icon("heart", size=22, color="#f43f5e"),
                rx.heading(State.total_highlights.to(str), size="5", font_family=FONT_HEADING),
                rx.text("Highlights", font_size="0.8rem", color=rx.cond(State.theme_mode == "light", "#be123c", "#fda4af"), font_weight="600"),
                spacing="1",
                align="center",
            ),
            style=styles["stat_card"],
            _hover=styles["glass_card_hover"],
            border=rx.cond(State.active_tab == "highlights", f"1px solid #f43f5e", f"1px solid {BORDER_COLOR}"),
            box_shadow=rx.cond(State.active_tab == "highlights", f"0 0 16px rgba(244, 63, 94, 0.35)", "none"),
            cursor="pointer",
            on_click=lambda: State.set_tab("highlights"),
        ),
        # Memory Map
        rx.box(
            rx.vstack(
                rx.icon("map-pin", size=22, color="#10b981"),
                rx.heading(State.total_past.to(str), size="5", font_family=FONT_HEADING),
                rx.text("Memory Map", font_size="0.8rem", color=rx.cond(State.theme_mode == "light", "#047857", "#6ee7b7"), font_weight="600"),
                spacing="1",
                align="center",
            ),
            style=styles["stat_card"],
            _hover=styles["glass_card_hover"],
            border=rx.cond(State.active_tab == "map", f"1px solid #10b981", f"1px solid {BORDER_COLOR}"),
            box_shadow=rx.cond(State.active_tab == "map", f"0 0 16px rgba(16, 185, 129, 0.35)", "none"),
            cursor="pointer",
            on_click=lambda: State.set_tab("map"),
        ),
        # Completed
        rx.box(
            rx.vstack(
                rx.icon("circle-check", size=22, color="#ec4899"),
                rx.heading(State.total_completed.to(str), size="5", font_family=FONT_HEADING),
                rx.text("Completed", font_size="0.8rem", color=rx.cond(State.theme_mode == "light", "#be185d", "#fbcfe8"), font_weight="600"),
                spacing="1",
                align="center",
            ),
            style=styles["stat_card"],
            _hover=styles["glass_card_hover"],
            border=rx.cond(State.active_tab == "completed", f"1px solid #ec4899", f"1px solid {BORDER_COLOR}"),
            box_shadow=rx.cond(State.active_tab == "completed", f"0 0 16px rgba(236, 72, 153, 0.35)", "none"),
            cursor="pointer",
            on_click=lambda: State.set_tab("completed"),
        ),
        # Plans
        rx.box(
            rx.vstack(
                rx.icon("clipboard-list", size=22, color="#38bdf8"),
                rx.heading(State.total_wishlist.to(str), size="5", font_family=FONT_HEADING),
                rx.text("Plans", font_size="0.8rem", color=rx.cond(State.theme_mode == "light", "#0369a1", "rgba(56, 189, 248, 0.8)"), font_weight="600"),
                spacing="1",
                align="center",
            ),
            style=styles["stat_card"],
            _hover=styles["glass_card_hover"],
            border=rx.cond(State.active_tab == "plans", f"1px solid #38bdf8", f"1px solid {BORDER_COLOR}"),
            box_shadow=rx.cond(State.active_tab == "plans", f"0 0 16px rgba(56, 189, 248, 0.35)", "none"),
            cursor="pointer",
            on_click=lambda: State.set_tab("plans"),
        ),
        columns=rx.breakpoints(initial="2", sm="3", md="5"),
        spacing="3",
        width="100%",
        max_width="1000px",
        margin="0 auto 1.5rem auto",
        padding_x="1rem",
    )


def timeline_card_content(item: rx.Var) -> rx.Component:
    """A single trip memory card."""
    return rx.box(
        rx.vstack(
            rx.box(
                rx.cond(
                    item["is_cover_video"],
                    rx.video(
                        src=rx.cond(
                            item["is_external"],
                            item["image_path"],
                            f"/{item['image_path']}",
                        ),
                        width="100%",
                        height="200px",
                        controls=False,
                        playing=True,
                        loop=True,
                        muted=True,
                        border_radius="14px 14px 0 0",
                        style={"pointer_events": "none"},
                        config={
                            "file": {
                                "attributes": {
                                    "playsInline": True,
                                    "muted": True,
                                    "autoPlay": True,
                                    "preload": "auto",
                                    "style": {"objectFit": "cover", "width": "100%", "height": "100%"},
                                }
                            }
                        },
                    ),
                    rx.image(
                        src=rx.cond(
                            item["is_external"],
                            item["image_path"],
                            f"/{item['image_path']}",
                        ),
                        width="100%",
                        height="200px",
                        object_fit="cover",
                        border_radius="14px 14px 0 0",
                    )
                ),
                # Media count badge
                rx.hstack(
                    rx.icon("image", size=12, color="#ffffff"),
                    rx.text(item["images"].to(list).length().to(str), font_size="0.75rem", font_weight="600", color="#ffffff"),
                    position="absolute",
                    bottom="8px",
                    right="8px",
                    background="rgba(15, 12, 30, 0.65)",
                    backdrop_filter="blur(8px)",
                    border="1px solid rgba(255, 255, 255, 0.15)",
                    border_radius="8px",
                    padding="3px 8px",
                    spacing="1",
                    align_items="center",
                    box_shadow="0 4px 10px rgba(0, 0, 0, 0.3)",
                ),
                width="100%",
                overflow="hidden",
                border_radius="14px 14px 0 0",
                position="relative",
            ),
            rx.vstack(
                rx.badge(
                    item["date"],
                    variant="solid",
                    color_scheme="purple",
                    border_radius="6px",
                    style=styles["badge_past"],
                ),
                rx.heading(
                    item["title"],
                    size="3",
                    font_family=FONT_HEADING,
                    color=TEXT_WHITE,
                    margin_top="1",
                    align="center",
                    text_align="center",
                    width="100%",
                ),
                align_items="center",
                text_align="center",
                padding="0.75rem 1rem",
                spacing="1",
            ),
            align_items="stretch",
            spacing="0",
        ),
        style=styles["glass_card"],
        _hover=styles["glass_card_hover"],
        width="100%",
        max_width="300px",
        height="300px",
        overflow="hidden",
        cursor="pointer",
        on_click=lambda: State.select_trip(item["id"]),
    )


def vertical_guide_line(is_top: bool) -> rx.Component:
    """A vertical glowing connection line between card and timeline dot."""
    grad = f"linear-gradient(to bottom, {ACCENT_COLOR}, rgba(168, 85, 247, 0.15))" if is_top else f"linear-gradient(to top, {ACCENT_COLOR}, rgba(168, 85, 247, 0.15))"
    return rx.box(
        width="2px",
        height="24px",
        background=grad,
        opacity=0.8,
        box_shadow=f"0 0 10px {ACCENT_COLOR}, 0 0 20px rgba(168, 85, 247, 0.4)",
    )


def timeline_card(item: rx.Var, index: rx.Var) -> rx.Component:
    """A single date memory card in the horizontal timeline."""
    is_even = index % 2 == 0
    card = timeline_card_content(item)

    return rx.vstack(
        # Top segment
        rx.cond(
            is_even,
            rx.vstack(
                card,
                vertical_guide_line(True),
                spacing="0",
                align_items="center",
                width="100%",
            ),
            rx.box(height="324px", width="100%")  # Matching spacer height (300 + 24)
        ),
        # Middle slot (horizontal line segment & center dot)
        rx.hstack(
            rx.box(height="2px", flex="1", bg=ACCENT_COLOR),
            rx.box(
                width="10px",
                height="10px",
                border_radius="50%",
                background_color=ACCENT_COLOR,
                box_shadow=SHADOW_GLOW,
                border="2px solid #ffffff",
                shrink=0,
            ),
            rx.box(height="2px", flex="1", bg=ACCENT_COLOR),
            width="100%",
            align_items="center",
            spacing="0",
        ),
        # Bottom segment
        rx.cond(
            is_even,
            rx.box(height="324px", width="100%"),  # Matching spacer height (300 + 24)
            rx.vstack(
                vertical_guide_line(False),
                card,
                spacing="0",
                align_items="center",
                width="100%",
            ),
        ),
        width=rx.breakpoints(initial="85vw", sm="340px", md="360px"),
        min_width=rx.breakpoints(initial="85vw", sm="340px", md="360px"),
        align_items="center",
        spacing="0",
        shrink=0,
        style={"scroll_snap_align": "center"},
    )


def timeline_view() -> rx.Component:
    """The horizontal trips timeline."""
    return rx.vstack(
        rx.heading(
            "Trips",
            size="5",
            font_family=FONT_HEADING,
            align="center",
            margin_bottom="1.5rem",
            color=TEXT_WHITE,
            width="100%",
        ),
        rx.cond(
            State.total_past > 0,
            rx.box(
                rx.hstack(
                    rx.foreach(
                        State.past_dates.to(list[dict]),
                        lambda item, index: timeline_card(item, index)
                    ),
                    spacing="0",
                    align_items="center",
                    min_width="max-content",
                    margin="0 auto",
                ),
                overflow_x="auto",
                width="100%",
                padding_y="1.5rem",
                style={
                    "scroll_snap_type": rx.breakpoints(initial="x mandatory", sm="none"),
                    "scroll_behavior": "smooth",
                    "padding_left": rx.breakpoints(initial="calc(50% - 42.5vw)", sm="2rem"),
                    "padding_right": rx.breakpoints(initial="calc(50% - 42.5vw)", sm="2rem"),
                    "&::-webkit-scrollbar": {"height": "6px"},
                    "&::-webkit-scrollbar-track": {
                        "background": "rgba(168, 85, 247, 0.05)",
                        "border_radius": "3px",
                    },
                    "&::-webkit-scrollbar-thumb": {
                        "background": "rgba(168, 85, 247, 0.2)",
                        "border_radius": "3px",
                    },
                    "&::-webkit-scrollbar-thumb:hover": {
                        "background": "rgba(168, 85, 247, 0.4)",
                    },
                },
            ),
            # Empty state
            rx.vstack(
                rx.icon("calendar-off", size=48, color=TEXT_MUTED),
                rx.text("No trips yet. Sync with Google Drive to see them!", color=TEXT_MUTED, align="center"),
                padding="3rem",
                style=styles["glass_card"],
                align="center",
                width="100%",
                max_width="450px",
            ),
        ),
        width="100%",
        align="center",
        padding_y="1rem",
    )


def bucket_item_card(item: rx.Var) -> rx.Component:
    """A card representing a future plan checklist item."""
    completed = item["completed"]
    return rx.box(
        rx.vstack(
            rx.hstack(
                # Category & Date Badges
                rx.hstack(
                    rx.badge(
                        item["category"],
                        variant="solid",
                        color_scheme=rx.cond(completed, "green", "purple"),
                        border_radius="6px",
                    ),
                    rx.cond(
                        item["date"] != "",
                        rx.badge(
                            item["date"],
                            variant="outline",
                            color_scheme="purple",
                            border_radius="6px",
                        ),
                    ),
                    spacing="2",
                ),
                rx.spacer(),
                # Checkmark Status
                rx.cond(
                    completed,
                    rx.hstack(
                        rx.icon("circle-check", size=14, color="#10b981"),
                        rx.text("Done", font_size="0.75rem", font_weight="700", color="#10b981"),
                        spacing="1",
                        align_items="center",
                    ),
                    rx.hstack(
                        rx.icon("sparkles", size=12, color=ACCENT_COLOR),
                        rx.text("Plan", font_size="0.75rem", font_weight="700", color=ACCENT_LIGHT),
                        spacing="1",
                        align_items="center",
                    )
                ),
                # Edit button
                rx.icon_button(
                    rx.icon("pencil", size=12),
                    variant="ghost",
                    color_scheme="purple",
                    size="1",
                    on_click=[State.open_edit_plan(item), rx.stop_propagation],
                    margin_left="1",
                    cursor="pointer",
                ),
                align_items="center",
                width="100%",
            ),
            # Title
            rx.heading(
                item["idea"],
                size="4",
                font_family=FONT_HEADING,
                color=rx.cond(completed, TEXT_MUTED, TEXT_WHITE),
                text_decoration=rx.cond(completed, "line-through", "none"),
                margin_top="2",
                align="center",
            ),
            # Notes
            rx.text(
                item["notes"],
                font_size="0.85rem",
                color=rx.cond(completed, TEXT_MUTED, TEXT_SOFT),
                margin_top="1",
                min_height="35px",
                align="center",
            ),
            align_items="center",
            padding="1.25rem",
        ),
        style=styles["glass_card"],
        _hover=styles["glass_card_hover"],
        opacity=rx.cond(completed, rx.cond(State.active_tab == "completed", 1.0, 0.78), 1.0),
        cursor=rx.cond(completed, "pointer", "default"),
        on_click=lambda: State.click_bucket_item(item),
    )


def completed_view() -> rx.Component:
    """The checklist of completed trips."""
    return rx.vstack(
        rx.heading(
            "Completed",
            size="5",
            font_family=FONT_HEADING,
            align="center",
            color=TEXT_WHITE,
            width="100%",
        ),
        
        # Category Filter Tabs
        rx.hstack(
            rx.foreach(
                State.bucket_categories.to(list[str]),
                lambda cat: rx.button(
                    cat,
                    on_click=lambda: State.set_filter(cat),
                    background_color=rx.cond(State.filter_category == cat, ACCENT_COLOR, "rgba(168, 85, 247, 0.08)"),
                    color=rx.cond(State.filter_category == cat, "#ffffff", ACCENT_LIGHT),
                    border=f"1px solid {BORDER_COLOR}",
                    border_radius="8px",
                    size="2",
                    _hover={"background_color": "rgba(168, 85, 247, 0.2)"},
                )
            ),
            spacing="2",
            flex_wrap="wrap",
            justify="center",
            margin_bottom="1.5rem",
        ),
        
        # Grid of Cards
        rx.cond(
            State.filtered_completed_list.length() > 0,
            rx.grid(
                rx.foreach(
                    State.filtered_completed_list.to(list[dict]),
                    lambda item: bucket_item_card(item)
                ),
                columns=rx.breakpoints(initial="1", sm="2", md="3"),
                spacing="3",
                width="100%",
            ),
            # Empty state
            rx.vstack(
                rx.icon("clipboard-x", size=48, color=TEXT_MUTED),
                rx.text("No completed trips in this category yet.", color=TEXT_MUTED, align="center"),
                padding="3rem",
                style=styles["glass_card"],
                align="center",
            ),
        ),
        width="100%",
        max_width="950px",
        margin="0 auto",
        padding="1rem",
        align="center",
    )


def plans_view() -> rx.Component:
    """The checklist of future plans."""
    return rx.vstack(
        rx.heading(
            "Plans",
            size="5",
            font_family=FONT_HEADING,
            align="center",
            color=TEXT_WHITE,
            width="100%",
        ),
        
        # Category Filter & Add Plan
        rx.hstack(
            rx.hstack(
                rx.foreach(
                    State.bucket_categories.to(list[str]),
                    lambda cat: rx.button(
                        cat,
                        on_click=lambda: State.set_filter(cat),
                        background_color=rx.cond(State.filter_category == cat, ACCENT_COLOR, "rgba(168, 85, 247, 0.08)"),
                        color=rx.cond(State.filter_category == cat, "#ffffff", ACCENT_LIGHT),
                        border=f"1px solid {BORDER_COLOR}",
                        border_radius="8px",
                        size="2",
                        _hover={"background_color": "rgba(168, 85, 247, 0.2)"},
                    )
                ),
                spacing="2",
                flex_wrap="wrap",
            ),
            rx.spacer(),
            rx.button(
                rx.hstack(rx.icon("plus", size=15), rx.text("Add Plan")),
                on_click=State.open_add_plan,
                color_scheme="purple",
                border_radius="8px",
                size="2",
            ),
            spacing="2",
            width="100%",
            align_items="center",
            margin_bottom="1.5rem",
        ),
        
        # Grid of Cards
        rx.cond(
            State.filtered_plans_list.length() > 0,
            rx.grid(
                rx.foreach(
                    State.filtered_plans_list.to(list[dict]),
                    lambda item: bucket_item_card(item)
                ),
                columns=rx.breakpoints(initial="1", sm="2", md="3"),
                spacing="3",
                width="100%",
            ),
            # Empty state
            rx.vstack(
                rx.icon("clipboard-x", size=48, color=TEXT_MUTED),
                rx.text("No plans in this category yet.", color=TEXT_MUTED, align="center"),
                padding="3rem",
                style=styles["glass_card"],
                align="center",
            ),
        ),
        width="100%",
        max_width="950px",
        margin="0 auto",
        padding="1rem",
        align="center",
    )


def footer() -> rx.Component:
    """The footer details with sync button."""
    return rx.box(
        rx.vstack(
            rx.divider(border_color="rgba(168, 85, 247, 0.08)"),
            rx.hstack(
                rx.text(
                    f"Last synced: {State.last_sync}",
                    font_size="0.75rem",
                    color="rgba(168, 85, 247, 0.45)",
                ),
                rx.button(
                    rx.cond(
                        State.is_syncing,
                        rx.hstack(rx.spinner(size="1"), rx.text("Syncing...", font_size="0.75rem")),
                        rx.hstack(rx.icon("refresh-cw", size=12), rx.text("Sync Cloud", font_size="0.75rem")),
                    ),
                    size="1",
                    variant="soft",
                    color_scheme="purple",
                    cursor="pointer",
                    on_click=State.sync_data,
                    disabled=State.is_syncing,
                ),
                justify="center",
                align="center",
                spacing="3",
                width="100%",
                padding_y="1.25rem",
            ),
            width="100%",
        ),
        margin_top="3rem",
        width="100%",
    )


def gallery_modal() -> rx.Component:
    """A beautiful responsive gallery overlay dialog for viewing trip pictures."""
    return rx.dialog.root(
        rx.dialog.content(
            # Dialog Header
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.badge(State.selected_trip_date, color_scheme="purple", border_radius="6px"),
                        rx.icon_button(
                            rx.icon("pencil", size=11),
                            size="1",
                            variant="ghost",
                            color_scheme="purple",
                            cursor="pointer",
                            opacity="0.8",
                            _hover={"opacity": "1", "transform": "scale(1.2)"},
                            on_click=lambda: State.open_edit_date(State.selected_trip_id),
                            title="Edit Date",
                        ),
                        align="center",
                        spacing="1",
                    ),
                    rx.dialog.title(State.selected_trip_title, size="5", font_family=FONT_HEADING, color=TEXT_WHITE),
                    spacing="1",
                    align_items="start",
                ),
                rx.dialog.close(
                    rx.button(
                        rx.icon("x", size=18),
                        variant="ghost",
                        color=ACCENT_LIGHT,
                        _hover={"background_color": "rgba(255, 255, 255, 0.1)"},
                    )
                ),
                justify="between",
                align_items="center",
                width="100%",
                border_bottom=f"1px solid {BORDER_COLOR}",
                padding_bottom="1rem",
                margin_bottom="1.5rem",
            ),
            
            # Description (Memory details)
            rx.cond(
                State.selected_trip_desc != "",
                rx.text(
                    State.selected_trip_desc,
                    font_size="0.95rem",
                    color=TEXT_SOFT,
                    margin_bottom="1.5rem",
                    line_height="1.6",
                ),
            ),
            
            # Scrollable Grid of Media (Images and Videos)
            rx.grid(
                rx.foreach(
                    State.selected_trip_images.to(list[dict]),
                    lambda img: rx.box(
                        rx.cond(
                            img["type"] == "video",
                            rx.box(
                                rx.video(
                                    src=rx.cond(
                                        img["is_external"],
                                        img["url"],
                                        f"/{img['url']}",
                                    ),
                                    width="100%",
                                    height="240px",
                                    object_fit="cover",
                                    controls=True,
                                    border_radius="12px",
                                ),
                                rx.hstack(
                                    rx.icon_button(
                                        rx.cond(
                                            State.favorites.contains(img["url"]),
                                            rx.icon("heart", size=13, color="#ec4899"),
                                            rx.icon("heart", size=13, color="#ffffff"),
                                        ),
                                        size="1",
                                        variant="ghost",
                                        cursor="pointer",
                                        background="rgba(15, 12, 30, 0.65)",
                                        backdrop_filter="blur(8px)",
                                        border="1px solid rgba(255, 255, 255, 0.2)",
                                        border_radius="999px",
                                        _hover={"transform": "scale(1.15)", "background": "rgba(236, 72, 153, 0.3)"},
                                        on_click=lambda: State.toggle_favorite(img["url"]),
                                    ),
                                    rx.button(
                                        rx.icon("maximize-2", size=13),
                                        size="1",
                                        color_scheme="purple",
                                        variant="solid",
                                        on_click=lambda: State.open_lightbox(img["url"], "video"),
                                        style={"cursor": "pointer"},
                                    ),
                                    position="absolute",
                                    top="8px",
                                    right="8px",
                                    spacing="1",
                                    z_index="10",
                                ),
                                # EXIF date overlay badge
                                rx.cond(
                                    img["date_taken"] != "",
                                    rx.hstack(
                                        rx.icon("calendar", size=10, color="#e9d5ff"),
                                        rx.text(img["date_taken"], font_size="0.65rem", font_weight="500", color="#e9d5ff"),
                                        position="absolute",
                                        bottom="8px",
                                        left="8px",
                                        background="rgba(15, 12, 30, 0.7)",
                                        backdrop_filter="blur(8px)",
                                        border="1px solid rgba(168, 85, 247, 0.25)",
                                        border_radius="6px",
                                        padding="2px 7px",
                                        spacing="1",
                                        align_items="center",
                                        z_index="10",
                                    ),
                                ),
                                position="relative",
                                overflow="hidden",
                                border_radius="12px",
                                border=f"1px solid {BORDER_COLOR_HOVER}",
                             ),
                             rx.box(
                                 rx.image(
                                     src=rx.cond(
                                         img["is_external"],
                                         img["thumb_url"],
                                         f"/{img['thumb_url']}",
                                     ),
                                     width="100%",
                                     height="240px",
                                     object_fit="cover",
                                     border_radius="12px",
                                     _hover={"transform": "scale(1.025)", "box_shadow": f"0 6px 20px rgba(168, 85, 247, 0.25)"},
                                     transition="transform 0.2s ease-out, box-shadow 0.2s ease-out",
                                     style={"will_change": "transform"},
                                     cursor="pointer",
                                     on_click=lambda: State.open_lightbox(img["url"], "image"),
                                 ),
                                 # Heart favorite toggle button
                                 rx.icon_button(
                                     rx.cond(
                                         State.favorites.contains(img["url"]),
                                         rx.icon("heart", size=13, color="#ec4899"),
                                         rx.icon("heart", size=13, color="#ffffff"),
                                     ),
                                     size="1",
                                     variant="ghost",
                                     cursor="pointer",
                                     position="absolute",
                                     top="8px",
                                     right="8px",
                                     background="rgba(15, 12, 30, 0.65)",
                                     backdrop_filter="blur(8px)",
                                     border="1px solid rgba(255, 255, 255, 0.2)",
                                     border_radius="999px",
                                     _hover={"transform": "scale(1.15)", "background": "rgba(236, 72, 153, 0.3)"},
                                     on_click=lambda: State.toggle_favorite(img["url"]),
                                     z_index="10",
                                 ),
                                 # EXIF date overlay badge
                                 rx.cond(
                                     img["date_taken"] != "",
                                     rx.hstack(
                                         rx.icon("calendar", size=10, color="#e9d5ff"),
                                         rx.text(img["date_taken"], font_size="0.65rem", font_weight="500", color="#e9d5ff"),
                                         position="absolute",
                                         bottom="8px",
                                         left="8px",
                                         background="rgba(15, 12, 30, 0.7)",
                                         backdrop_filter="blur(8px)",
                                         border="1px solid rgba(168, 85, 247, 0.25)",
                                         border_radius="6px",
                                         padding="2px 7px",
                                         spacing="1",
                                         align_items="center",
                                     ),
                                 ),
                                 position="relative",
                                 overflow="hidden",
                                 border_radius="12px",
                                 border=f"1px solid {BORDER_COLOR_HOVER}",
                             )
                         )
                     )
                 ),
                columns=rx.breakpoints(initial="1", sm="2", md="3"),
                spacing="4",
                width="100%",
            ),
            
            # Dialog styling
            background=BG_GRADIENT,
            border=f"1px solid {BORDER_COLOR_HOVER}",
            border_radius="24px",
            max_width="850px",
            max_height="80vh",
            overflow_y="auto",
            padding="2rem",
            box_shadow=f"{CARD_SHADOW}, {SHADOW_GLOW}",
            style={
                **get_theme_vars(State.theme_mode),
                "&::-webkit-scrollbar": {
                    "width": "6px",
                },
                "&::-webkit-scrollbar-track": {
                    "background": "transparent",
                },
                "&::-webkit-scrollbar-thumb": {
                    "background": "rgba(168, 85, 247, 0.2)",
                    "border_radius": "3px",
                },
            }
        ),
        open=State.selected_trip_id != "",
        on_open_change=lambda _: State.close_gallery(),
    )


def lightbox_modal() -> rx.Component:
    """A premium fullscreen media overlay lightbox for viewing images/videos in full size."""
    return rx.dialog.root(
        rx.dialog.content(
             # Close Button at Top Right
             rx.hstack(
                 rx.spacer(),
                 rx.dialog.close(
                     rx.button(
                         rx.icon("x", size=20),
                         variant="ghost",
                         color=ACCENT_LIGHT,
                         _hover={"background_color": "rgba(255, 255, 255, 0.1)"},
                     )
                 ),
                 width="100%",
                 margin_bottom="1rem",
             ),
            # Media Container
            rx.center(
                rx.cond(
                    State.lightbox_type == "video",
                    rx.video(
                        src=rx.cond(
                            State.lightbox_is_external,
                            State.lightbox_url,
                            f"/{State.lightbox_url}",
                        ),
                        controls=True,
                        autoplay=True,
                        width="100%",
                        max_height="70vh",
                        border_radius="8px",
                    ),
                    rx.image(
                        src=rx.cond(
                            State.lightbox_is_external,
                            State.lightbox_url,
                            f"/{State.lightbox_url}",
                        ),
                        width="100%",
                        max_height="70vh",
                        object_fit="contain",
                        border_radius="8px",
                    )
                ),
                width="100%",
            ),
            background=BG_GRADIENT,
            border=f"1px solid {BORDER_COLOR_HOVER}",
            border_radius="20px",
            max_width="1000px",
            padding="1.5rem",
            box_shadow=f"0 12px 48px rgba(0, 0, 0, 0.8), {SHADOW_GLOW}",
            style=get_theme_vars(State.theme_mode),
        ),
        open=State.lightbox_url != "",
        on_open_change=lambda _: State.close_lightbox(),
    )


def plan_modal() -> rx.Component:
    """A beautiful modal to add or edit plans."""
    return rx.dialog.root(
        rx.dialog.content(
            # Dialog Header
            rx.hstack(
                rx.dialog.title(
                    rx.cond(State.plan_is_editing, "Edit Plan", "Add New Plan"),
                    size="5",
                    font_family=FONT_HEADING,
                    color=TEXT_WHITE,
                ),
                rx.dialog.close(
                    rx.button(
                        rx.icon("x", size=18),
                        variant="ghost",
                        color=ACCENT_LIGHT,
                        on_click=State.close_plan_dialog,
                        _hover={"background_color": "rgba(255, 255, 255, 0.1)"},
                    )
                ),
                justify="between",
                align_items="center",
                width="100%",
                border_bottom=f"1px solid {BORDER_COLOR}",
                padding_bottom="1rem",
                margin_bottom="1.5rem",
            ),
            
            # Dialog Body
            rx.vstack(
                rx.vstack(
                    rx.text("What's the plan?", font_size="0.85rem", color=TEXT_MUTED, font_weight="600"),
                    rx.input(
                        placeholder="e.g. Couples Cooking Class",
                        value=State.form_plan_idea,
                        on_change=State.set_form_plan_idea,
                        width="100%",
                        background_color="var(--input-bg)",
                        border=f"1px solid {BORDER_COLOR}",
                        color=TEXT_WHITE,
                        border_radius="8px",
                    ),
                    align_items="start",
                    width="100%",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Category", font_size="0.85rem", color=TEXT_MUTED, font_weight="600"),
                    rx.input(
                        placeholder="e.g. Adventure, Food, Chill",
                        value=State.form_plan_category,
                        on_change=State.set_form_plan_category,
                        width="100%",
                        background_color="var(--input-bg)",
                        border=f"1px solid {BORDER_COLOR}",
                        color=TEXT_WHITE,
                        border_radius="8px",
                    ),
                    align_items="start",
                    width="100%",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Target Date (Optional)", font_size="0.85rem", color=TEXT_MUTED, font_weight="600"),
                    rx.input(
                        type="date",
                        value=State.form_plan_date,
                        on_change=State.set_form_plan_date,
                        width="100%",
                        background_color="var(--input-bg)",
                        border=f"1px solid {BORDER_COLOR}",
                        color=TEXT_WHITE,
                        border_radius="8px",
                        style={"color-scheme": rx.cond(State.theme_mode == "dark", "dark", "light")},
                    ),
                    align_items="start",
                    width="100%",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Notes / Description", font_size="0.85rem", color=TEXT_MUTED, font_weight="600"),
                    rx.text_area(
                        placeholder="Add some details about this plan...",
                        value=State.form_plan_notes,
                        on_change=State.set_form_plan_notes,
                        width="100%",
                        height="100px",
                        background_color="var(--input-bg)",
                        border=f"1px solid {BORDER_COLOR}",
                        color=TEXT_WHITE,
                        border_radius="8px",
                    ),
                    align_items="start",
                    width="100%",
                    spacing="1",
                ),
                rx.hstack(
                    rx.checkbox(
                        checked=State.form_plan_completed,
                        on_change=State.set_form_plan_completed,
                        color_scheme="purple",
                    ),
                    rx.text("Mark as completed", font_size="0.9rem", color=TEXT_WHITE),
                    spacing="2",
                    align_items="center",
                    padding_y="2",
                ),
                rx.hstack(
                    rx.cond(
                        State.plan_is_editing,
                        rx.button(
                            rx.hstack(rx.icon("trash-2", size=15), rx.text("Delete")),
                            color_scheme="red",
                            variant="soft",
                            on_click=State.delete_plan,
                            border_radius="8px",
                            size="2",
                        ),
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="ghost",
                            color="#8e9196",
                            on_click=State.close_plan_dialog,
                            border_radius="8px",
                            size="2",
                        )
                    ),
                    rx.button(
                        rx.hstack(rx.icon("check", size=15), rx.text("Save")),
                        color_scheme="purple",
                        on_click=State.save_plan,
                        border_radius="8px",
                        size="2",
                    ),
                    width="100%",
                    spacing="3",
                    padding_top="1rem",
                ),
                width="100%",
                spacing="4",
            ),
            background=BG_GRADIENT,
            backdrop_filter="blur(25px)",
            border=f"1px solid {BORDER_COLOR_HOVER}",
            border_radius="24px",
            max_width="450px",
            padding="2rem",
            box_shadow=f"{CARD_SHADOW}, {SHADOW_GLOW}",
            style=get_theme_vars(State.theme_mode),
        ),
        open=State.plan_dialog_open,
        on_open_change=State.toggle_plan_dialog,
    )


def countdown_banner() -> rx.Component:
    """A beautiful, glowing countdown banner for the next trip."""
    details = State.next_adventure_details
    return rx.cond(
        details["has_adventure"],
        rx.box(
            rx.hstack(
                rx.icon("sparkles", size=18, color="#a855f7"),
                rx.vstack(
                    rx.text(
                        rx.text.span("Next Trip: ", font_weight="400", color=TEXT_SOFT),
                        rx.text.span(details["title"], font_weight="600", color=TEXT_WHITE),
                        font_size="0.95rem",
                    ),
                    rx.text(
                        rx.text.span(details["days_left"].to(str), font_weight="800", color=ACCENT_COLOR, font_size="1.1rem"),
                        rx.text.span(" days left! ", font_weight="600", color=ACCENT_LIGHT),
                        rx.text.span(f"({details['date']})", font_size="0.8rem", color=TEXT_MUTED),
                        font_size="0.9rem",
                    ),
                    spacing="0",
                    align_items="center",
                ),
                rx.icon("calendar", size=18, color="#a855f7"),
                spacing="4",
                align_items="center",
                justify="center",
                width="100%",
            ),
            style={
                **styles["glass_card"],
                "padding": "1rem 2rem",
                "margin": "0 auto 1.5rem auto",
                "max_width": "600px",
                "text_align": "center",
                "box_shadow": f"{CARD_SHADOW}, {SHADOW_GLOW}",
                "border_color": BORDER_COLOR_HOVER,
            },
        ),
        # Fallback empty space
        rx.fragment()
    )


def edit_date_modal() -> rx.Component:
    """Modal for editing trip date."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.hstack(
                rx.dialog.title(
                    rx.hstack(
                        rx.icon("calendar", size=20, color=ACCENT_COLOR),
                        rx.text("Edit Memory Date", font_family=FONT_HEADING, font_weight="700"),
                        align="center",
                        spacing="2",
                    ),
                    color=TEXT_WHITE,
                    size="5",
                ),
                rx.dialog.close(
                    rx.button(
                        rx.icon("x", size=18),
                        variant="ghost",
                        color=ACCENT_LIGHT,
                        on_click=State.close_edit_date,
                        _hover={"background_color": "rgba(255, 255, 255, 0.1)"},
                    )
                ),
                justify="between",
                align_items="center",
                width="100%",
                border_bottom=f"1px solid {BORDER_COLOR}",
                padding_bottom="0.75rem",
                margin_bottom="1.25rem",
            ),
            rx.vstack(
                rx.text(
                    rx.text.span("Trip: ", font_weight="600", color=TEXT_SOFT),
                    rx.text.span(State.edit_date_trip_title, font_weight="700", color=TEXT_WHITE),
                    font_size="0.95rem",
                    margin_bottom="0.5rem",
                ),
                rx.text("Date (YYYY-MM-DD)", font_size="0.85rem", color=TEXT_MUTED, font_weight="600"),
                rx.input(
                    type="date",
                    value=State.edit_date_value,
                    on_change=State.set_edit_date_value,
                    width="100%",
                    background_color="var(--input-bg)",
                    border=f"1px solid {BORDER_COLOR}",
                    color=TEXT_WHITE,
                    border_radius="8px",
                    padding="0.5rem",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="ghost",
                            color="#8e9196",
                            on_click=State.close_edit_date,
                            border_radius="8px",
                            size="2",
                        )
                    ),
                    rx.button(
                        rx.hstack(rx.icon("check", size=15), rx.text("Save Date")),
                        color_scheme="purple",
                        background=ACCENT_COLOR,
                        on_click=State.save_trip_date,
                        border_radius="8px",
                        size="2",
                        cursor="pointer",
                    ),
                    justify="end",
                    width="100%",
                    spacing="3",
                    padding_top="1rem",
                ),
                spacing="3",
                width="100%",
            ),
            background=BG_GRADIENT,
            backdrop_filter="blur(25px)",
            border=f"1px solid {BORDER_COLOR_HOVER}",
            border_radius="22px",
            max_width="420px",
            padding="1.75rem",
            box_shadow=f"{CARD_SHADOW}, {SHADOW_GLOW}",
            style=get_theme_vars(State.theme_mode),
        ),
        open=State.edit_date_dialog_open,
        on_open_change=State.close_edit_date,
    )


def highlights_view() -> rx.Component:
    """Collage view of all favorited/hearted pictures and videos."""
    return rx.vstack(
        rx.vstack(
            rx.heading("Highlights & Favorites", size="7", font_family=FONT_HEADING, color=TEXT_WHITE),
            rx.text("A collection of our favorite moments and cherished memories together ✨", color=TEXT_MUTED, font_size="0.95rem"),
            align="center",
            spacing="1",
            margin_bottom="2rem",
            text_align="center",
        ),
        rx.cond(
            State.total_highlights > 0,
            rx.grid(
                rx.foreach(
                    State.highlight_images.to(list[dict]),
                    lambda item: rx.box(
                        rx.vstack(
                            rx.box(
                                rx.cond(
                                    item["type"] == "video",
                                    rx.video(
                                        src=rx.cond(
                                            item["is_external"],
                                            item["url"],
                                            f"/{item['url']}",
                                        ),
                                        width="100%",
                                        height="240px",
                                        controls=False,
                                        playing=True,
                                        loop=True,
                                        muted=True,
                                        border_radius="14px 14px 0 0",
                                        style={"pointer_events": "none"},
                                        config={"file": {"attributes": {"playsInline": True, "muted": True, "autoPlay": True, "style": {"objectFit": "cover", "width": "100%", "height": "100%"}}}}
                                    ),
                                    rx.image(
                                        src=rx.cond(
                                            item["is_external"],
                                            item["thumb_url"],
                                            f"/{item['thumb_url']}",
                                        ),
                                        width="100%",
                                        height="240px",
                                        object_fit="cover",
                                        border_radius="14px 14px 0 0",
                                    )
                                ),
                                # Heart un-favorite button
                                rx.icon_button(
                                    rx.icon("heart", size=14, color="#ec4899"),
                                    variant="ghost",
                                    size="1",
                                    cursor="pointer",
                                    position="absolute",
                                    top="10px",
                                    right="10px",
                                    background="rgba(15, 12, 30, 0.75)",
                                    backdrop_filter="blur(8px)",
                                    border="1px solid rgba(236, 72, 153, 0.4)",
                                    border_radius="999px",
                                    _hover={"transform": "scale(1.15)"},
                                    on_click=lambda: State.toggle_favorite(item["url"]),
                                ),
                                position="relative",
                                width="100%",
                                overflow="hidden",
                            ),
                            # Polaroid description
                            rx.vstack(
                                rx.text(item["trip_title"], font_weight="700", font_size="0.9rem", color=TEXT_WHITE, line_clamp=1),
                                rx.hstack(
                                    rx.badge(item["trip_date"], variant="soft", color_scheme="purple", font_size="0.7rem"),
                                    rx.cond(
                                        item["date_taken"] != "",
                                        rx.text(item["date_taken"], font_size="0.7rem", color=TEXT_MUTED),
                                    ),
                                    spacing="2",
                                    align="center",
                                ),
                                padding="12px",
                                width="100%",
                                spacing="1",
                                align="start",
                            ),
                            spacing="0",
                            width="100%",
                        ),
                        cursor="pointer",
                        on_click=lambda: State.open_lightbox(item["url"], item["type"]),
                        background=rx.cond(State.theme_mode == "dark", "rgba(22, 16, 43, 0.75)", "rgba(255, 255, 255, 0.9)"),
                        border=f"1px solid {BORDER_COLOR}",
                        border_radius="16px",
                        overflow="hidden",
                        box_shadow=CARD_SHADOW,
                        _hover={"transform": "translateY(-4px) scale(1.01)", "border_color": "#ec4899", "box_shadow": "0 12px 30px rgba(236, 72, 153, 0.2)"},
                        transition="all 0.25s cubic-bezier(0.16, 1, 0.3, 1)",
                    )
                ),
                columns=rx.breakpoints(initial="1", sm="2", md="3"),
                spacing="4",
                width="100%",
                max_width="1000px",
                margin="0 auto",
            ),
            # Empty state
            rx.center(
                rx.vstack(
                    rx.icon("heart", size=48, color="rgba(236, 72, 153, 0.4)"),
                    rx.heading("No Highlights Yet", size="4", color=TEXT_WHITE),
                    rx.text("Click the heart ❤️ icon on any photo in the gallery to add it to your highlights wall!", color=TEXT_MUTED, text_align="center", max_width="400px"),
                    spacing="2",
                    align="center",
                    padding="3rem 1rem",
                ),
                width="100%",
            )
        ),
        width="100%",
        align="center",
        padding_y="1rem",
    )


def memory_map_view() -> rx.Component:
    """Interactive Map view showing all trip memory locations with pins."""
    map_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
      <style>
        body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; background: #120b24; overflow: hidden; }}
        #map {{ width: 100%; height: 100%; }}
        .leaflet-popup-content-wrapper {{
          background: rgba(22, 16, 43, 0.95);
          color: #f1f5f9;
          border-radius: 14px;
          border: 1px solid rgba(168, 85, 247, 0.4);
          backdrop-filter: blur(10px);
          box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        }}
        .leaflet-popup-tip {{
          background: rgba(22, 16, 43, 0.95);
        }}
      </style>
    </head>
    <body>
      <div id="map"></div>
      <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
      <script>
        var map = L.map('map', {{
          center: [-6.2088, 106.8456],
          zoom: 11,
          zoomControl: true
        }});

        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
          attribution: '&copy; OpenStreetMap &copy; CARTO',
          maxZoom: 19
        }}).addTo(map);

        var locations = {State.map_locations_json};
        var bounds = [];

        var customIcon = L.divIcon({{
          className: 'custom-pin',
          html: '<div style="background:linear-gradient(135deg, #ec4899, #a855f7); color:white; width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 0 14px rgba(236,72,153,0.8), 0 4px 10px rgba(0,0,0,0.5); border:2px solid #ffffff; font-size:15px; cursor:pointer;">💖</div>',
          iconSize: [34, 34],
          iconAnchor: [17, 34],
          popupAnchor: [0, -32]
        }});

        if (locations && locations.length > 0) {{
          locations.forEach(function(loc) {{
            if (loc.lat && loc.lng) {{
              bounds.push([loc.lat, loc.lng]);
              var imgHtml = loc.image ? '<img src="/_upload/' + loc.image.replace(/^\\//, '') + '" onerror="this.src=\\'' + loc.image + '\\'" style="width:100%; height:95px; object-fit:cover; border-radius:8px; margin-bottom:6px; box-shadow:0 2px 8px rgba(0,0,0,0.4);" />' : '';
              var popupContent = '<div style="font-family:system-ui,-apple-system,sans-serif; text-align:center; padding:4px; min-width:170px;">' +
                imgHtml +
                '<strong style="font-size:13px; color:#ffffff; display:block; margin-bottom:2px;">' + loc.title + '</strong>' +
                '<span style="font-size:11px; color:#c084fc; font-weight:600; background:rgba(168,85,247,0.2); border:1px solid rgba(168,85,247,0.3); padding:2px 8px; border-radius:999px; display:inline-block; margin-bottom:4px;">' + loc.date + '</span>' +
                '<div style="font-size:11px; color:#94a3b8;">' + loc.count + ' photos & videos</div>' +
              '</div>';
              
              L.marker([loc.lat, loc.lng], {{ icon: customIcon }})
                .addTo(map)
                .bindPopup(popupContent, {{ maxWidth: 240 }});
            }}
          }});

          if (bounds.length > 0) {{
            map.fitBounds(bounds, {{ padding: [40, 40], maxZoom: 14 }});
          }}
        }}
      </script>
    </body>
    </html>
    """
    return rx.vstack(
        rx.vstack(
            rx.heading("Interactive Memory Map", size="7", font_family=FONT_HEADING, color=TEXT_WHITE),
            rx.text("Explore the special places from our adventures together 🗺️✨", color=TEXT_MUTED, font_size="0.95rem"),
            align="center",
            spacing="1",
            margin_bottom="1.5rem",
            text_align="center",
        ),
        rx.box(
            rx.html(
                f'<iframe srcdoc="{map_code.replace("\"", "&quot;")}" style="width:100%; height:550px; border:1px solid rgba(168, 85, 247, 0.3); border-radius:20px; box-shadow:0 15px 45px rgba(0,0,0,0.5);"></iframe>'
            ),
            width="100%",
            max_width="1000px",
            margin="0 auto",
        ),
        width="100%",
        align="center",
        padding_y="1rem",
    )
