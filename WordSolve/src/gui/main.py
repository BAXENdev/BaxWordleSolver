
import tkinter as tk

class PALETTE():
    BG_GRAY = '#373737'
    ITEM_GRAY = '#404040'
    SELECT_GRAY = '#4b4b4b'
    ITEM_BLUE = '#04006f'
    FRAME_ARGS = { 'bg':BG_GRAY }
    ITEM_ARGS = { 'bg':BG_GRAY, 'fg':ITEM_GRAY }
    INTERACTABLE_ARGS = { 'bg':BG_GRAY, 'fg':ITEM_GRAY, 'highlightcolor':SELECT_GRAY }
    LABEL_ARGS = { 'bg':BG_GRAY, 'fg':ITEM_BLUE }
    TEXT_ARGS = { 'bg':ITEM_GRAY, 'fg':ITEM_BLUE, 'highlightcolor':SELECT_GRAY }

def init(root, width, height):
    root.geometry(f'{width}x{height}')
    root.configure(**PALETTE.FRAME_ARGS)
    frameWidth = width / 2
    
    # GAME FRAME
    gameFrame = tk.Frame(root, **PALETTE.FRAME_ARGS, width=frameWidth)
    gameFrame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.Y)
    # gameFrame.pack(side=tk.LEFt)
    gFramePadding = 25
    entryFramePadding = 4
    entryFrame = tk.Frame(gameFrame)
    entryFrame.pack(padx=gFramePadding, pady=gFramePadding)
    for i in range(6):
        for j in range(5):
            entry = tk.Entry(entryFrame, width=20, **PALETTE.TEXT_ARGS)
            entry.grid(row=i, column=j)

    # LIST FRAME
    listFrame = tk.Frame(root, **PALETTE.FRAME_ARGS, width=frameWidth)
    listFrame.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.Y)
    # listFrame.pack(side=tk.RIGHT)
    
    root.mainloop()

def test1():
    root = tk.Tk()
    root.geometry("600x600")
    frame = tk.Frame(bg='#3e1d85')
    frame.pack()
    for i in range(3):
        for j in range(4):
            label = tk.Entry(frame, textvariable=f"R{i}/C{j}")
            label.grid(row = i, column = j, padx=2, pady=2)
    root.mainloop()

def test2():
    root = tk.Tk()
    custBut = tk.Canvas(root, bg=PALETTE.BG_GRAY, width=200, height=200)
    custBut.pack()

    root.mainloop()

if __name__ == '__main__':
    # root = tk.Tk()
    # init(root, 1000, 600)
    # test()
    test2()
