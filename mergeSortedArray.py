from typing import List
import tkinter as tk

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        a = m - 1 # up to nums1 last element
        b = n - 1 # up to nums2 last element
        c = m + n - 1 # nums1 + nums2

        while b >= 0:
            if a >= 0 and nums1[a] > nums2[b]:
                nums1[c] = nums1[a] # should fit perfectly as nums1 already has the exact amount of elements available
                a -= 1
            else:
                nums1[c] = nums2[b]
                b -= 1
            c -= 1 # move to next element

import os
import time

def print_blocks(arr, pointer=None, label=None):
    block_row = " ".join(f"|{x:^3}|" for x in arr)
    pointer_row = ""
    if pointer is not None:
        pointer_row = "    "
        for i in range(len(arr)):
            if i == pointer:
                pointer_row += "  ^  "
            else:
                pointer_row += "     "
    if label:
        print(f"{label}: {block_row}")
    else:
        print(block_row)
    if pointer is not None:
        print(pointer_row)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def visual_merge_demo():
    nums1 = [1, 3, 5, 7, 0, 0, 0]
    nums2 = [2, 4, 6]
    m = 4
    n = 3
    a = m - 1
    b = n - 1
    c = m + n - 1
    step = 1
    while b >= 0:
        clear()
        print(f"Step {step}")
        print_blocks(nums1, pointer=c, label="nums1")
        print_blocks(nums2, pointer=b, label="nums2")
        print(f"a = {a}, b = {b}, c = {c}")
        if a >= 0 and nums1[a] > nums2[b]:
            print(f"nums1[a]={nums1[a]} > nums2[b]={nums2[b]} → nums1[c]={nums1[a]}")
            nums1[c] = nums1[a]
            a -= 1
        else:
            print(f"nums2[b]={nums2[b]} >= nums1[a]={nums1[a] if a >= 0 else 'N/A'} → nums1[c]={nums2[b]}")
            nums1[c] = nums2[b]
            b -= 1
        c -= 1
        step += 1
        time.sleep(1.2)
    clear()
    print("Final result:")
    print_blocks(nums1, label="nums1")
    print("Done!")

def visual_merge_gui():
    nums1 = [1, 3, 5, 7, 0, 0, 0]
    nums2 = [2, 4, 6]
    m = 4
    n = 3
    a = m - 1
    b = n - 1
    c = m + n - 1

    # History stack for stepping backward
    history = []
    step_data = {
        'nums1': nums1[:],
        'nums2': nums2[:],
        'a': a,
        'b': b,
        'c': c,
        'step': 1,
        'running': False
    }

    def draw_blocks(canvas, arr, y, pointers=None, colors=None, labels=None, label=None):
        x0 = 60
        block_w = 50
        block_h = 40
        # Determine which indices are pointed to and by whom
        highlight = {}  # idx: set of pointer labels
        if pointers:
            for idx, color, plabel in pointers:
                if idx is not None and 0 <= idx < len(arr):
                    if idx not in highlight:
                        highlight[idx] = set()
                    highlight[idx].add(plabel)
        for i, val in enumerate(arr):
            fill = colors[i] if colors else '#90caf9'
            # Highlight logic: if pointed to, use border color
            if i in highlight:
                # Priority: c (red), a (blue), b (orange)
                border = '#d32f2f' if 'c' in highlight[i] else ('#1976d2' if 'a' in highlight[i] else '#f57c00')
                canvas.create_rectangle(x0 + i*block_w, y, x0 + (i+1)*block_w, y+block_h, fill=fill, outline=border, width=4)
            else:
                canvas.create_rectangle(x0 + i*block_w, y, x0 + (i+1)*block_w, y+block_h, fill=fill, outline='black', width=1)
            canvas.create_text(x0 + i*block_w + block_w//2, y+block_h//2, text=str(val), font=('Arial', 16))
        if label:
            canvas.create_text(x0 - 40, y + block_h//2, text=label, font=('Arial', 14, 'bold'))
        # Draw pointers (list of (idx, color, label))
        if pointers:
            pointer_y = y + block_h + 10
            for idx, color, plabel in pointers:
                if idx is not None and 0 <= idx < len(arr):
                    canvas.create_text(x0 + idx*block_w + block_w//2, pointer_y, text=plabel, font=('Arial', 14, 'bold'), fill=color)

    def update_canvas():
        canvas.delete('all')
        # Pointers for nums1: a (blue), c (red)
        nums1_pointers = []
        if 0 <= step_data['a'] < len(step_data['nums1']):
            nums1_pointers.append((step_data['a'], '#1976d2', 'a'))
        if 0 <= step_data['c'] < len(step_data['nums1']):
            nums1_pointers.append((step_data['c'], '#d32f2f', 'c'))
        # Pointers for nums2: b (orange)
        nums2_pointers = []
        if 0 <= step_data['b'] < len(step_data['nums2']):
            nums2_pointers.append((step_data['b'], '#f57c00', 'b'))
        draw_blocks(canvas, step_data['nums1'], 30, pointers=nums1_pointers, label='nums1')
        draw_blocks(canvas, step_data['nums2'], 110, pointers=nums2_pointers, label='nums2')
        info = f"Step: {step_data['step']}   a={step_data['a']}  b={step_data['b']}  c={step_data['c']}"
        canvas.create_text(60, 210, text=info, font=('Arial', 14), anchor='nw')

        # Show calculation below arrays
        a = step_data['a']
        b = step_data['b']
        nums1 = step_data['nums1']
        nums2 = step_data['nums2']
        calc_text = ""
        if b >= 0:
            val_a = nums1[a] if a >= 0 else 'N/A'
            val_b = nums2[b]
            if a >= 0:
                result = 'nums1' if val_a > val_b else 'nums2'
                calc_text = f"{val_a} > {val_b}  →  {result}"
            else:
                calc_text = f"a < 0, so use nums2[b]={val_b}"
        else:
            calc_text = "Done!"
        canvas.create_text(60, 240, text=calc_text, font=('Arial', 13), anchor='nw', fill='#333')

        if step_data['b'] < 0:
            canvas.create_text(60, 270, text='Done!', font=('Arial', 16, 'bold'), fill='green', anchor='nw')

    def save_history():
        # Deep copy for nums1 and nums2
        history.append({
            'nums1': step_data['nums1'][:],
            'nums2': step_data['nums2'][:],
            'a': step_data['a'],
            'b': step_data['b'],
            'c': step_data['c'],
            'step': step_data['step']
        })

    def restore_history():
        if history:
            prev = history.pop()
            step_data['nums1'] = prev['nums1'][:]
            step_data['nums2'] = prev['nums2'][:]
            step_data['a'] = prev['a']
            step_data['b'] = prev['b']
            step_data['c'] = prev['c']
            step_data['step'] = prev['step']
            update_canvas()

    def animate_move(from_arr, from_idx, to_arr, to_idx, value, vertical=False):
        # Animate moving a block from (from_idx) to (to_idx) in from_arr
        steps = 16
        x0 = 60
        block_w = 50
        block_h = 40
        # Start/end positions
        if from_arr == 'nums1':
            x_start = x0 + from_idx * block_w
            y_start = 30
        else:
            x_start = x0 + from_idx * block_w
            y_start = 110
        x_end = x0 + to_idx * block_w
        y_end = 30
        for step in range(steps + 1):
            canvas.delete('move_anim')
            frac = step / steps
            x = x_start + (x_end - x_start) * frac
            y = y_start + (y_end - y_start) * frac
            # Draw moving block
            canvas.create_rectangle(x, y, x + block_w, y + block_h, fill='#fff59d', outline='#d32f2f', width=4, tags='move_anim')
            canvas.create_text(x + block_w // 2, y + block_h // 2, text=str(value), font=('Arial', 16), tags='move_anim')
            canvas.update()
            canvas.after(40)
        canvas.delete('move_anim')

    def next_step():
        if step_data['b'] < 0:
            return
        save_history()
        a = step_data['a']
        b = step_data['b']
        c = step_data['c']
        nums1 = step_data['nums1']
        nums2 = step_data['nums2']
        update_canvas()  # Show state before move
        canvas.update()
        if a >= 0 and nums1[a] > nums2[b]:
            animate_move('nums1', a, 'nums1', c, nums1[a], vertical=False)
            nums1[c] = nums1[a]
            step_data['a'] -= 1
        else:
            animate_move('nums2', b, 'nums1', c, nums2[b], vertical=True)
            nums1[c] = nums2[b]
            step_data['b'] -= 1
        step_data['c'] -= 1
        step_data['step'] += 1
        update_canvas()

    def auto_step():
        if step_data['running']:
            next_step()
            if step_data['b'] >= 0:
                root.after(800, auto_step)
            else:
                step_data['running'] = False

    def start_auto():
        if not step_data['running'] and step_data['b'] >= 0:
            step_data['running'] = True
            auto_step()

    def repeat_animation():
        # Reset everything to initial state
        history.clear()
        step_data['nums1'] = [1, 3, 5, 7, 0, 0, 0]
        step_data['nums2'] = [2, 4, 6]
        step_data['a'] = 3
        step_data['b'] = 2
        step_data['c'] = 6
        step_data['step'] = 1
        step_data['running'] = False
        update_canvas()

    root = tk.Tk()
    root.title('Merge Sorted Arrays Visualizer')
    canvas = tk.Canvas(root, width=500, height=270, bg='white')
    canvas.pack()

    btn_frame = tk.Frame(root)
    btn_frame.pack()
    next_btn = tk.Button(btn_frame, text='Next Step', command=next_step)
    next_btn.grid(row=0, column=0, padx=10, pady=5)
    auto_btn = tk.Button(btn_frame, text='Auto', command=start_auto)
    auto_btn.grid(row=0, column=1, padx=10, pady=5)
    back_btn = tk.Button(btn_frame, text='Back Step', command=restore_history)
    back_btn.grid(row=0, column=2, padx=10, pady=5)
    repeat_btn = tk.Button(btn_frame, text='Repeat', command=repeat_animation)
    repeat_btn.grid(row=0, column=3, padx=10, pady=5)
    quit_btn = tk.Button(btn_frame, text='Quit', command=root.destroy)
    quit_btn.grid(row=0, column=4, padx=10, pady=5)

    update_canvas()
    root.mainloop()

if __name__ == "__main__":
    visual_merge_gui()