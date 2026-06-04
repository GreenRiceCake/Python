import random
import tkinter as tk
from tkinter import messagebox, ttk


SUITS = ("♠", "♦", "♥", "♣")
RANKS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
RED_SUITS = ("♦", "♥")

BG_COLOR = "#f4f7fb"
PANEL_COLOR = "#ffffff"
LINE_COLOR = "#d8dee9"
TEXT_COLOR = "#1f2933"
MUTED_COLOR = "#687385"
ACCENT_COLOR = "#256d85"
ACCENT_DARK = "#174b5f"
SUCCESS_COLOR = "#2f855a"
WARNING_COLOR = "#b7791f"
RED_CARD_COLOR = "#c9363f"
BLACK_CARD_COLOR = "#1f2933"

deck = []
target_card = None
current_card = None
draw_count = 0

mode_var = None
mode_title = None
card_canvas = None
status_label = None
draw_button = None
remaining_label = None
count_label = None
target_label = None
history_list = None


def make_card(suit, rank):
    return f"{suit} {rank}"


def split_card(card):
    suit, rank = card.split()
    return suit, rank


def card_color(card):
    suit, rank = split_card(card)
    if suit in RED_SUITS:
        return RED_CARD_COLOR
    return BLACK_CARD_COLOR


def shuffle_deck():
    new_deck = []
    for suit in SUITS:
        for rank in RANKS:
            new_deck.append(make_card(suit, rank))
    random.shuffle(new_deck)
    return new_deck


def make_label(parent, text, size=11, bold=False, color=TEXT_COLOR, bg=PANEL_COLOR):
    if bold:
        font = ("Malgun Gothic", size, "bold")
    else:
        font = ("Malgun Gothic", size)

    return tk.Label(parent, text=text, font=font, fg=color, bg=bg)


def configure_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background=BG_COLOR)
    style.configure("Panel.TFrame", background=PANEL_COLOR)
    style.configure("TRadiobutton", background=BG_COLOR, font=("Malgun Gothic", 11))
    style.configure("TButton", font=("Malgun Gothic", 11), padding=(14, 8))
    style.configure(
        "Accent.TButton",
        font=("Malgun Gothic", 12, "bold"),
        padding=(18, 10),
        background=ACCENT_COLOR,
        foreground="#ffffff",
    )
    style.map("TButton", background=[("active", "#e8eef5")])
    style.map("Accent.TButton", background=[("active", ACCENT_DARK), ("disabled", "#9aa4b2")])


def build_layout(root):
    global mode_title
    global card_canvas
    global status_label
    global draw_button
    global remaining_label
    global count_label
    global target_label
    global history_list

    root.configure(bg=BG_COLOR)

    main = ttk.Frame(root, padding=20)
    main.pack(fill="both", expand=True)
    main.columnconfigure(0, weight=3, minsize=460)
    main.columnconfigure(1, weight=2, minsize=280)
    main.rowconfigure(1, weight=1)

    header = ttk.Frame(main)
    header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 14))
    header.columnconfigure(0, weight=1)
    make_label(header, "카드 뽑기 게임", 24, True, bg=BG_COLOR).grid(row=0, column=0, sticky="w")

    mode_bar = ttk.Frame(header)
    mode_bar.grid(row=0, column=1, sticky="e")

    modes = (("기본", "basic"), ("목표", "target"))
    for text, value in modes:
        ttk.Radiobutton(mode_bar, text=text, value=value, variable=mode_var, command=reset_game).pack(
            side="left",
            padx=(0, 8),
        )
    ttk.Button(mode_bar, text="도움말", command=show_help).pack(side="left")

    play = ttk.Frame(main, style="Panel.TFrame", padding=20)
    play.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
    play.columnconfigure(0, weight=1)
    play.rowconfigure(1, weight=1)

    mode_title = make_label(play, "", 16, True)
    mode_title.grid(row=0, column=0, sticky="w")

    card_canvas = tk.Canvas(play, width=280, height=380, bg=PANEL_COLOR, highlightthickness=0)
    card_canvas.grid(row=1, column=0, pady=14)

    status_label = make_label(play, "", 12, color=MUTED_COLOR)
    status_label.config(wraplength=460, justify="left")
    status_label.grid(row=2, column=0, sticky="ew", pady=(0, 14))

    controls = ttk.Frame(play, style="Panel.TFrame")
    controls.grid(row=3, column=0, sticky="ew")
    for col in range(3):
        controls.columnconfigure(col, weight=1)

    buttons = (
        ("카드 뽑기", draw_card, "Accent.TButton"),
        ("새 게임", reset_game, "TButton"),
        ("종료", root.destroy, "TButton"),
    )
    for col, button_info in enumerate(buttons):
        text, command, style = button_info
        button = ttk.Button(controls, text=text, command=command, style=style)
        button.grid(row=0, column=col, sticky="ew", padx=(0, 8) if col < 2 else 0)
        if text == "카드 뽑기":
            draw_button = button

    side = ttk.Frame(main, style="Panel.TFrame", padding=18)
    side.grid(row=1, column=1, sticky="nsew")
    side.columnconfigure(0, weight=1)
    side.rowconfigure(7, weight=1)

    remaining_label = make_stat(side, "남은 카드", 0)
    count_label = make_stat(side, "뽑은 횟수", 2)
    target_label = make_stat(side, "목표 카드", 4)

    make_label(side, "뽑은 기록", 12, True).grid(row=6, column=0, sticky="w", pady=(16, 6))
    history_list = tk.Listbox(
        side,
        height=8,
        font=("Malgun Gothic", 11),
        borderwidth=1,
        relief="solid",
        highlightthickness=0,
        activestyle="none",
    )
    history_list.grid(row=7, column=0, sticky="nsew")


def make_stat(parent, title, row):
    make_label(parent, title, 10, color=MUTED_COLOR).grid(row=row, column=0, sticky="w")

    value_label = make_label(parent, "-", 15, True)
    value_label.grid(row=row + 1, column=0, sticky="w", pady=(0, 10))
    return value_label


def reset_game():
    global deck
    global target_card
    global current_card
    global draw_count

    deck = shuffle_deck()
    current_card = None
    draw_count = 0

    if mode_var.get() == "target":
        target_card = random.choice(deck)
    else:
        target_card = None

    draw_button.state(["!disabled"])
    history_list.delete(0, tk.END)
    update_view()


def draw_card():
    global current_card
    global draw_count

    if len(deck) == 0:
        status_label.config(text="카드를 모두 뽑았습니다.", fg=WARNING_COLOR)
        draw_button.state(["disabled"])
        return

    current_card = deck.pop()
    draw_count += 1
    history_list.insert(0, f"{draw_count}. {current_card}")

    if mode_var.get() == "target" and current_card == target_card:
        status_label.config(
            text=f"성공! {current_card} 카드를 {draw_count}번 만에 뽑았습니다.",
            fg=SUCCESS_COLOR,
        )
        draw_button.state(["disabled"])
    elif len(deck) == 0:
        status_label.config(text="마지막 카드까지 뽑았습니다.", fg=WARNING_COLOR)
        draw_button.state(["disabled"])
    else:
        status_label.config(text=f"{current_card} 카드를 뽑았습니다.", fg=MUTED_COLOR)

    update_view()


def update_view():
    if mode_var.get() == "target":
        mode_title.config(text="특정 카드 뽑기")
        target_text = target_card
        opening_text = "목표 카드를 찾아보세요."
    else:
        mode_title.config(text="기본 카드 뽑기")
        target_text = "-"
        opening_text = "카드를 한 장 뽑아보세요."

    remaining_label.config(text=str(len(deck)))
    count_label.config(text=str(draw_count))
    target_label.config(text=target_text)

    if current_card is None:
        status_label.config(text=opening_text, fg=MUTED_COLOR)
        draw_card_face(None)
    else:
        draw_card_face(current_card)


def draw_card_face(card):
    card_canvas.delete("all")
    width = int(card_canvas["width"])
    height = int(card_canvas["height"])
    x0, y0, x1, y1 = 18, 18, width - 18, height - 18

    card_canvas.create_rectangle(x0 + 4, y0 + 6, x1 + 4, y1 + 6, fill="#c6ced8", outline="")
    card_canvas.create_rectangle(x0, y0, x1, y1, fill="#ffffff", outline=LINE_COLOR, width=2)

    if card is None:
        card_canvas.create_rectangle(x0 + 18, y0 + 18, x1 - 18, y1 - 18, fill="#dce8f2", outline="")
        card_canvas.create_text(width // 2, height // 2, text="CARD", font=("Arial", 30, "bold"), fill=ACCENT_COLOR)
        return

    suit, rank = split_card(card)
    color = card_color(card)
    card_marks = (
        (48, 52, rank, 24, 0),
        (48, 86, suit, 26, 0),
        (width // 2, height // 2, suit, 86, 0),
        (width - 48, height - 52, rank, 24, 180),
        (width - 48, height - 86, suit, 26, 180),
    )

    for x, y, text, size, angle in card_marks:
        card_canvas.create_text(x, y, text=text, font=("Arial", size, "bold"), fill=color, angle=angle)


def show_help():
    messagebox.showinfo(
        "도움말",
        "기본 모드: 52장의 카드에서 한 장씩 뽑습니다.\n\n"
        "목표 모드: 목표 카드가 나올 때까지 카드를 뽑고 횟수를 확인합니다.\n\n"
        "새 게임을 누르면 현재 모드의 덱이 다시 섞입니다.",
    )


def main():
    global mode_var

    root = tk.Tk()
    root.title("카드 뽑기 게임")
    root.geometry("900x720")
    root.minsize(900, 720)

    mode_var = tk.StringVar(value="basic")
    configure_style()
    build_layout(root)
    reset_game()
    root.mainloop()


if __name__ == "__main__":
    main()
