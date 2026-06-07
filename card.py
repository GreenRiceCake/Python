import random
import tkinter as tk
from tkinter import messagebox


SUITS = ("♠", "♦", "♥", "♣")
RANKS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
RED_SUITS = ("♦", "♥")

CARD_WIDTH = 220
CARD_HEIGHT = 300

deck = []
target_card = None
current_card = None
draw_count = 0

mode_var = None
title_label = None
card_canvas = None
status_label = None
remaining_label = None
count_label = None
target_label = None
history_list = None
draw_button = None


def make_card(suit, rank):
    return f"{suit} {rank}"


def split_card(card):
    return card.split()


def make_deck():
    new_deck = []
    for suit in SUITS:
        for rank in RANKS:
            new_deck.append(make_card(suit, rank))
    random.shuffle(new_deck)
    return new_deck


def reset_game():
    global deck, target_card, current_card, draw_count

    deck = make_deck()
    current_card = None
    draw_count = 0

    if mode_var.get() == "target":
        target_card = random.choice(deck)
    else:
        target_card = None

    draw_button.config(state="normal")
    history_list.delete(0, tk.END)
    update_screen()


def draw_card():
    global current_card, draw_count

    if len(deck) == 0:
        status_label.config(text="카드를 모두 뽑았습니다.")
        draw_button.config(state="disabled")
        return

    current_card = deck.pop()
    draw_count += 1
    history_list.insert(0, f"{draw_count}. {current_card}")

    if mode_var.get() == "target" and current_card == target_card:
        status_label.config(text=f"성공! {draw_count}번 만에 {current_card} 카드를 뽑았습니다.")
        draw_button.config(state="disabled")
    elif len(deck) == 0:
        status_label.config(text="마지막 카드까지 뽑았습니다.")
        draw_button.config(state="disabled")
    else:
        status_label.config(text=f"{current_card} 카드를 뽑았습니다.")

    update_screen()


def update_screen():
    if mode_var.get() == "target":
        title_label.config(text="특정 카드 뽑기")
        target_label.config(text=f"목표 카드: {target_card}")
        start_text = "목표 카드를 찾아보세요."
    else:
        title_label.config(text="기본 카드 뽑기")
        target_label.config(text="목표 카드: -")
        start_text = "카드를 한 장 뽑아보세요."

    remaining_label.config(text=f"남은 카드: {len(deck)}")
    count_label.config(text=f"뽑은 횟수: {draw_count}")

    if current_card is None:
        status_label.config(text=start_text)
    draw_card_image(current_card)


def draw_card_image(card):
    card_canvas.delete("all")
    x0, y0 = 20, 20
    x1, y1 = CARD_WIDTH - 20, CARD_HEIGHT - 20

    card_canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black", width=2)

    if card is None:
        card_canvas.create_text(CARD_WIDTH // 2, CARD_HEIGHT // 2, text="CARD", font=("Arial", 26, "bold"))
        return

    suit, rank = split_card(card)
    color = "red" if suit in RED_SUITS else "black"
    card_canvas.create_text(45, 45, text=rank, font=("Arial", 20, "bold"), fill=color)
    card_canvas.create_text(45, 75, text=suit, font=("Arial", 22, "bold"), fill=color)
    card_canvas.create_text(CARD_WIDTH // 2, CARD_HEIGHT // 2, text=suit, font=("Arial", 70, "bold"), fill=color)
    card_canvas.create_text(CARD_WIDTH - 45, CARD_HEIGHT - 45, text=rank, font=("Arial", 20, "bold"), fill=color)
    card_canvas.create_text(CARD_WIDTH - 45, CARD_HEIGHT - 75, text=suit, font=("Arial", 22, "bold"), fill=color)


def show_help():
    messagebox.showinfo(
        "도움말",
        "기본 모드: 카드를 한 장씩 뽑습니다.\n\n"
        "목표 모드: 목표 카드가 나올 때까지 뽑습니다.\n\n"
        "새 게임: 덱을 다시 섞고 처음부터 시작합니다.",
    )


def main():
    global mode_var, title_label, card_canvas, status_label
    global remaining_label, count_label, target_label, history_list, draw_button

    root = tk.Tk()
    root.title("카드 뽑기 게임")
    root.geometry("480x500")

    mode_var = tk.StringVar(value="basic")

    top_frame = tk.Frame(root, pady=8)
    top_frame.pack()

    tk.Radiobutton(top_frame, text="기본", value="basic", variable=mode_var, command=reset_game).pack(side="left")
    tk.Radiobutton(top_frame, text="목표", value="target", variable=mode_var, command=reset_game).pack(side="left")
    tk.Button(top_frame, text="도움말", command=show_help).pack(side="left", padx=8)

    title_label = tk.Label(root, text="", font=("Malgun Gothic", 18, "bold"))
    title_label.pack(pady=5)

    middle_frame = tk.Frame(root)
    middle_frame.pack(fill="both", expand=True, padx=15)

    left_frame = tk.Frame(middle_frame)
    left_frame.pack(side="left", expand=True)

    card_canvas = tk.Canvas(left_frame, width=CARD_WIDTH, height=CARD_HEIGHT, bg="lightgray")
    card_canvas.pack()

    status_label = tk.Label(left_frame, text="", font=("Malgun Gothic", 11))
    status_label.pack(pady=8)

    button_frame = tk.Frame(left_frame)
    button_frame.pack()
    draw_button = tk.Button(button_frame, text="카드 뽑기", command=draw_card, width=10)
    draw_button.pack(side="left", padx=4)
    tk.Button(button_frame, text="새 게임", command=reset_game, width=10).pack(side="left", padx=4)
    tk.Button(button_frame, text="종료", command=root.destroy, width=10).pack(side="left", padx=4)

    right_frame = tk.Frame(middle_frame, padx=15)
    right_frame.pack(side="right", fill="y")

    remaining_label = tk.Label(right_frame, text="", font=("Malgun Gothic", 12))
    count_label = tk.Label(right_frame, text="", font=("Malgun Gothic", 12))
    target_label = tk.Label(right_frame, text="", font=("Malgun Gothic", 12))
    remaining_label.pack(anchor="w", pady=3)
    count_label.pack(anchor="w", pady=3)
    target_label.pack(anchor="w", pady=3)

    tk.Label(right_frame, text="뽑은 기록", font=("Malgun Gothic", 12, "bold")).pack(anchor="w", pady=(15, 3))
    history_list = tk.Listbox(right_frame, width=18, height=13)
    history_list.pack()

    reset_game()
    root.mainloop()


if __name__ == "__main__":
    main()
