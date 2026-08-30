import reflex as rx

# Theme values are set as CSS variables on the page root.
BG_GRADIENT = "var(--bg-main)"
ACCENT_COLOR = "var(--accent)"
ACCENT_DARK = "var(--accent-dark)"
ACCENT_LIGHT = "var(--accent-light)"
TEXT_MUTED = "var(--text-muted)"
TEXT_WHITE = "var(--text-main)"
TEXT_SOFT = "var(--text-soft)"
BG_GLASS = "var(--glass-bg)"
BORDER_COLOR = "var(--border)"
BORDER_COLOR_HOVER = "var(--border-hover)"

# Shadow styling
CARD_SHADOW = "var(--card-shadow)"
SHADOW_GLOW = "var(--shadow-glow)"

# Fonts
FONT_HEADING = "Outfit, sans-serif"
FONT_BODY = "Inter, sans-serif"

# Reusable Styles
styles = {
    "bg_main": {
        "background": BG_GRADIENT,
        "color": TEXT_WHITE,
        "font_family": FONT_BODY,
        "min_height": "100vh",
        "padding": "0",
        "margin": "0",
        "transition": "background 0.25s ease, color 0.25s ease",
    },
    
    "glass_card": {
        "background_color": BG_GLASS,
        "backdrop_filter": "blur(16px)",
        "-webkit-backdrop-filter": "blur(16px)",
        "border": f"1px solid {BORDER_COLOR}",
        "border_radius": "18px",
        "box_shadow": CARD_SHADOW,
        "transition": "all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1)",
    },
    
    "glass_card_hover": {
        "transform": "translateY(-4px)",
        "border_color": BORDER_COLOR_HOVER,
        "box_shadow": f"{CARD_SHADOW}, {SHADOW_GLOW}",
    },

    "stat_card": {
        "background": "var(--stat-bg)",
        "backdrop_filter": "blur(12px)",
        "-webkit-backdrop-filter": "blur(12px)",
        "border": f"1px solid {BORDER_COLOR}",
        "border_radius": "16px",
        "padding": "1.5rem",
        "text_align": "center",
        "flex": "1",
        "transition": "all 0.2s ease-in-out",
    },
    
    "nav_bar": {
        "position": "sticky",
        "top": "0",
        "z_index": "100",
        "width": "100%",
        "background_color": "var(--nav-bg)",
        "backdrop_filter": "blur(12px)",
        "-webkit-backdrop-filter": "blur(12px)",
        "border_bottom": f"1px solid {BORDER_COLOR}",
        "padding_y": "1rem",
        "padding_x": "2rem",
    },
    
    "gradient_text": {
        "background": "var(--title-gradient)",
        "background_clip": "text",
        "-webkit-background-clip": "text",
        "text_fill_color": "transparent",
        "-webkit-text-fill-color": "transparent",
        "font_family": FONT_HEADING,
    },
    
    "accent_button": {
        "background": f"linear-gradient(135deg, {ACCENT_COLOR} 0%, {ACCENT_DARK} 100%)",
        "color": TEXT_WHITE,
        "border_radius": "12px",
        "padding": "0.75rem 1.5rem",
        "font_weight": "600",
        "box_shadow": "0 4px 14px 0 rgba(124, 58, 237, 0.4)",
        "_hover": {
            "transform": "scale(1.02)",
            "box_shadow": f"0 6px 20px 0 rgba(124, 58, 237, 0.6), {SHADOW_GLOW}",
        },
        "transition": "all 0.2s ease-in-out",
    },

    "secondary_button": {
        "background_color": "rgba(168, 85, 247, 0.1)",
        "border": f"1px solid {BORDER_COLOR}",
        "color": ACCENT_LIGHT,
        "border_radius": "12px",
        "padding": "0.75rem 1.5rem",
        "font_weight": "600",
        "_hover": {
            "background_color": "rgba(168, 85, 247, 0.2)",
            "border_color": BORDER_COLOR_HOVER,
        },
        "transition": "all 0.2s ease-in-out",
    },
    
    "badge_past": {
        "background_color": "var(--badge-bg)",
        "color": ACCENT_LIGHT,
        "border": "1px solid var(--badge-border)",
        "padding_x": "0.5rem",
        "padding_y": "0.15rem",
        "border_radius": "6px",
        "font_size": "0.75rem",
        "font_weight": "600",
    },
    
    "badge_bucket": {
        "background_color": "rgba(236, 72, 153, 0.15)",
        "color": "#fbcfe8",
        "border": "1px solid rgba(236, 72, 153, 0.3)",
        "padding_x": "0.5rem",
        "padding_y": "0.15rem",
        "border_radius": "6px",
        "font_size": "0.75rem",
        "font_weight": "600",
    }
}


def get_theme_vars(theme_mode: rx.Var) -> dict:
    """CSS variables for dark and light themes."""
    is_light = theme_mode == "light"
    return {
        "--bg-main": rx.cond(
            is_light,
            "linear-gradient(180deg, #fffaff 0%, #f7f1ff 48%, #ffffff 100%)",
            "linear-gradient(180deg, #090514 0%, #120924 50%, #07030e 100%)",
        ),
        "--accent": rx.cond(is_light, "#b88cff", "#a855f7"),
        "--accent-dark": rx.cond(is_light, "#8b5cf6", "#7c3aed"),
        "--accent-light": rx.cond(is_light, "#6d28d9", "#e9d5ff"),
        "--text-main": rx.cond(is_light, "#211335", "#ffffff"),
        "--text-soft": rx.cond(is_light, "#5b4a72", "#d1d5db"),
        "--text-muted": rx.cond(is_light, "#574075", "#a78bfa"),
        "--glass-bg": rx.cond(is_light, "rgba(255, 255, 255, 0.72)", "rgba(24, 15, 46, 0.5)"),
        "--nav-bg": rx.cond(is_light, "rgba(255, 250, 255, 0.82)", "rgba(9, 5, 20, 0.75)"),
        "--border": rx.cond(is_light, "rgba(184, 140, 255, 0.28)", "rgba(168, 85, 247, 0.15)"),
        "--border-hover": rx.cond(is_light, "rgba(139, 92, 246, 0.48)", "rgba(168, 85, 247, 0.4)"),
        "--stat-bg": rx.cond(
            is_light,
            "linear-gradient(135deg, rgba(184, 140, 255, 0.18) 0%, rgba(255, 255, 255, 0.58) 100%)",
            "linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(124, 58, 237, 0.05) 100%)",
        ),
        "--title-gradient": rx.cond(
            is_light,
            "linear-gradient(135deg, #7c3aed 0%, #b88cff 48%, #d8b4fe 100%)",
            "linear-gradient(135deg, #ffffff 0%, #e9d5ff 50%, #a855f7 100%)",
        ),
        "--badge-bg": rx.cond(is_light, "rgba(184, 140, 255, 0.16)", "rgba(168, 85, 247, 0.15)"),
        "--badge-border": rx.cond(is_light, "rgba(139, 92, 246, 0.34)", "rgba(168, 85, 247, 0.3)"),
        "--card-shadow": rx.cond(is_light, "0 10px 30px rgba(91, 74, 114, 0.14)", "0 8px 32px 0 rgba(0, 0, 0, 0.37)"),
        "--shadow-glow": rx.cond(is_light, "0 0 22px rgba(184, 140, 255, 0.28)", "0 0 20px rgba(168, 85, 247, 0.25)"),
        "--modal-bg": rx.cond(is_light, "#f7f1ff", "#120924"),
        "--lightbox-bg": rx.cond(is_light, "#ffffff", "#07030e"),
        "--input-bg": rx.cond(is_light, "rgba(255, 255, 255, 0.78)", "rgba(255, 255, 255, 0.03)"),
    }

