
import io, math
import chess, chess.svg
from PIL import Image, ImageDraw


def _eval_to_frac(cp_white, mate):
    if mate is not None: return 1.0 if mate > 0 else 0.0
    if cp_white is None: return 0.5
    return 0.5 + math.tanh(cp_white/600.0)*0.5

def _board_png(fen: str, last_uci: str|None, size=480) -> Image.Image:
    import cairosvg 
    b = chess.Board(fen)
    last = chess.Move.from_uci(last_uci) if last_uci else None
    svg = chess.svg.board(board=b, lastmove=last, size=size)
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"))
    return Image.open(io.BytesIO(png)).convert("RGBA" )

def render_position(fen: str, cp_white, mate, last_uci: str|None=None) -> Image.Image:
    img = _board_png(fen, last_uci)
    w,h = img.size
    bar_w = int(w*0.06)
    bar = Image.new("RGBA",(bar_w,h),(30,30,30,255))
    draw = ImageDraw.Draw(bar)
    frac = _eval_to_frac(cp_white, mate)
    fill_h = int(h*frac)
    draw.rectangle([0, h-fill_h, bar_w, h], fill=(240,240,240,255))
    out = Image.new("RGBA",(w+bar_w,h))
    out.paste(bar,(0,0))
    out.paste(img,(bar_w,0), img)
    return out
